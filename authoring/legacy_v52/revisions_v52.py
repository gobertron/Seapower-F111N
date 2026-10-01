#!/usr/bin/env python3
"""Apply the screenshot corrections to a V5.1 package or a source rebuild."""
from pathlib import Path
from collections import Counter
import json,re,sys
from build_mod import read_ini,write_ini

def apply_package(package):
    package=Path(package);mod=package/'RAN-F111N-Naval-Wing'
    for short in ['f','fb','rf','ef']:
        p=mod/f'aircraft/ran_{short}-111n.ini';d=read_ini(p)
        d['General']['CarrierCapable']='True'
        if short=='fb':
            # StationParent uses the original world-space station position.
            # A 0.343 m Harpoon body touches the pylon at this raised offset.
            d['WeaponSystem1']['HarpoonPositions']='0,0.0011,0.002'
            d['WeaponSystem1AntiShipLongRange'].update(
                Station1='usn_aim-9l|AAM',Station2='usn_aim-9l|AAM')
        if short=='ef':
            ws=d['WeaponSystem1'];ws['NumberOfStations']='6'
            for k in list(ws):
                if re.match(r'Station[78](?:Parent|Rotation)?$',k):del ws[k]
            # One pod under each outer pylon; top of the shipped pod model is
            # +0.004804 above its origin, meeting the pylon foot near -0.0013.
            ws['Station5']='0.068848,-0.0061,0.008404'
            ws['Station6']='-0.068848,-0.0061,0.008404'
            ws['Station5Rotation']='0,0,0';ws['Station6Rotation']='0,0,0'
            for name in d['WeaponSystems']['AvailableLoadouts'].split(','):
                ld=d['WeaponSystem1'+name]
                ld.pop('Station7',None);ld.pop('Station8',None)
            # Aircraft-mounted sensors follow the native EA-6B pattern. The
            # pod containers provide their meshes and mass, not extra sensors.
            d['SensorSystem6']={'Type':'ECM','SystemName':'RAN_ALQ99N_1',
                'Mount':'hang2','ModuleType':'Sensor'}
            d['SensorSystem7']={'Type':'ECM','SystemName':'RAN_ALQ99N_2',
                'Mount':'hang1','ModuleType':'Sensor'}
            d['SensorSystems']['NumberOfSensorSystems']='7'
        if short=='rf':
            perf=d['Performance']
            perf.update(MaxSpeedAtSeaLevel='1985',MachLimit='3.0',
                PerEngineMaxThrust='320000',PerEngineMaxAfterburnerThrust='480000',
                SpeedAndRange_Cruise='2.52,2300',SpeedAndRange_Max='3.0,0.8',
                SpeedAndRange_Afterburner='3.0,0.2',
                Altitudes='50,300,1000,3000,6000,10000,20000,37000,50000,65000')
            d['FlightModel'].update(VelocityGain='0.3408',ThrustGain='0.975')
        write_ini(p,d)
    for i in [1,2]:
        p=mod/f'ammunition/ran_alq-131n_{i}.ini';d=read_ini(p)
        d.pop('SensorSystems',None);d.pop('SensorSystem1',None)
        write_ini(p,d)
    for i in [3,4]:
        (mod/f'ammunition/ran_alq-131n_{i}.ini').unlink(missing_ok=True)
    sensors=read_ini(mod/'systems/sensors.ini')
    for k in ['RAN_ALQ99N_3','RAN_ALQ99N_4']:sensors.pop(k,None)
    write_ini(mod/'systems/sensors.ini',sensors)
    names=read_ini(mod/'language_en/ammunition_names.ini')
    for i in [3,4]:names['AmmunitionNames'].pop(f'ran_alq-131n_{i}',None)
    write_ini(mod/'language_en/ammunition_names.ini',names)
    language=read_ini(mod/'language_en/aircraft_names.ini')
    for k,v in language.items():
        for key,val in v.items():
            if key=='DefaultDescription' and 'ef-111n' in k:
                v[key]='Fleet electronic attack aircraft with two wing-mounted ECM pods, two independently mounted offensive ECM systems, two AIM-9L, two external fuel tanks and 160 chaff.'
            if key=='DefaultDescription' and 'rf-111n' in k:
                v[key]='Fastest Naval Wing variant. Fictional Mach 3 maximum with Mach 2.52 cruise, three times the Mach 0.84 cruise of the other variants, increased thrust and acceleration, two defensive AIM-9L and four external tanks.'
            if key=='DefaultDescription' and 'fb-111n' in k:
                v[key]=('Maritime-strike bomber with anti-ship and long-range anti-ship primary roles, plus conventional and precision bombing. Anti Ship: two AIM-9L and two wing AGM-84C. Heavy Anti Ship: four wing and three internal AGM-84C. Long Range Anti Ship: two external AIM-9L, two wing AGM-84C, two tanks and three internal AGM-84C.')
    write_ini(mod/'language_en/aircraft_names.ini',language)
    info=read_ini(mod/'_info.ini')
    info['Language_en']['Name']='RAN F-111N Naval Wing V5.2.1'
    write_ini(mod/'_info.ini',info)
    manifest=json.loads((package/'loadout_manifest.json').read_text())
    for unit,entry in manifest.items():
        d=read_ini(mod/f'aircraft/{unit}.ini')
        entry['mach_limit']=float(d['Performance']['MachLimit'])
        entry['cruise_mach']=float(d['Performance']['SpeedAndRange_Cruise'].split(',')[0])
        entry['carrier_capable']=True
        for name,spec in entry['loadouts'].items():
            counts=Counter();by_system={}
            for i in range(1,int(d['WeaponSystems']['NumberOfWeaponSystems'])+1):
                ws=d[f'WeaponSystem{i}'];st=Counter()
                if ws['Type']!='Hardpoint':continue
                for key,value in d.get(f'WeaponSystem{i}{name}',{}).items():
                    if not re.fullmatch(r'Station\d+',key):continue
                    bits=value.split('|');ammo=bits[0]
                    n=len(ws[bits[1]+'Positions'].split('|')) if len(bits)>1 else 1
                    st[ammo]+=n
                by_system[i]=dict(st);counts.update(st)
            spec['stores']=dict(counts)
            if unit=='ran_fb-111n' and name.startswith('AntiShip'):
                spec['wing_stores']=by_system.get(1,{})
                spec['internal_bay_stores']=by_system.get(3,{})
            if unit=='ran_ef-111n':spec['offensive_ecm_systems']=2
    (package/'loadout_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    apply_package(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent.parent)
