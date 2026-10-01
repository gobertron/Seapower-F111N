#!/usr/bin/env python3
"""Apply the MudPig maritime presets to an existing V5 or rebuilt package."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import sys

HARP = 'usn_agm-84c'
TANK = 'ran_tank_600_fb111n'
ANTI_SHIP = ('AntiShip', 'AntiShipHeavy', 'AntiShipLongRange')
DESCRIPTION = (
    'Reinforced fast maritime-strike bomber. Anti-ship and long-range anti-ship '
    'missions are its primary roles, with conventional and precision bombing '
    'options retained. Anti Ship carries two AIM-9L and two wing-mounted '
    'AGM-84C. Heavy Anti Ship carries four wing-mounted and three internal '
    'AGM-84C. Long Range Anti Ship carries two wing-mounted AGM-84C, two '
    'external tanks, two external AIM-9L and three internal AGM-84C. Heavy anti-ship '
    'carries no air-to-air missiles. Default remains defensive air-to-air only.'
)


def configure_aircraft(data):
    data['Animations']['AnimationFile_1'] = 'animations_ran_fb111n'
    data['WeaponSystems']['NumberOfWeaponSystems'] = '3'
    original = data['WeaponSystems']['AvailableLoadouts'].split(',')
    remaining = [x for x in original if x not in ANTI_SHIP]
    split = next((i for i, x in enumerate(remaining) if x.startswith('Strike')), len(remaining))
    presets = remaining[:split] + list(ANTI_SHIP) + remaining[split:]
    data['WeaponSystems']['AvailableLoadouts'] = ','.join(presets)
    data['WeaponSystem1'].update(HarpoonPositions='0,0.0011,0.002',
                                 HarpoonRotations='-2,0,0')
    # Native BombBay properties; the three stations remain fixed to the fuselage.
    data['WeaponSystem3'] = {
        'Type': 'Hardpoint', 'SystemName': 'BombBay',
        'AssociatedSensors': 'SensorSystem3',
        'OpenSystemAnimation': 'Bay_Open', 'CloseSystemAnimation': 'Bay_Close',
        'FiringArcs': '-15,15', 'NumberOfStations': '3',
        'Station1': '-0.005,-0.006,0.070',
        'Station2': '0.005,-0.006,0.070',
        'Station3': '0,-0.006,0.075',
        'Station1Rotation': '0,0,0', 'Station2Rotation': '0,0,0',
        'Station3Rotation': '0,0,0',
        'HideWeaponsInsideSystem': 'True', 'ModuleType': 'Weapon',
    }
    hidden = 'tank1,tank2,MER_Outer_Right,MER_Outer_Left,MER_Inner_Left,MER_Inner_Right,pave_body,pave'
    stores = {
        'AntiShip': {1: 'usn_aim-9l|AAM', 2: 'usn_aim-9l|AAM',
                     3: HARP + '|Harpoon', 4: HARP + '|Harpoon'},
        'AntiShipHeavy': {i: HARP + '|Harpoon' for i in range(3, 7)},
        'AntiShipLongRange': {1: 'usn_aim-9l|AAM', 2: 'usn_aim-9l|AAM',
                              3: TANK + '|Tank', 4: TANK + '|Tank',
                              5: HARP + '|Harpoon', 6: HARP + '|Harpoon'},
    }
    for name in presets:
        if name in stores:
            data['WeaponSystem1' + name] = {
                'SubModelsToHide': hidden, 'ReadyUpTime': '30', 'CoolDownTime': '60',
                **{f'Station{k}': v for k, v in stores[name].items()},
                'LevelAttack': 'Missiles',
            }
        internal = {'LevelAttack': 'Missiles'}
        if name in ('AntiShipHeavy', 'AntiShipLongRange'):
            internal.update({f'Station{i}': HARP for i in range(1, 4)})
        data['WeaponSystem3' + name] = internal


def bay_animations(common):
    animation = deepcopy(common)
    for action, start, end in [('Bay_Open', 0, 90), ('Bay_Close', 90, 0)]:
        # Pave Tack uses the same cavity, so it is hidden for anti-ship presets
        # and is not moved by this aircraft's missile-bay door actions.
        animation[action] = {'NumberOfSequencesToPlay': '2'}
        for number, side, sign in [(1, 'l', 1), (2, 'r', -1)]:
            sequence = 'MudPig_' + action + '_' + side
            animation[action].update({f'Sequence{number}': sequence,
                                       f'Sequence{number}_Model': 'bay_' + side})
            animation[sequence] = {
                'NumberOfSteps': '2',
                'Step1': f'0|x,y,z|x,y,{start * sign}|EaseInOut',
                'Step2': f'3|x,y,z|x,y,{end * sign}|EaseInOut',
            }
    for unused in ['Bay_Open_l', 'Bay_Open_r', 'Bay_Close_l', 'Bay_Close_r',
                   'Pave_Open', 'Pave_Open2', 'Pave_Close', 'Pave_Close2']:
        animation.pop(unused, None)
    return animation


def summarise(data):
    result = {}
    for name in data['WeaponSystems']['AvailableLoadouts'].split(','):
        combined = Counter()
        by_system = {}
        for i in (1, 3):
            definition = data[f'WeaponSystem{i}']
            counts = Counter()
            for k, value in data.get(f'WeaponSystem{i}{name}', {}).items():
                if not k.startswith('Station') or not k[7:].isdigit():
                    continue
                parts = value.split('|')
                quantity = len(definition[parts[1] + 'Positions'].split('|')) if len(parts) > 1 else 1
                counts[parts[0]] += quantity
            combined.update(counts)
            by_system[i] = dict(counts)
        item = {'stores': dict(combined),
                'total_fuel_kg': int(data['Performance']['MaxFuel']) + combined.get(TANK, 0) * 1800}
        if name in ANTI_SHIP:
            item.update(wing_stores=by_system[1], internal_bay_stores=by_system[3])
        result[name] = item
    return result


def apply_package(package):
    # Local import allows build_mod to invoke this after its normal source build.
    from build_mod import read_ini, write_ini
    package = Path(package).resolve()
    mod = package / 'RAN-F111N-Naval-Wing'
    aircraft = mod / 'aircraft/ran_fb-111n.ini'
    data = read_ini(aircraft)
    configure_aircraft(data)
    write_ini(aircraft, data)
    common = read_ini(mod / 'animations/animations_ran_f111n.ini')
    write_ini(mod / 'animations/animations_ran_fb111n.ini', bay_animations(common))
    manifest_file = package / 'loadout_manifest.json'
    manifest = json.loads(manifest_file.read_text())
    manifest['ran_fb-111n']['primary_role'] = 'Anti-ship and long-range anti-ship strike, plus bombing'
    manifest['ran_fb-111n']['loadouts'] = summarise(data)
    manifest_file.write_text(json.dumps(manifest, indent=2) + '\n')
    names_file = mod / 'language_en/aircraft_names.ini'
    names = read_ini(names_file)
    names['ran_fb-111n']['DefaultDescription'] = (
        'Fictional RAN-RAAF naval aviation programme. ' + DESCRIPTION +
        ' RAN operates the ships and carrier support; the RAAF supplies the '
        'specialist airpower and training. Squadron references are heritage tributes.'
    )
    write_ini(names_file, names)
    info_file = mod / '_info.ini'
    info = read_ini(info_file)
    info['Language_en']['Name'] = 'RAN F-111N Naval Wing V5.2.1'
    info['Language_en']['Description'] = (
        'WaterPig fighter, MudPig maritime-strike bomber, SprintPig reconnaissance, '
        'ScreamPig electronic attack. Exact anti-ship presets, animated internal '
        'Harpoon bay, real fuel tanks and RAN liveries.'
    )
    write_ini(info_file, info)


if __name__ == '__main__':
    apply_package(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
