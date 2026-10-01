#!/usr/bin/env python3
"""Repair the native ammunition language table and isolate zero-reload chaff."""
from copy import deepcopy
import json
from pathlib import Path
import re
from era_upgrade import ROOT, MOD, read_ini, write_ini

CHAFF_SYSTEM = "RAN_NW_AIR_CHAFF_DISP"


def apply(root=ROOT, mod=MOD):
    root, mod = Path(root), Path(mod)
    catalog = json.loads((root / "weapon_catalog.json").read_text())
    table = {}
    for path in sorted((mod / "ammunition").glob("*.ini")):
        unit = path.stem
        ammo = read_ini(path)
        general = ammo["General"]
        label = catalog[unit]["name"]
        if general["Type"] == "Missile":
            category = "AAM" if general.get("TargetType") == "AAW" else "AGM"
            if any(name in unit for name in ("standardarm", "shrike", "harma", "harmc")):
                category = "ARM"
        elif general["Type"] == "Bomb":
            category = "Bomb"
        elif "tank_600" in unit:
            category = "Fuel tank"
        else:
            category = "Pod"
        description = catalog[unit].get("simulation", label)
        # Native ammunition localisation is one flat table with four fields:
        # display name, optional nickname, category, description.
        table[unit] = ",".join((
            label.replace(",", ";"), "", category,
            description.replace(",", ";").replace("\n", " "),
        ))
    write_ini(mod / "language_en/ammunition_names.ini", {"AmmunitionNames": table})
    native = read_ini(root / "authoring/native/systems/weapons.ini")
    dispenser = deepcopy(native["WP_AIR_CHAFF_DISP"])
    dispenser["ReloadTime"] = "0"
    weapons_path = mod / "systems/weapons.ini"
    weapons = read_ini(weapons_path) if weapons_path.is_file() else {}
    weapons[CHAFF_SYSTEM] = dispenser
    write_ini(weapons_path, weapons)
    aircraft = 0
    for path in sorted((mod / "aircraft").glob("*.ini")):
        if path.name.endswith("_squadrons.ini"):
            continue
        data = read_ini(path)
        changed = False
        for section, values in data.items():
            if re.fullmatch(r"WeaponSystem\d+", section) and values.get("Type") == "Chaff":
                values["SystemName"] = CHAFF_SYSTEM
                changed = True
        if changed:
            write_ini(path, data)
            aircraft += 1
    print("Runtime fixes:", len(table), "native ammunition names;", aircraft, "aircraft with zero-reload chaff.")


if __name__ == "__main__":
    apply()
