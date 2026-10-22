#!/usr/bin/env python3
"""Version 8: install/remove a read-only monitor and interpret its observations.

The generated standalone shell wrapper embeds the compiled original plugin and
the release's store catalogue. No game, Unity or BepInEx assembly is distributed.
"""
import argparse
import base64
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

PLUGIN_BASE64 = ""  # populated by authoring/build_weight_monitor.py
PLUGIN_SHA256 = ""
CATALOG = {}
GUID = "com.gobertron.f111n.weight.v8"
FOLDER = "RANF111NWeightMonitorV8"
DLL = "RANF111NWeightMonitorV8.dll"
MASS_NAMES = {"mass", "totalmass", "currentmass", "grossmass", "aircraftmass", "weight", "totalweight", "currentweight"}
FUEL_NAMES = {"fuelmass", "currentfuelmass", "remainingfuelmass", "fuelweight", "currentfuelweight"}


def normal(name):
    return re.sub(r"[^a-z]", "", name.rsplit(".", 1)[-1].lower())


def game_running():
    for process in Path("/proc").glob("[0-9]*/comm"):
        try:
            if process.read_text().strip().lower() in {"sea power.exe", "seapower.exe", "sea power", "seapower"}:
                return True
        except (OSError, UnicodeError):
            pass
    return False


def check_game(game):
    if not (game / "Sea Power_Data/StreamingAssets").is_dir():
        raise RuntimeError("This is not a Sea Power folder: " + str(game))


def install(game, remove=False):
    check_game(game)
    if game_running():
        raise RuntimeError("Close Sea Power before installing or removing the monitor.")
    parent = game / "BepInEx/plugins"
    destination = parent / FOLDER
    for path in (game / "BepInEx", parent, destination):
        if path.is_symlink():
            raise RuntimeError("Refusing a symlink in the monitor installation path: " + str(path))
    marker = destination / "monitor-v8.json"
    if destination.exists():
        try:
            data = json.loads(marker.read_text())
        except (OSError, ValueError):
            raise RuntimeError("The monitor destination has unrecognised files; nothing was replaced.")
        if data.get("plugin_guid") != GUID:
            raise RuntimeError("The monitor destination belongs to another plugin; nothing was replaced.")
    if remove:
        if destination.exists():
            shutil.rmtree(destination)
        print("[100%] Version 8 weight monitor removed. Recordings have been kept.")
        return
    if not (game / "BepInEx/core/BepInEx.dll").is_file():
        raise RuntimeError("The existing Anchor Chain/BepInEx preloader was not found. Install it before this optional monitor.")
    print("[20%] Sea Power and the existing BepInEx installation found.")
    payload = base64.b64decode(PLUGIN_BASE64, validate=True)
    if not payload or hashlib.sha256(payload).hexdigest() != PLUGIN_SHA256:
        raise RuntimeError("Embedded Version 8 monitor checksum failed.")
    print("[50%] Version 8 monitor checksum verified.")
    parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="weight-v8-stage-", dir=parent))
    old = stage / "previous"
    try:
        (stage / DLL).write_bytes(payload)
        (stage / "monitor-v8.json").write_text(json.dumps({"version": "Version 8", "plugin_guid": GUID, "sha256": PLUGIN_SHA256}, indent=2) + "\n")
        if destination.exists():
            destination.rename(old)
        try:
            destination.mkdir()
            for name in (DLL, "monitor-v8.json"):
                (stage / name).rename(destination / name)
        except BaseException:
            if destination.exists():
                shutil.rmtree(destination)
            if old.exists():
                old.rename(destination)
            raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    print("[100%] Version 8 weight monitor installed: " + str(destination))
    print("Start Sea Power and use a Naval Wing aircraft. The monitor only records state.")
    print("Use MudPig AntiShipHeavy, let it fly for 30 seconds, fire Harpoons, then fly for another minute.")
    print("Close the game, then run this script again with --collect to make the report.")


