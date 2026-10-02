"""Generate the bay guide and combined release breakdown from current data."""
from bay_loadouts import BAY_UPGRADE_MASS
from era_upgrade import ROOT, YEARS, unit_id


def write(docs, manifest, stores, table, number):
    total = sum(len(s['loadouts']) for s in manifest.values())
    new_fits = sum('Bay' in name for s in manifest.values() for name in s['loadouts'])
    text = """# V8 MudPig internal bay and armed carrier recovery

Version 8 retains three physical stations, original concealment and the Bay_Open/Bay_Close door actions. Bay targeting now includes the dedicated Phoenix controller. Single-store suspension adapters offset Phoenix 10 cm rearward and Shrike 50 cm rearward to accommodate their native origin/collider envelopes. The supplied carrier configuration has no condition requiring an empty bay for launch or recovery. Actual armed recovery has not been runtime-tested.

## Investment and capacity

Real Australian F-111 investment included Pave Tack/Harpoon and the Avionics Update Program. These naval bay integrations extend that history within the hypothetical Naval Wing programme; they are not historical F-111 certifications. Estimated adapters and interfaces add 40/50/60/75 kg to MudPig empty mass for 1980/1985/1995/2003. Bay readiness improves to 30/25/20/15 seconds with the existing dated programme. External designation/control pods leave the bay available.

"""
    text += table(['Internal store', 'Maximum selected', 'Editions'], [
        ['Mk 82', 3, 'All'], ['Harpoon', 3, 'All; edition-specific missile'],
        ['Mk 83 / Mk 84', 2, 'All'], ['GBU-12', 2, 'All; external laser pod'],
        ['Maverick', 2, 'All; edition-specific seeker'], ['Phoenix', 2, 'All; dedicated air-targeting controller'],
        ['Shrike', 2, '1980 Shrike fit'], ['SLAM', 2, '1995 / 2003; external control pod'],
        ['GBU-31 / GBU-32 JDAM', 2, '2003 only'],
    ])
    text += """
These are bounded, estimated integrations in the existing model. The three-Harpoon fit remains a fictional design requirement. No internal MER racks or stacked ammunition are added. Popeye, SLAM-ER and JSOW stay external; their shipped deployed-wing models and integration are not qualified for these internal stations. Larger Paveway/EO bombs stay external while smaller GBU-12s supplement precision fits.

## New bay mission presets

Each listed preset has a LongRange companion with two external fuel tanks. Offensive strike stores are internal; defensive IR missiles, tanks and the precision designation pod remain external. FleetInterceptBay also carries external BVR missiles.

"""
    text += table(['Preset', 'Internal stores', 'Editions'], [
        ['AntiShipBay', '3 Harpoons', 'All'], ['StrikeBay', '3 Mk 82', 'All'],
        ['StrikeHeavyBay', '2 Mk 84', 'All'], ['StrikePrecisionBay', '2 GBU-12', 'All'],
        ['FleetInterceptBay', '2 Phoenix', 'All'], ['JDAMBay', '2 GBU-32', '2003'],
        ['JDAMHeavyBay', '2 GBU-31', '2003'],
    ])
    text += '\n## Every loaded-bay fit and mass budget\n\n'
    rows = []
    for year in YEARS:
        for name, loadout in manifest[unit_id('fb', year)]['loadouts'].items():
            if loadout['internal_bay_stores']:
                rows.append([year, name, stores(loadout['internal_bay_stores']),
                             number(loadout['full_fuel_takeoff_mass_kg']), number(loadout['margin_kg'])])
    text += table(['Edition', 'Preset', 'Internal bay', 'Full-fuel takeoff kg', 'Reference margin kg'], rows)
    text += """
## Armed recovery test in Sea Power

1. Enable the refreshed V8 and required carrier/source mods, then restart. Use the 2003 MudPig on a stock catapult carrier first.
2. Select StrikeHeavyBay (two internal Mk 84s), launch, issue independent flight orders and return without firing. Check approach, bay doors, touchdown and deck recovery.
3. Repeat with AntiShipBay, FleetInterceptBay, StrikePrecisionBay and JDAMHeavyBay; then check the generated RAN carrier overrides.
4. Test weapon release separately. Check that doors open for release, close afterwards and do not interfere with landing gear.

All budgets include full internal fuel, every carried store, external tank fuel and gun ammunition. The 51,845 kg reference is a takeoff budget, not an arrestor/catapult or maximum carrier-landing limit. A real recovery assessment must account for fuel and the carrier's arresting limits. Static configuration checks cannot certify armed recovery or release clearance.

[Real RAAF upgrades](https://www.airforce.gov.au/sites/default/files/2023-07/F111%20A8-142.pdf) · [Every loadout](../COMPLETE_BREAKDOWN_V8.md)
"""
    text = text.replace('40/50/60/75', '/'.join(str(BAY_UPGRADE_MASS[year]) for year in YEARS))
    text = text.replace('Static configuration checks cannot certify armed recovery or release clearance.', 'Native collider/local-mesh envelopes are checked against the closed-door horizontal footprint for the additional weapon types. This coarse check does not establish three-dimensional packing or release clearance; the retained three-Harpoon fit remains a fictional requirement. Static configuration checks cannot certify armed recovery or release clearance.')
    (docs / 'INTERNAL_BAY_V8.md').write_text(text)
    combined = f"""# RAN F-111N Naval Wing V8 — Complete Breakdown

Version 8 internal-bay update, 2 October 2026. Four families in four editions: 16 aircraft, {total} selectable presets and 61 local store definitions. The 167-preset V6 baseline is expanded with {new_fits} new MudPig bay fits. Station geometry, concealment, door actions, original models and carrier/landing settings are retained. Targeting and estimated bay-upgrade mass are updated.

Use the release installer to refresh V8. Enable it with priority over carrier mods, keep required source assets enabled and restart. Select dated aircraft in carrier air groups; unsuffixed IDs are 1980. Armed recovery and release still require in-game testing.

"""
    for path in [docs / 'AIRCRAFT_COMPARISON.md', docs / 'INVESTMENT_PROGRAMME.md',
                 docs / 'INTERNAL_BAY_V8.md', ROOT / 'RELEASE_NOTES_V8.md', ROOT / 'COMPLETE_BREAKDOWN_V8.md']:
        content = path.read_text()
        if path.parent == ROOT:
            content = content.replace('(docs/', '(').replace('(HISTORICAL_REFERENCES.md)', '(../HISTORICAL_REFERENCES.md)')
        content = '\n'.join('#' + line if line.startswith('#') else line for line in content.splitlines())
        combined += content + '\n\n'
    (docs / 'V8-Complete-Breakdown.md').write_text(combined.rstrip() + '\n')
