#!/usr/bin/env python3
"""Exercise the standalone replacement script against disposable game folders."""
import contextlib
import fcntl
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import types
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
script = (ROOT / "replace-f111n-with-v7.sh").read_text()
python = script.split("<<'V7_REPLACEMENT_PY'\n", 1)[1].rsplit("\nV7_REPLACEMENT_PY", 1)[0]
replacement = types.ModuleType("v7_replacement_test_module")
exec(compile(python, "replace-f111n-with-v7.sh", "exec"), replacement.__dict__)


def snapshot(folder):
    return {
        p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in folder.rglob("*") if p.is_file()
    }


def seed_old(folder, title):
    (folder / "aircraft").mkdir(parents=True)
    (folder / "_info.ini").write_text("[Language_en]\nName=" + title + "\n")
    (folder / "aircraft/ran_f-111n.ini").write_text("; old local aircraft\n")
    (folder / "stale-old-file.txt").write_text("Keep this complete old folder in the backup.")


class ReplacementTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="test-v7-replacement-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.game = self.root / "Steam library/steamapps/common/Sea Power"
        self.streaming = self.game / "Sea Power_Data/StreamingAssets"
        original = self.streaming / "original/vessels"
        original.mkdir(parents=True)
        # Match the user's reported 0xA0 error with a real carrier definition.
        self.carrier = original / "ran_cv_test.ini"
        data = (ROOT / "authoring/reference_carriers/usn_cvn_nimitz.ini").read_bytes()
        self.carrier.write_bytes(data + b"\n; Windows encoding: pilot\xa0notes\n")
        self.target = self.streaming / "user/RAN-F111N-Naval-Wing"
        seed_old(self.target, "RAN F-111N Naval Wing V6")
        self.alias = self.streaming / "RAN-RAAF-Series"
        seed_old(self.alias, "RAN / RAAF F-111N Series")
        self.mission = self.streaming / "user/missions/keep.ini"
        self.mission.parent.mkdir(parents=True)
        self.mission.write_text("Keep unrelated missions.")
        self.workshop = self.game.parents[1] / "workshop/content/1286220/3810606011"
        seed_old(self.workshop, "RAN / RAAF F-111N Series")
        self.output = io.StringIO()
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(replacement, "game_is_running", return_value=False).start()

    def install(self, package=ROOT, **kwargs):
        with contextlib.redirect_stdout(self.output):
            return replacement.install(package, self.game, **kwargs)

    def assert_old_unchanged(self, before):
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse(list(self.game.glob("ran-f111n-v7-stage-*")))

    def test_replaces_both_local_versions_and_keeps_full_backups(self):
        old = {p: snapshot(p) for p in (self.target, self.alias)}
        originals = snapshot(self.streaming / "original")
        workshop = snapshot(self.workshop)
        backup = self.install()
        self.assertIn("V7", (self.target / "_info.ini").read_text())
        self.assertFalse((self.target / "stale-old-file.txt").exists())
        self.assertFalse(self.alias.exists())
        for folder, files in old.items():
            self.assertEqual(snapshot(backup / folder.relative_to(self.streaming)), files)
        self.assertEqual(snapshot(self.streaming / "original"), originals)
        self.assertEqual(snapshot(self.workshop), workshop)
        self.assertEqual(self.mission.read_text(), "Keep unrelated missions.")
        self.assertEqual(json.loads((backup / "replacement.json").read_text())["status"], "installed")
        generated = (self.target / "vessels/ran_cv_test.ini").read_text()
        self.assertIn("pilot\u00a0notes", generated)
        self.assertTrue("AllowedType=Plane,VTOL" in generated)
        report = json.loads((self.target / "CARRIER_COMPATIBILITY.json").read_text())
        self.assertIn("ran_f-111n_2003", report["carriers"][0]["aircraft"])
        self.assertEqual(len(report["carriers"][0]["aircraft"]), 16)
        names = (self.target / "language_en/ammunition_names.ini").read_text()
        self.assertTrue("ran_nw_aim9l=AIM-9L Sidewinder,,AAM," in names)
        self.assertTrue("ReloadTime=0" in (self.target / "systems/weapons.ini").read_text())

    def test_dry_run_does_not_change_game_files_or_create_backup(self):
        before = snapshot(self.game)
        self.assertIsNone(self.install(dry_run=True))
        self.assertEqual(snapshot(self.game), before)
        self.assertFalse((self.game / "RAN-F111N-backups").exists())

    def test_swap_failure_restores_every_predecessor(self):
        before = snapshot(self.streaming)
        real_rename = Path.rename
        def fail_swap(path, target):
            if path.parent.name.startswith("ran-f111n-v7-stage-"):
                raise OSError("Simulated final rename failure")
            return real_rename(path, target)
        with mock.patch.object(Path, "rename", fail_swap):
            with self.assertRaisesRegex(RuntimeError, "previous local folders were restored"):
                self.install()
        self.assert_old_unchanged(before)
        report = next((self.game / "RAN-F111N-backups").glob("*/replacement.json"))
        self.assertEqual(json.loads(report.read_text())["status"], "rolled_back")

    def test_failure_before_moving_target_does_not_delete_it(self):
        before = snapshot(self.streaming)
        real_rename = Path.rename
        def fail_target_backup(path, target):
            if path == self.target:
                raise OSError("Simulated old-folder rename failure")
            return real_rename(path, target)
        with mock.patch.object(Path, "rename", fail_target_backup):
            with self.assertRaisesRegex(RuntimeError, "restored"):
                self.install()
        self.assert_old_unchanged(before)

    def test_post_swap_record_failure_restores_old_folders(self):
        before = snapshot(self.streaming)
        real_write = Path.write_text
        def fail_record(path, data, *args, **kwargs):
            if path.name == "replacement.json" and '"status": "installed"' in data:
                raise OSError("Simulated record-write failure")
            return real_write(path, data, *args, **kwargs)
        with mock.patch.object(Path, "write_text", fail_record):
            with self.assertRaisesRegex(RuntimeError, "restored"):
                self.install()
        self.assert_old_unchanged(before)

    def test_malformed_carrier_keeps_old_mod_intact(self):
        self.carrier.write_text(
            "[General]\nRole=Aircraft Carrier\n[FlightDeck]\n"
            "[RecoveryPoint1]\nAllowedType=Plane\n"
            "[LaunchPoint1]\nAllowedType=Plane\n"
        )
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "Carrier preparation failed"):
            self.install()
        self.assert_old_unchanged(before)

    def test_unrecognised_destination_is_not_overwritten(self):
        shutil.rmtree(self.target)
        self.target.mkdir()
        (self.target / "important.txt").write_text("Unrelated destination content.")
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "unrecognised"):
            self.install()
        self.assert_old_unchanged(before)

    def test_wrong_package_checksum_keeps_old_mod_intact(self):
        bad = self.root / "wrong-package"
        shutil.copytree(ROOT / "RAN-F111N-Naval-Wing", bad / "RAN-F111N-Naval-Wing")
        shutil.copy2(ROOT / "carrier_compatibility.py", bad)
        (bad / "MOD_SHA256.txt").write_text("wrong manifest")
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "manifest checksum"):
            self.install(bad)
        self.assert_old_unchanged(before)

    def test_damaged_asset_keeps_old_mod_intact(self):
        bad = self.root / "damaged-package"
        shutil.copytree(ROOT / "RAN-F111N-Naval-Wing", bad / "RAN-F111N-Naval-Wing")
        for name in ("carrier_compatibility.py", "MOD_SHA256.txt"):
            shutil.copy2(ROOT / name, bad)
        (bad / "RAN-F111N-Naval-Wing/_info.ini").write_text("damaged file")
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "game-file checksum failed"):
            self.install(bad)
        self.assert_old_unchanged(before)

    def test_running_game_stops_replacement(self):
        before = snapshot(self.streaming)
        with mock.patch.object(replacement, "game_is_running", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "Close Sea Power"):
                self.install()
        self.assert_old_unchanged(before)

    def test_parallel_installer_is_rejected(self):
        backup_parent = self.game / "RAN-F111N-backups"
        backup_parent.mkdir()
        before = snapshot(self.streaming)
        with (backup_parent / ".replacement.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(RuntimeError, "already running"):
                self.install()
        self.assert_old_unchanged(before)

    def test_old_zip_without_weapon_naming_fix_is_rejected(self):
        archive = ROOT.parents[2] / "deliverables/RAN-F111N-Naval-Wing-V7.zip"
        # Repository checkouts outside this workspace can run the other tests.
        if not archive.is_file():
            self.skipTest("Original standalone V7 ZIP is not present.")
        extracted = self.root / "legacy-zip"
        replacement.extract_archive(archive, extracted)
        package = replacement.package_root(extracted)
        self.assertEqual(replacement.digest(package / "carrier_compatibility.py"), replacement.LEGACY_CARRIER_SHA256)
        before = snapshot(package)
        game_before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, "not the corrected V7 release"):
            self.install(package)
        self.assert_old_unchanged(game_before)
        self.assertEqual(snapshot(package), before)


class DiscoveryAndInputTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="test-v7-input-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_finds_secondary_and_flatpak_libraries(self):
        home = self.root / "home"
        steam = home / ".local/share/Steam"
        secondary = self.root / "Secondary drive/SteamLibrary"
        flatpak = home / ".var/app/com.valvesoftware.Steam/.local/share/Steam"
        for root in (steam, secondary, flatpak):
            (root / "steamapps").mkdir(parents=True)
        (steam / "steamapps/libraryfolders.vdf").write_text(
            '"libraryfolders" { "1" { "path" "' + str(secondary) + '" } }'
        )
        secondary_game = secondary / "steamapps/common/Sea Power"
        flatpak_game = flatpak / "steamapps/common/Sea Power"
        for game in (secondary_game, flatpak_game):
            (game / "Sea Power_Data/StreamingAssets").mkdir(parents=True)
        (home / ".steam").mkdir()
        (home / ".steam/root").symlink_to(steam)
        self.assertEqual(replacement.discover_games(home), sorted((secondary_game, flatpak_game)))

    def test_rejects_zip_traversal_and_symlinks(self):
        for name in ("../outside.txt", "/outside.txt"):
            archive = self.root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr(name, "unsafe")
            with self.assertRaisesRegex(RuntimeError, "Unsafe archive"):
                replacement.extract_archive(archive, self.root / "extracted")
        archive = self.root / "symlink.zip"
        entry = zipfile.ZipInfo("package/link")
        entry.external_attr = (0o120777 << 16)
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr(entry, "../outside")
        with self.assertRaisesRegex(RuntimeError, "Unsafe archive"):
            replacement.extract_archive(archive, self.root / "extracted")

    def test_encoding_reader_handles_utf8_bom_utf16_and_windows(self):
        path = self.root / "encoding.ini"
        for encoding in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
            text = "; pilot\u00a0notes\n[General]\nRole=Aircraft Carrier\n"
            path.write_bytes(text.encode(encoding))
            self.assertEqual(replacement.read_source_text(path), text)
        path.write_bytes(b"; unknown byte \x81\n")
        self.assertIn("\x81", replacement.read_source_text(path))

    def test_package_path_argument_is_not_mistaken_for_running_game(self):
        proc = self.root / "proc"
        cmdline = proc / "123/cmdline"
        cmdline.parent.mkdir(parents=True)
        cmdline.write_bytes(b"python3\0-\0/full/path/Sea Power\0")
        real_path = Path
        with mock.patch.object(replacement, "Path", side_effect=lambda p: proc if p == "/proc" else real_path(p)):
            self.assertFalse(replacement.game_is_running())
            cmdline.write_bytes(b"wine64\0C:\\game\\Sea Power.exe\0")
            self.assertTrue(replacement.game_is_running())


if __name__ == "__main__":
    unittest.main(verbosity=2)