def load_recording(path):
    snapshots = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["sample", "realtime_s", "unit_key", "aircraft_id", "kind", "name", "value"]:
            raise ValueError("Unrecognised Version 8 recording format")
        for row in reader:
            # A recording may still be open in game. Ignore an unfinished last row.
            try:
                value = float(row["value"])
                sample, realtime = int(row["sample"]), float(row["realtime_s"])
                if not math.isfinite(value) or not math.isfinite(realtime):
                    continue
                key = row["unit_key"], row["aircraft_id"], sample
                snapshot = snapshots.setdefault(key, {"sample": sample, "time": realtime, "unit": key[0], "aircraft": key[1], "metric": {}, "ammunition": {}, "ammunition_parameter": {}, "status": {}})
                if row["kind"] in {"metric", "ammunition", "ammunition_parameter", "status"} and row["name"]:
                    snapshot[row["kind"]][row["name"]] = value
            except (ValueError, TypeError, KeyError):
                continue
    units = {}
    for (_, _, _), snapshot in snapshots.items():
        units.setdefault((snapshot["unit"], snapshot["aircraft"]), []).append(snapshot)
    for values in units.values():
        values.sort(key=lambda s: s["sample"])
    return units


def mass_for(ammunition, first, second, catalog):
    """Prefer the live ammunition parameter; reject disagreeing mass candidates."""
    live = []
    for point in (first, second):
        for path, value in point["ammunition_parameter"].items():
            if path.startswith(ammunition + ".") and normal(path) == "mass" and value > 0:
                live.append(value)
    if live:
        return live[0] if max(live) - min(live) <= .01 else None
    data = catalog.get(ammunition)
    return data["mass_kg"] if data else None


def compare(first, second, catalog):
    if first.get("status", {}).get("inventory_available") != 1 or second.get("status", {}).get("inventory_available") != 1:
        return {"kind": "inventory", "status": "insufficient_data", "reason": "Live inventory was not available in both samples."}
    ammo_delta = {name: first["ammunition"].get(name, 0) - second["ammunition"].get(name, 0)
                  for name in first["ammunition"].keys() | second["ammunition"].keys()}
    changes = {name: count for name, count in ammo_delta.items() if count}
    # Rearming, loadout swaps and pooled respawns are not weapon-release tests.
    if any(count < 0 for count in changes.values()):
        return None
    expected = 0.0
    for name, count in changes.items():
        mass = mass_for(name, first, second, catalog)
        if mass is None:
            return {"kind": "release", "status": "insufficient_data", "reason": "Missing live/catalogued mass for " + name, "released": changes}
        expected += count * mass
    metrics = first["metric"].keys() & second["metric"].keys()
    candidates = [name for name in metrics if normal(name) in MASS_NAMES and first["metric"][name] >= 5000
                  and not any(part in name.lower() for part in ("parameters", "._obp", "._ap", "._fp"))]
    fuels = [name for name in metrics if normal(name) in FUEL_NAMES]
    kind = "release" if changes else "fuel"
    if not changes and not any(first["metric"][f] - second["metric"][f] >= 10 for f in fuels):
        return None
    observations = []
    for name in sorted(candidates):
        actual = first["metric"][name] - second["metric"][name]
        for fuel in sorted(fuels):
            fuel_loss = first["metric"][fuel] - second["metric"][fuel]
            if fuel_loss < -.1:  # refuelling is a separate test
                continue
            predicted = expected + fuel_loss
            # Constant values can never count as evidence of an update.
            matches = predicted > 2 and actual > 0 and abs(actual - predicted) <= 2
            observations.append({"mass_field": name, "fuel_field": fuel, "observed_loss_kg": round(actual, 3),
                                 "weapon_loss_kg": round(expected, 3), "fuel_loss_kg": round(fuel_loss, 3),
                                 "difference_kg": round(actual - predicted, 3), "consistent": matches})
    if not observations:
        return {"kind": kind, "status": "insufficient_data", "released": changes,
                "reason": "No usable live gross-mass/fuel-mass pair was exposed; raw fields are retained."}
    return {"kind": kind, "status": "observed_consistent" if any(o["consistent"] for o in observations) else "mismatch",
            "released": changes, "observations": observations}


