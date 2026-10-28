"""Build readable Unit Reference stories from the shipped aircraft settings.

The supplied screenshot suggests semicolons end language values in Sea Power.
Keep descriptions on one physical line and avoid comment or markup syntax.
"""
import re

from investment_programme import BLOCKS


NAMES = {
    'f': ('F-111N', 'WaterPig'),
    'fb': ('FB-111N', 'MudPig'),
    'rf': ('RF-111N', 'SprintPig'),
    'ef': ('EF-111N', 'ScreamPig'),
}

STORIES = {
    'f': {
        1980: "Australia retains fixed-wing carrier aviation and funds a joint RAN-RAAF programme to protect its task groups far from shore. WaterPig develops the naval fleet-interceptor concept into a heavy fighter, exchanging the strike family's broad stores inventory for an outer air-defence screen and sustained combat air patrols.",
        1985: "Continued Australian funding turns the first fleet interceptor into a more responsive escort for an expanding carrier force. The second block concentrates on wider search coverage, uprated propulsion and missile improvements, giving patrol crews more room to search while keeping the proven fleet-defence mission at the centre of the design.",
        1995: "A major Australian reinvestment keeps the heavy naval fighter relevant alongside newer aircraft. The programme combines an F110-class engine adaptation with a digital fleet-defence radar concept, AMRAAM integration and shared radar tracks. WaterPig now acts as both an interceptor and a forward contributor to the carrier group's air picture.",
        2003: "The mature naval fighter receives a final funded upgrade for a more crowded and contested air environment. Improved propulsion, broader radar coverage and updated defensive missiles support flexible patrol positioning. WaterPig remains the wing's specialist for meeting hostile aircraft before they can threaten the carrier and its supporting ships.",
    },
    'fb': {
        1980: "Australia's retained carrier force needs a strike aircraft able to cover distant sea lanes without giving up its land-attack role. MudPig becomes the programme's versatile workhorse, combining a concealed weapons bay with wing stations for maritime attack, bombing and defensive missiles. The naval conversion is funded as a long-term national capability.",
        1985: "Lessons from the first naval strike block lead Australia to invest in a more flexible attack aircraft rather than a separate platform for every mission. MudPig gains wider radar coverage and newer precision and anti-radiation weapons. The emphasis shifts from simply carrying heavy stores to choosing the right weapons for defended targets.",
        1995: "A major engine and mission-system investment extends the Australian naval strike programme into the digital era. MudPig broadens its stand-off options while retaining conventional bombing, maritime attack and interception fits. Shared radar tracks help it work with the fleet, and its internal bay remains central to the programme's adaptable approach to stores carriage.",
        2003: "Australia's final major MudPig block focuses on precision attack, updated maritime weapons and more flexible task-group support. Continued funding keeps the familiar naval airframe in service through new propulsion and sensors. Its value lies in changing mission fits, from heavy anti-ship attack to stand-off strike, rather than carrying every available weapon at once.",
    },
    'rf': {
        1980: "Australia funds a dedicated reconnaissance member of the naval family so the carrier force can search distant approaches before committing its strike aircraft. SprintPig prioritises reconnaissance and electronic intelligence over offensive stores. Its defensive weapons and fuel options support an aircraft intended to find threats, report their presence and preserve the information it gathers.",
        1985: "Continued Australian investment improves the reconnaissance aircraft's search coverage, propulsion and electronic support. SprintPig remains a specialist scout rather than a second strike platform. The upgrade supports wider searches around the task group and gives crews the choice between endurance with external tanks and a lighter reconnaissance fit.",
        1995: "The naval reconnaissance programme receives a major engine and digital mission-system refit. Improved electronic intelligence and shared radar tracks make SprintPig a more useful forward scout for the carrier group. Australia keeps a dedicated reconnaissance role within the family, preserving the distinction between locating a threat and sending armed strike aircraft to engage it.",
        2003: "The final reconnaissance block reflects sustained Australian investment in keeping the fleet informed beyond the carrier's immediate horizon. Wider radar coverage, stronger electronic support and updated defensive missiles improve the scout's flexibility. SprintPig continues to favour information gathering and endurance, with a lighter fit available when external fuel is less valuable than reduced stores carriage.",
    },
    'ef': {
        1980: "Australia develops a dedicated electronic-attack escort alongside its naval fighters and strike aircraft. ScreamPig is intended to support a task group's operations against radar-directed threats, carrying two external jammer pods and an integrated electronic-support fit. Its crew concentrates on electronic attack and escort duties, with defensive missiles and a selectable anti-radiation mission.",
        1985: "The second ScreamPig block strengthens Australia's investment in specialist carrier-based electronic attack. More capable jamming settings, wider radar coverage and HARM integration broaden its escort options. The aircraft continues to trade gun armament and general-purpose strike stores for its electronic mission, helping the rest of the naval wing operate around hostile radar systems.",
        1995: "A major propulsion and mission-system refit keeps Australia's electronic escort alongside the upgraded fighter and strike families. Improved electronic support, shared radar tracks and more capable jammer settings make ScreamPig a stronger partner for coordinated task-group operations. The programme retains two physical jammer pods and a distinct electronic-attack crew mission.",
        2003: "Australia's mature electronic-attack aircraft receives stronger propulsion, broader search coverage and its most capable programme jamming settings. ScreamPig remains an escort and suppression specialist, intended to support the rest of the wing rather than replace its fighters or bombers. Modern defensive missiles accompany the established two-pod electronic-attack arrangement.",
    },
}


