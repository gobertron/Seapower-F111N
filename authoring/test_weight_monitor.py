#!/usr/bin/env python3
"""Meaningful failure/measurement checks for the optional Version 8 monitor."""
import base64
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("weight_v8", ROOT / "diagnostics/weight-v8/weight_check.py")
weight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weight)


def point(sample=1, mass=46595, fuel=14897, count=7):
    return {"sample": sample, "time": sample, "unit": "10:20", "aircraft": "ran_fb-111n_2003",
            "metric": {"aircraft.Motioncontroller.Mass": mass, "aircraft.FuelMass": fuel},
            "status": {"inventory_available": 1},
            "ammunition": {"ran_nw_harpoonl": count},
            "ammunition_parameter": {"ran_nw_harpoonl._mass": 526}}


class MeasurementTests(unittest.TestCase):
    def test_release_includes_fuel_consumed(self):
        event = weight.compare(point(), point(2, 46059, 14887, 6), {})
        self.assertEqual(event["status"], "observed_consistent")
        self.assertEqual(event["observations"][0]["weapon_loss_kg"], 526)

    def test_static_mass_does_not_pass(self):
        event = weight.compare(point(), point(2, 46595, 14887, 6), {})
        self.assertEqual(event["status"], "mismatch")

    def test_no_fuel_mass_is_unverified(self):
        before, after = point(), point(2, 46059, 14887, 6)
        for p in (before, after):
            p["metric"].pop("aircraft.FuelMass")
            p["metric"]["aircraft.RangeInKm"] = 2000
        self.assertEqual(weight.compare(before, after, {})["status"], "insufficient_data")

    def test_no_gross_mass_is_unverified(self):
        before, after = point(), point(2, 46059, 14887, 6)
        for p in (before, after):
            p["metric"] = {"aircraft._obp.Mass": 26975, "aircraft.FuelMass": 14897}
        self.assertEqual(weight.compare(before, after, {})["status"], "insufficient_data")

    def test_unknown_ammunition_does_not_count_as_zero_mass(self):
        before, after = point(), point(2, 46059, 14887, 6)
        for p in (before, after):
            p["ammunition_parameter"] = {}
        self.assertEqual(weight.compare(before, after, {})["status"], "insufficient_data")

    def test_catalogue_fallback(self):
        before, after = point(), point(2, 46059, 14887, 6)
        for p in (before, after):
            p["ammunition_parameter"] = {}
        self.assertEqual(weight.compare(before, after, {"ran_nw_harpoonl": {"mass_kg": 526}})["status"], "observed_consistent")

    def test_live_store_override_takes_precedence(self):
        before, after = point(), point(2, 45985, 14887, 6)
        for p in (before, after):
            p["ammunition_parameter"]["ran_nw_harpoonl._mass"] = 600
        self.assertEqual(weight.compare(before, after, {"ran_nw_harpoonl": {"mass_kg": 526}})["status"], "observed_consistent")

    def test_inconsistent_live_store_mass_is_unverified(self):
        before, after = point(), point(2, 45985, 14887, 6)
        after["ammunition_parameter"]["ran_nw_harpoonl._mass"] = 600
        self.assertEqual(weight.compare(before, after, {})["status"], "insufficient_data")

    def test_fuel_only_evidence_does_not_prove_release(self):
        result = weight.analyse({("10:20", "ran_fb-111n_2003"): [point(), point(2, 46575, 14877, 7)]}, {})
        self.assertTrue(result["fuel_burn_observed"])
        self.assertFalse(result["release_observed"])

    def test_rearming_ignored(self):
        self.assertIsNone(weight.compare(point(count=6), point(2, count=7), {}))

    def test_refuelling_not_release_evidence(self):
        self.assertEqual(weight.compare(point(), point(2, 46069, 14997, 6), {})["status"], "insufficient_data")

    def test_no_change_is_not_evidence(self):
        self.assertIsNone(weight.compare(point(), point(2), {}))

    def test_small_fuel_burns_accumulate(self):
        points = [point(i + 1, 46595 - i, 14897 - i) for i in range(31)]
        result = weight.analyse({("10:20", "ran_fb-111n_2003"): points}, {})
        self.assertTrue(result["fuel_burn_observed"])
        self.assertFalse(result["release_observed"])

    def test_unavailable_inventory_cannot_pass(self):
        before, after = point(), point(2, 46059, 14887, 6)
        after["status"] = {"inventory_available": 0}
        self.assertEqual(weight.compare(before, after, {})["status"], "insufficient_data")

    def test_missing_and_truncated_rows_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weight.csv"
            path.write_text("sample,realtime_s,unit_key,aircraft_id,kind,name,value\n1,1,10:20,ran_fb-111n_2003,metric,aircraft.Mass,46595\n2,2,10:20,ran_fb-111n_2003,metric,aircraft.Mass,")
            result = weight.load_recording(path)
            self.assertEqual(len(result[("10:20", "ran_fb-111n_2003")]), 1)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name) / "Steam library/Sea Power"
        (self.game / "Sea Power_Data/StreamingAssets/original").mkdir(parents=True)
        (self.game / "Sea Power_Data/StreamingAssets/original/keep.ini").write_text("Original aircraft")
        (self.game / "BepInEx/core").mkdir(parents=True)
        (self.game / "BepInEx/core/BepInEx.dll").write_bytes(b"existing preloader")
        (self.game / "BepInEx/plugins").mkdir()
        (self.game / "BepInEx/plugins/other.dll").write_bytes(b"other mod")
        self.payload = b"MZ engine-free installer test payload"
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(weight, "game_running", return_value=False).start()
        mock.patch.object(weight, "PLUGIN_BASE64", base64.b64encode(self.payload).decode()).start()
        mock.patch.object(weight, "PLUGIN_SHA256", hashlib.sha256(self.payload).hexdigest()).start()

    def run_install(self, remove=False):
        with contextlib.redirect_stdout(io.StringIO()):
            weight.install(self.game, remove)

    def test_install_reinstall_remove_preserves_game_and_other_mods(self):
        self.run_install()
        target = self.game / "BepInEx/plugins" / weight.FOLDER
        self.assertEqual((target / weight.DLL).read_bytes(), self.payload)
        self.run_install()
        self.run_install(remove=True)
        self.assertFalse(target.exists())
        self.assertEqual((self.game / "Sea Power_Data/StreamingAssets/original/keep.ini").read_text(), "Original aircraft")
        self.assertEqual((self.game / "BepInEx/plugins/other.dll").read_bytes(), b"other mod")

    def test_running_game_blocks_mutations(self):
        with mock.patch.object(weight, "game_running", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "Close Sea Power"):
                self.run_install()

    def test_missing_preloader_does_not_install(self):
        (self.game / "BepInEx/core/BepInEx.dll").unlink()
        with self.assertRaisesRegex(RuntimeError, "preloader"):
            self.run_install()

    def test_bad_payload_does_not_replace_existing_plugin(self):
        self.run_install()
        with mock.patch.object(weight, "PLUGIN_SHA256", "bad"):
            with self.assertRaisesRegex(RuntimeError, "checksum"):
                self.run_install()
        self.assertEqual((self.game / "BepInEx/plugins" / weight.FOLDER / weight.DLL).read_bytes(), self.payload)

    def test_unrecognised_folder_not_deleted(self):
        target = self.game / "BepInEx/plugins" / weight.FOLDER
        target.mkdir()
        (target / "keep.txt").write_text("keep")
        with self.assertRaisesRegex(RuntimeError, "unrecognised"):
            self.run_install(remove=True)
        self.assertTrue((target / "keep.txt").is_file())

    def test_symlink_not_followed(self):
        target = self.game / "BepInEx/plugins" / weight.FOLDER
        target.symlink_to(self.game / "Sea Power_Data/StreamingAssets/original", target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.run_install()

    def test_no_runtime_samples_does_not_claim_pass(self):
        with self.assertRaisesRegex(RuntimeError, "No aircraft samples"):
            weight.report(self.game)

    def test_install_failure_restores_previous_monitor(self):
        self.run_install()
        original_rename = Path.rename
        target = self.game / "BepInEx/plugins" / weight.FOLDER / weight.DLL
        def rename(path, destination):
            if path.name == weight.DLL and path.parent.name.startswith("weight-v8-stage-"):
                raise OSError("Simulated write failure")
            return original_rename(path, destination)
        with mock.patch.object(Path, "rename", rename):
            with self.assertRaisesRegex(OSError, "Simulated"):
                self.run_install()
        self.assertEqual(target.read_bytes(), self.payload)

    def test_recording_report_and_collector(self):
        folder = self.game / "RAN-F111N-weight-V8"
        folder.mkdir()
        recording = folder / "weight-v8-test.csv"
        with recording.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["sample", "realtime_s", "unit_key", "aircraft_id", "kind", "name", "value"])
            for p in [point(), point(2, 46059, 14887, 6), point(3, 46039, 14867, 6)]:
                for kind in ("metric", "ammunition", "ammunition_parameter", "status"):
                    for name, value in p[kind].items():
                        writer.writerow([p["sample"], p["time"], p["unit"], p["aircraft"], kind, name, value])
        with contextlib.redirect_stdout(io.StringIO()):
            result = weight.report(self.game, collect=True)
        self.assertTrue(result["release_observed"])
        self.assertTrue(result["fuel_burn_observed"])
        import zipfile
        with zipfile.ZipFile(folder / "weight-results-v8.zip") as archive:
            self.assertEqual(set(archive.namelist()), {recording.name, "weight-report-v8.txt", "weight-report-v8.json"})


if __name__ == "__main__":
    unittest.main()