def analyse(units, catalog):
    result = {"version": "Version 8", "runtime_tested_here": False, "units": [], "scope": "Observed game fields and inventory; this is not flight-performance or carrier certification."}
    for (key, aircraft), points in sorted(units.items()):
        events = []
        fuel_anchor = points[0]
        for previous, second in zip(points, points[1:]):
            changed = previous["ammunition"] != second["ammunition"]
            event = compare(previous if changed else fuel_anchor, second, catalog)
            if event is not None:
                event["sample"] = second["sample"]
                events.append(event)
            # Accumulate small per-second burns until a useful fuel-only delta
            # exists; reset at releases, rearming or a completed observation.
            if changed or event is not None:
                fuel_anchor = second
        result["units"].append({"unit_key": key, "aircraft": aircraft, "samples": len(points),
                                "metric_fields": sorted({name for p in points for name in p["metric"]}), "events": events})
    result["release_observed"] = any(e["kind"] == "release" and e["status"] == "observed_consistent" for u in result["units"] for e in u["events"])
    result["fuel_burn_observed"] = any(e["kind"] == "fuel" and e["status"] == "observed_consistent" for u in result["units"] for e in u["events"])
    return result


def report(game, collect=False):
    check_game(game)
    folder = game / "RAN-F111N-weight-V8"
    recordings = sorted(folder.glob("weight-v8-*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    for path in recordings:
        units = load_recording(path)
        if units:
            break
    else:
        raise RuntimeError("No aircraft samples yet. Start a mission with V8 aircraft, then use --collect after the test. Check BepInEx/LogOutput.log for 'Weight Monitor' if no recording appears.")
    result = analyse(units, CATALOG)
    result["recording"] = path.name
    lines = ["RAN F-111N — Version 8 weight report", "Recording: " + path.name,
             "Weapon release: " + ("observed mass change consistent with released weapons and fuel burn" if result["release_observed"] else "NOT VERIFIED"),
             "Fuel burn: " + ("observed mass change consistent with fuel consumption" if result["fuel_burn_observed"] else "NOT VERIFIED")]
    for unit in result["units"]:
        lines.append(f"\n{unit['aircraft']} ({unit['samples']} samples)")
        for kind in ("release", "fuel", "inventory"):
            events = [e for e in unit["events"] if e["kind"] == kind]
            for status in ("observed_consistent", "mismatch", "insufficient_data"):
                selected = [e for e in events if e["status"] == status]
                if selected:
                    lines.append(f"  {kind}: {len(selected)} {status}")
                    example = selected[0]
                    lines.append("  " + json.dumps(example, sort_keys=True))
    lines += ["", "Raw mass/fuel fields remain in the CSV. Unknown field layouts are reported as unverified.",
              "The monitor never changes aircraft, weapons, fuel, thrust, AI orders or game assemblies."]
    text = "\n".join(lines) + "\n"
    (folder / "weight-report-v8.txt").write_text(text)
    (folder / "weight-report-v8.json").write_text(json.dumps(result, indent=2) + "\n")
    print(text)
    if collect:
        bundle = folder / "weight-results-v8.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
            for source in (path, folder / "weight-report-v8.txt", folder / "weight-report-v8.json"):
                archive.write(source, source.name)
        print("Results ready to share: " + str(bundle))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Version 8 read-only in-game weight monitor")
    parser.add_argument("game", nargs="?", default=str(Path.home() / ".local/share/Steam/steamapps/common/Sea Power"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--remove", action="store_true")
    mode.add_argument("--report", action="store_true")
    mode.add_argument("--collect", action="store_true")
    args = parser.parse_args(argv)
    game = Path(args.game).expanduser().resolve()
    if args.report or args.collect:
        report(game, args.collect)
    else:
        install(game, args.remove)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print("Version 8 weight check stopped: " + str(error), file=sys.stderr)
        sys.exit(1)