def _selected_stores(aircraft, presets):
    stores = set()
    for section, values in aircraft.items():
        if not any(re.fullmatch(r'WeaponSystem\d+' + re.escape(preset), section)
                   for preset in presets):
            continue
        for key, value in values.items():
            if re.fullmatch(r'Station\d+', key):
                stores.add(value.split('|', 1)[0])
    return stores


def _radar(aircraft, sensors):
    for section, values in aircraft.items():
        if re.fullmatch(r'SensorSystem\d+', section) and values.get('Type') == 'Radar':
            sensor = sensors[values['SystemName']]
            if sensor['Type'] == 'DirectedSearch':
                return sensor
    raise ValueError('Unit Reference card requires a search radar')


def description(role, year, aircraft_data, presets, catalog, sensors):
    """Return one INI-safe description for a dated aircraft's reference card."""
    model, nickname = NAMES[role]
    block = BLOCKS[year]
    stores = _selected_stores(aircraft_data, presets)

    def name(prefix):
        matches = sorted(store for store in stores if store.startswith('ran_nw_' + prefix))
        if len(matches) != 1:
            raise ValueError(f'{model} {year}: expected one selected {prefix}, found {matches}')
        return catalog[matches[0]]['name']

    paragraphs = [f"{model} {nickname}, {year}. {block['name']}. Alternate-history Australian Naval Wing. "
                  + STORIES[role][year]]
    radar = _radar(aircraft_data, sensors)
    left, right = (float(value) for value in radar['ViewArcs'].split('|')[0].split(','))
    coverage = f'{abs(left):g} degrees left and {right:g} degrees right of the nose'
    targets = 'air targets' if radar['Role'] == 'Air' else 'air, surface and land targets'
    sharing = ('Radar tracks are shared by datalink.' if radar['HasDataLink'] == 'True'
               else 'Radar detections remain local to the aircraft.')
    paragraphs.append(f'This block searches for {targets}, with a {right-left:g}-degree forward sector covering {coverage}. '
                      + sharing + ' Detection still depends on target size, altitude, aspect and jamming.')

    gun = aircraft_data.get('WeaponMagazineM61')
    gun_text = f"an M61 Vulcan with {int(gun['Ammunition1_Count']):,} rounds" if gun else 'no gun'
    if role == 'f':
        paragraphs.append(f"Selectable armament includes {name('aim9') if year < 2003 else name('asraam')}, "
                          f"{name('aim7') if year < 1995 else name('aim120')}, {name('aim54')} and {gun_text}. "
                          'Long-range patrol fits exchange wing stores for external fuel tanks. '
                          'Phoenix has a separate targeting controller, and the fighter radar does not provide surface search.')
    elif role == 'fb':
        extra = ('GBU-15 and Paveway III add further precision options. ' if year == 1985 else
                 'Popeye and SLAM add stand-off strike options. ' if year == 1995 else
                 'SLAM-ER, JDAM and JSOW add further stand-off and precision options. ' if year == 2003 else '')
        paragraphs.append(f"Selectable fits include period air-to-air missiles, {name('harpoon')}, "
                          f"{name('maverick')}, conventional bombs, Paveway and anti-radiation weapons. "
                          f"The fixed armament is {gun_text}. "
                          + extra + 'Heavy Anti-Ship carries four wing and three internal Harpoons. '
                          'Other bay fits support bombing, precision attack or interception. '
                          'Designation pods and removable EW pods are fitted only to the relevant presets.')
    elif role == 'rf':
        paragraphs.append(f"Defensive armament is {name('aim9') if year < 2003 else name('asraam')} and {gun_text}. "
                          'Reconnaissance fits carry up to four external fuel tanks. ReconFast removes the tanks. '
                          'Electronic intelligence complements the radar and infrared sensors, while the aircraft remains dedicated to reconnaissance.')
    else:
        arm = name('standardarm') if year == 1980 else name('harma' if year == 1985 else 'harmc')
        paragraphs.append(f"The electronic-attack fit retains two physical ECM pods and two offensive ECM systems, with {gun_text}. "
                          f"Defensive armament is {name('aim9') if year < 2003 else name('asraam')}. "
                          f'EscortSEAD adds {arm}. Fuel-tank fits support endurance, while electronic support and defensive countermeasures support the escort role.')

    performance = aircraft_data['Performance']
    thrust = float(performance['PerEngineMaxAfterburnerThrust']) / 1000
    paragraphs.append(f"Power comes from the programme's {block['engine']}, configured for {thrust:g} kN per engine in afterburner. "
                      f"The common maximum is Mach {float(performance['MachLimit']):g}. "
                      f"Configured empty mass is {int(performance['EmptyMass']):,} kg, with {int(performance['MaxFuel']):,} kg internal fuel before external tanks. "
                      'Naval engineering and upgrade performance are fictional programme estimates.')
    result = ' '.join(paragraphs)
    if any(token in result for token in (';', '//', '\n', '\r', '[', ']')):
        raise ValueError('Unsafe Unit Reference description syntax')
    return result
