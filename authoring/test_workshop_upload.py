#!/usr/bin/env python3
"""Exercise replacement, publication preparation and the SteamCMD boundary."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

from authoring.test_v8_replacement import ROOT, replacement, seed_old, snapshot


class WorkshopTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="test-v8-workshop-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.game = self.root / "Steam library/steamapps/common/Sea Power"
        self.streaming = self.game / "Sea Power_Data/StreamingAssets"
        original = self.streaming / "original/vessels"
        original.mkdir(parents=True)
        shutil.copy2(ROOT / "authoring/reference_carriers/usn_cvn_nimitz.ini", original)
        self.target = self.streaming / "user/RAN-F111N-Naval-Wing"
        seed_old(self.target, "RAN / RAAF F-111N Series")
        self.output = io.StringIO()
        self.patch = mock.patch.object(replacement, "game_is_running", return_value=False)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def install(self, **kwargs):
        with contextlib.redirect_stdout(self.output):
            backup = replacement.install(ROOT, self.game, prepare_upload=True, **kwargs)
        if backup is None:
            return None
        self.backup = backup
        self.bundle = Path(json.loads((backup / "replacement.json").read_text())["workshop_bundle"])
        return self.bundle

    def emulator(self, output, code=0):
        executable = self.root / "SteamCMD folder/fake-steamcmd"
        executable.parent.mkdir(exist_ok=True)
        self.arguments = self.root / "steamcmd-arguments.json"
        executable.write_text(
            "#!/usr/bin/env python3\nimport json,sys\nfrom pathlib import Path\n"
            + "Path(" + repr(str(self.arguments)) + ").write_text(json.dumps(sys.argv[1:]))\n"
            + "print(" + repr(output) + ", flush=True)\nraise SystemExit(" + str(code) + ")\n"
        )
        executable.chmod(0o755)
        return executable

    def test_complete_payload_is_flat_and_matches_the_installed_mod(self):
        old = snapshot(self.target)
        sources = snapshot(self.streaming / "original")
        bundle = self.install()
        self.assertEqual(snapshot(bundle / "content"), snapshot(self.target))
        self.assertTrue((bundle / "content/_info.ini").is_file())
        self.assertFalse((bundle / "content/RAN-F111N-Naval-Wing").exists())
        self.assertFalse((bundle / "content/replace-f111n-with-v8.sh").exists())
        self.assertEqual(snapshot(self.backup / "user/RAN-F111N-Naval-Wing"), old)
        self.assertEqual(snapshot(self.streaming / "original"), sources)
        self.assertEqual((bundle / "preview.png").read_bytes(), (self.target / "preview.png").read_bytes())
        self.assertIn("[AmmunitionNames]", (bundle / "content/language_en/ammunition_names.ini").read_text())
        self.assertIn("ReloadTime=0", (bundle / "content/systems/weapons.ini").read_text())
        self.assertNotIn(str(self.root), (bundle / "content/CARRIER_COMPATIBILITY.json").read_text())
        self.assertIn(str(self.root), (bundle / "carrier-report.local.json").read_text())
        vdf = (bundle / "upload.vdf").read_text()
        self.assertIn('"appid" "1286220"', vdf)
        self.assertIn('"publishedfileid" "3810606011"', vdf)
        self.assertNotIn('"visibility"', vdf)
        self.assertIn('"title" "RAN F-111N Naval Wing V8"', vdf)
        self.assertIn('"description" "[h1]RAN F-111N Naval Wing — V8[/h1]', vdf)
        self.assertEqual(json.loads((bundle / "workshop-sha256.json").read_text())["version"], "V8")
        self.assertEqual(replacement.verify_workshop_bundle(bundle), bundle)

    def test_dry_run_prepares_and_checks_without_writing_to_game(self):
        before = snapshot(self.game)
        self.assertIsNone(self.install(dry_run=True))
        self.assertEqual(snapshot(self.game), before)
        self.assertFalse((self.game / "RAN-F111N-workshop").exists())
        self.assertFalse((self.game / "RAN-F111N-backups").exists())

    def test_invalid_preview_stops_before_replacement(self):
        before = snapshot(self.streaming)
        with mock.patch.dict(replacement.WORKSHOP_ASSETS, {"RAN-F111N-preview.png": "0" * 64}):
            with self.assertRaisesRegex(RuntimeError, "Workshop asset checksum"):
                self.install()
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse((self.game / "RAN-F111N-backups").exists())

    def test_preparation_failure_preserves_old_mod(self):
        before = snapshot(self.streaming)
        with mock.patch.object(replacement, "prepare_workshop", side_effect=OSError("Simulated copy failure")):
            with self.assertRaisesRegex(OSError, "copy failure"):
                self.install()
        self.assertEqual(snapshot(self.streaming), before)

    def test_workshop_swap_failure_restores_old_mod(self):
        before = snapshot(self.streaming)
        rename = Path.rename
        def fail_bundle(path, destination):
            if path.name == "workshop" and path.parent.name.startswith("ran-f111n-v8-stage-"):
                raise OSError("Simulated Workshop rename failure")
            return rename(path, destination)
        with mock.patch.object(Path, "rename", fail_bundle):
            with self.assertRaisesRegex(RuntimeError, "previous local folders were restored"):
                self.install()
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse(list((self.game / "RAN-F111N-workshop").rglob("upload.vdf")))

    def test_post_swap_failure_restores_mod_and_removes_new_payload(self):
        before = snapshot(self.streaming)
        write = Path.write_text
        def fail_record(path, data, *args, **kwargs):
            if path.name == "replacement.json" and '"status": "installed"' in data:
                raise OSError("Simulated completed-record failure")
            return write(path, data, *args, **kwargs)
        with mock.patch.object(Path, "write_text", fail_record):
            with self.assertRaisesRegex(RuntimeError, "restored"):
                self.install()
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse(list((self.game / "RAN-F111N-workshop").rglob("upload.vdf")))

    def test_success_is_confirmed_for_the_requested_existing_id(self):
        bundle = self.install()
        executable = self.emulator("Success. Published item 3810606011.")
        with contextlib.redirect_stdout(self.output):
            replacement.upload_workshop(bundle, "steam_owner", executable)
        args = json.loads(self.arguments.read_text())
        self.assertEqual(args[:3], ["+login", "steam_owner", "+workshop_build_item"])
        self.assertEqual(args[3], '"' + str(bundle / "upload.vdf") + '"')
        self.assertEqual(args[4], "+quit")
        self.assertIn("STEAM WORKSHOP UPDATED", self.output.getvalue())

    def test_zero_exit_without_success_is_reported_as_a_failure(self):
        bundle = self.install()
        before = snapshot(bundle)
        executable = self.emulator("ERROR! Failed to update Workshop item (Access Denied).")
        with contextlib.redirect_stdout(self.output):
            with self.assertRaisesRegex(RuntimeError, "did not confirm"):
                replacement.upload_workshop(bundle, "steam_owner", executable)
        self.assertEqual(snapshot(bundle), before)
        self.assertTrue((self.target / "aircraft/ran_f-111n_2003.ini").is_file())

    def test_success_for_a_different_item_is_rejected(self):
        bundle = self.install()
        executable = self.emulator("Success. Published item 1234567890.")
        with contextlib.redirect_stdout(self.output):
            with self.assertRaisesRegex(RuntimeError, "did not confirm"):
                replacement.upload_workshop(bundle, "steam_owner", executable)

    def test_payload_changes_block_upload_before_launching_steamcmd(self):
        bundle = self.install()
        (bundle / "content/aircraft/ran_f-111n.ini").write_text("broken aircraft")
        with mock.patch.object(replacement.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "checksum failed"):
                replacement.upload_workshop(bundle, "steam_owner", "/usr/bin/true")
            launch.assert_not_called()

    def test_extra_files_block_upload(self):
        bundle = self.install()
        (bundle / "content/unexpected-personal-file.txt").write_text("not part of the mod")
        with self.assertRaisesRegex(RuntimeError, "content has changed"):
            replacement.verify_workshop_bundle(bundle)

    def test_modified_destination_is_rejected_even_with_a_new_checksum(self):
        bundle = self.install()
        vdf = bundle / "upload.vdf"
        vdf.write_text(vdf.read_text().replace('"3810606011"', '"0"'))
        marker = bundle / "workshop-sha256.json"
        manifest = json.loads(marker.read_text())
        manifest["files"]["upload.vdf"] = replacement.digest(vdf)
        marker.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(RuntimeError, "configuration was changed"):
            replacement.verify_workshop_bundle(bundle)

    def test_invalid_username_never_reaches_steamcmd(self):
        bundle = self.install()
        with mock.patch.object(replacement.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "Invalid Steam account"):
                replacement.upload_workshop(bundle, "owner +quit", "/usr/bin/true")
            launch.assert_not_called()

    def test_missing_steamcmd_leaves_prepared_payload_available(self):
        bundle = self.install()
        before = snapshot(bundle)
        with self.assertRaisesRegex(RuntimeError, "executable was not found"):
            replacement.upload_workshop(bundle, "steam_owner", self.root / "missing-steamcmd")
        self.assertEqual(snapshot(bundle), before)

    def test_upload_prepared_does_not_download_or_replace_again(self):
        bundle = self.install()
        executable = self.emulator("Success. Published item 3810606011.")
        before = snapshot(self.game)
        with mock.patch.object(replacement.os, "geteuid", return_value=1000), \
             mock.patch.object(replacement, "fetch_archive") as download, \
             mock.patch.object(replacement, "install") as install, \
             contextlib.redirect_stdout(self.output):
            result = replacement.main(["--upload-prepared", str(bundle), "--steam-user", "steam_owner", "--steamcmd", str(executable)])
        self.assertEqual(result, 0)
        download.assert_not_called()
        install.assert_not_called()
        self.assertEqual(snapshot(self.game), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
