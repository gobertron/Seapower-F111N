"""Estimated multistore qualification for the retained three-station MudPig bay.

These are hypothetical Naval Wing integrations, not historical F-111 approvals.
No extra stations, bomb racks, door geometry or landing overrides are introduced.
Large deployed-wing weapons (Popeye, SLAM-ER and JSOW) stay on the wings.
"""
BAY_UPGRADE_MASS = {1980: 40, 1985: 50, 1995: 60, 2003: 75}


def stations(store, count):
    if count not in (2, 3):
        raise ValueError("The bay uses two outer stations or all three existing stations")
    return {number: store for number in range(1, count + 1)}


def expand(d, year, ir, bvr, phoenix, ship, maverick, tank, load):
    """Supplement existing fits and add presets with offensive stores in the bay."""
    aid = lambda key: "ran_nw_" + key
    # One-store suspension adapters accommodate the native weapon origin and
    # collider length. Physical station coordinates and door geometry stay fixed.
    d['WeaponSystem3'].update(BayPhoenixPositions='0,0,-0.001', BayShrikePositions='0,0,-0.005')
    additions = {
        "Strike": (aid("mk82"), 3),
        "StrikeLongRange": (aid("mk82"), 3),
        "StrikeHeavy": (aid("mk84"), 2),
        "StrikeHeavyLongRange": (aid("mk84"), 2),
        "StrikeMedium": (aid("mk83"), 2),
        "StrikePrecision": (aid("gbu12"), 2),
        "StrikePrecisionLight": (aid("gbu12"), 2),
        "StrikePrecisionMedium": (aid("gbu12"), 2),
        "StrikePrecisionLongRange": (aid("gbu12"), 2),
        "MaverickStrike": (maverick, 2),
        "SEADShrike": (aid("shrike") + "|BayShrike", 2),
        "StrikePavewayIII": (aid("gbu12"), 2),
        "SLAMStrike": (aid("slam"), 2),
        "JDAMHeavy": (aid("gbu31"), 2),
        "JDAMMedium": (aid("gbu32"), 2),
    }
    for name, (store, count) in additions.items():
        if "WeaponSystem1" + name not in d:
            continue
        bay = d["WeaponSystem3" + name]
        bay.update({"Station" + str(n): value for n, value in stations(store, count).items()})

    defensive = {1: ir + "|AAM", 2: ir + "|AAM"}
    endurance = dict(defensive)
    endurance.update({3: tank + "|Tank", 4: tank + "|Tank"})
    for suffix, wing in (("", defensive), ("LongRange", endurance)):
        label_suffix = " (long range)" if suffix else ""
        load("AntiShipBay" + suffix, wing, stations(ship, 3),
             label="Internal-bay anti-ship strike" + label_suffix)
        load("StrikeBay" + suffix, wing, stations(aid("mk82"), 3),
             label="Internal-bay Mk 82 bombing" + label_suffix, mode="DumbBombs,Missiles")
        load("StrikeHeavyBay" + suffix, wing, stations(aid("mk84"), 2),
             label="Internal-bay Mk 84 heavy bombing" + label_suffix, mode="DumbBombs,Missiles")
        precision_wing = dict(wing)
        precision_wing[6] = "ran_nw_laserpod"
        load("StrikePrecisionBay" + suffix, precision_wing, stations(aid("gbu12"), 2),
             label="Internal-bay GBU-12 precision strike" + label_suffix, mode="GuidedBombs,Missiles")
        interceptor_wing = dict(wing)
        interceptor_wing.update({5: bvr + "|AAM", 6: bvr + "|AAM"})
        load("FleetInterceptBay" + suffix, interceptor_wing, stations(phoenix + "|BayPhoenix", 2),
             label="Fleet interception with internal Phoenix" + label_suffix)
        if year >= 2003:
            load("JDAMBay" + suffix, wing, stations(aid("gbu32"), 2),
                 label="Internal-bay GBU-32 JDAM strike" + label_suffix, mode="DumbBombs,Missiles")
            load("JDAMHeavyBay" + suffix, wing, stations(aid("gbu31"), 2),
                 label="Internal-bay GBU-31 JDAM heavy strike" + label_suffix, mode="DumbBombs,Missiles")

    # Both the original and new loaded-bay presets receive the dated readiness
    # programme. Native investment.apply updates these fields alongside the wing.
    for section, values in d.items():
        if section.startswith("WeaponSystem3") and section != "WeaponSystem3":
            if any(key.startswith("Station") for key in values):
                values.update(ReadyUpTime="30", CoolDownTime="60")


def qualification():
    return {
        "physical_stations": 3,
        "single_store_adapter_offsets_metres": {"Phoenix": [0, 0, -0.1], "Shrike": [0, 0, -0.5]},
        "upgrade_mass_kg_by_edition": BAY_UPGRADE_MASS,
        "status": "Estimated integration in the hypothetical Australian naval programme",
        "maximum_counts": {
            "Mk 82": 3, "Harpoon": 3, "Mk 83": 2, "Mk 84": 2,
            "GBU-12": 2, "Maverick": 2, "Shrike": 2, "Phoenix": 2,
            "SLAM": 2, "GBU-31": 2, "GBU-32": 2,
        },
        "excluded_internal_stores": ["Popeye", "SLAM-ER", "JSOW", "external MER racks", "fuel tanks", "control/ECM pods"],
        "carrier_recovery_runtime_tested": False,
        "carrier_arrestor_or_catapult_certified": False,
    }
