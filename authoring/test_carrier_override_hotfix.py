#!/usr/bin/env python3
"""Test carrier-override rollback in isolated disposable game directories."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("carrier_hotfix", ROOT / "fix-f111n-v9-carrier-overrides.py")
hotfix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotfix)


def files_at(path):
    return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob("*") if p.is_file()}


class CarrierHotfixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.game = Path(self.tmp.name) / "Sea Power"
        self.streaming = self.game / "Sea Power_Data/StreamingAssets"
        (self.streaming / "original/vessels").mkdir(parents=True)
        (self.streaming / "original/vessels/usn_cvn_enterprise.ini").write_text("original carrier")
        self.mod = self.streaming / hotfix.MOD_NAME
        (self.mod / "aircraft").mkdir(parents=True)
        (self.mod / "_info.ini").write_text("[Language_en]\nName=RAN F-111N Naval Wing V9.0 - 1980 / 1985 / 1995 / 2003\n")
        for family in ("f", "fb", "rf", "ef"):
            for edition in ("", "_1985", "_1995", "_2003"):
                (self.mod / "aircraft" / f"ran_{family}-111n{edition}.ini").write_text("aircraft")
        (self.mod / "vessels").mkdir()
        (self.mod / "vessels/usn_cvn_enterprise.ini").write_text("conflicting generated override")
        (self.mod / "vessels/ran_cv_custom.ini").write_text("custom generated override")
        (self.streaming / "RAN-Carrier-Australis-2030/vessels").mkdir(parents=True)
        (self.streaming / "RAN-Carrier-Australis-2030/vessels/ran_cv_custom.ini").write_text("source custom carrier")
        self.running = mock.patch.object(hotfix, "game_is_running", return_value=False)
        self.running.start()
        self.addCleanup(self.running.stop)

    def test_backup_preserves_only_override_and_keeps_carriers_and_aircraft(self):
        prior = files_at(self.mod / "vessels")
        aircraft = files_at(self.mod / "aircraft")
        original = files_at(self.streaming / "original")
        other = files_at(self.streaming / "RAN-Carrier-Australis-2030")
        backup = hotfix.install(self.streaming)
        self.assertFalse((self.mod / "vessels").exists())
        self.assertEqual(files_at(backup / "vessels"), prior)
        self.assertEqual(files_at(self.mod / "aircraft"), aircraft)
        self.assertEqual(files_at(self.streaming / "original"), original)
        self.assertEqual(files_at(self.streaming / "RAN-Carrier-Australis-2030"), other)
        self.assertIsNone(hotfix.install(self.game))
        self.assertEqual(files_at(backup / "vessels"), prior)

    def test_wrong_mod_identity_is_not_changed(self):
        (self.mod / "_info.ini").write_text("[Language_en]\nName=Other Mod\n")
        before = files_at(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "not the expected"):
            hotfix.install(self.streaming)
        self.assertEqual(files_at(self.streaming), before)

    def test_open_game_is_not_changed(self):
        before = files_at(self.streaming)
        with mock.patch.object(hotfix, "game_is_running", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "Close Sea Power"):
                hotfix.install(self.streaming)
        self.assertEqual(files_at(self.streaming), before)

    def test_symlinked_vessel_directory_is_not_changed(self):
        import shutil
        shutil.rmtree(self.mod / "vessels")
        source = self.streaming / "RAN-Carrier-Australis-2030/vessels"
        (self.mod / "vessels").symlink_to(source, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            hotfix.install(self.streaming)
        self.assertTrue((source / "ran_cv_custom.ini").is_file())

    def test_failed_move_keeps_existing_overrides(self):
        before = files_at(self.mod / "vessels")
        with mock.patch.object(Path, "rename", side_effect=OSError("simulated failure")):
            with self.assertRaisesRegex(OSError, "simulated failure"):
                hotfix.install(self.streaming)
        self.assertEqual(files_at(self.mod / "vessels"), before)

    def test_interruption_after_move_restores_existing_overrides(self):
        before = files_at(self.mod / "vessels")
        original = Path.rename
        def interrupt_after_move(path, target):
            result = original(path, target)
            if path == self.mod / "vessels":
                raise KeyboardInterrupt()
            return result
        with mock.patch.object(Path, "rename", interrupt_after_move):
            with self.assertRaises(KeyboardInterrupt):
                hotfix.install(self.streaming)
        self.assertEqual(files_at(self.mod / "vessels"), before)


if __name__ == "__main__":
    unittest.main()
