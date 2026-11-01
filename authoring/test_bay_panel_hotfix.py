#!/usr/bin/env python3
"""Exercise user-facing bay repair with the actual source model and 12 INIs."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bay_hotfix', ROOT / 'fix-f111n-v9-bay-panels.py')
hotfix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotfix)


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file() and not p.is_symlink()}


class BayPanelHotfixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.game = Path(self.tmp.name) / 'Sea Power'
        self.streaming = self.game / 'Sea Power_Data/StreamingAssets'
        (self.streaming / 'original/vessels').mkdir(parents=True)
        (self.streaming / 'original/vessels/usn_cvn_enterprise.ini').write_text('native carrier')
        (self.streaming / 'user/missions').mkdir(parents=True)
        (self.streaming / 'user/missions/save.ini').write_text('saved mission')
        (self.streaming / 'RAN-Carrier-Australis/vessels').mkdir(parents=True)
        (self.streaming / 'RAN-Carrier-Australis/vessels/ran_cv.ini').write_text('custom carrier')
        self.target = self.streaming / hotfix.MOD_NAME
        self.target.mkdir()
        source = ROOT / 'RAN-F111N-Naval-Wing'
        paths = [Path('_info.ini'), hotfix.MODEL] + [Path(k) for k in hotfix.SOURCE_INI_SHA256]
        for rel in paths:
            dest = self.target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, dest)
        for name in ('animations_ran_f111n.ini', 'animations_ran_fb111n.ini'):
            dest = self.target / 'animations' / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / 'animations' / name, dest)
        (self.target / 'local-note.txt').write_text('untouched extra content')
        self.running = mock.patch.object(hotfix, 'game_is_running', return_value=False)
        self.running.start()
        self.addCleanup(self.running.stop)

    def test_install_backup_preserve_carriers_idempotent(self):
        prior = snapshot(self.streaming)
        backup = hotfix.install(self.streaming)
        for rel in [hotfix.MODEL] + [Path(k) for k in hotfix.SOURCE_INI_SHA256]:
            self.assertEqual((backup / rel).read_bytes(), prior[str(Path(hotfix.MOD_NAME)/rel)])
        self.assertEqual((self.target/'local-note.txt').read_text(), 'untouched extra content')
        self.assertFalse((self.target/'vessels').exists())
        self.assertEqual((self.streaming/'original/vessels/usn_cvn_enterprise.ini').read_text(), 'native carrier')
        self.assertEqual((self.streaming/'RAN-Carrier-Australis/vessels/ran_cv.ini').read_text(), 'custom carrier')
        self.assertEqual((self.streaming/'user/missions/save.ini').read_text(), 'saved mission')
        self.assertEqual(hotfix.digest((self.target/hotfix.MODEL).read_bytes()), hotfix.PATCHED_MODEL_SHA256)
        for name, checksum in hotfix.PATCHED_INI_SHA256.items():
            self.assertEqual(hotfix.digest((self.target/name).read_bytes()), checksum)
        self.assertIsNone(hotfix.install(self.game))

    def test_wrong_aircraft_refused_before_replacing(self):
        p = self.target / next(iter(hotfix.SOURCE_INI_SHA256))
        p.write_text(p.read_text()+'\n# custom edit\n')
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, 'differs from tested'):
            hotfix.install(self.game)
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse((self.game/'RAN-F111N-backups').exists())

    def test_wrong_model_refused(self):
        with (self.target/hotfix.MODEL).open('ab') as stream: stream.write(b'\n# custom edit\n')
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, 'differs from tested'):
            hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_broken_mudpig_door_sequence_refused(self):
        anim = self.target / 'animations/animations_ran_fb111n.ini'
        text = anim.read_text().replace('Sequence1_Model=bay_l', 'Sequence1_Model=wrong_door', 1)
        anim.write_text(text)
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, 'must target both bay_l and bay_r'):
            hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)
        self.assertFalse((self.game / 'RAN-F111N-backups').exists())

    def test_missing_aircraft_animation_refused(self):
        (self.target / 'animations/animations_ran_f111n.ini').unlink()
        before = snapshot(self.streaming)
        with self.assertRaisesRegex(RuntimeError, 'Required mod file missing'):
            hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_compatible_custom_animation_timing_preserved(self):
        anim = self.target / 'animations/animations_ran_fb111n.ini'
        source = anim.read_text()
        source = source.replace('Step2=3|x,y,z|x,y,90|EaseInOut', 'Step2=4|x,y,z|x,y,90|EaseInOut')
        anim.write_text(source)
        backup = hotfix.install(self.streaming)
        self.assertEqual(anim.read_text(), source)
        self.assertEqual((backup / 'animations/animations_ran_fb111n.ini').read_text(), source)

    def test_game_running_refused(self):
        before = snapshot(self.streaming)
        with mock.patch.object(hotfix, 'game_is_running', return_value=True):
            with self.assertRaisesRegex(RuntimeError, 'Close Sea Power'):
                hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_swap_failure_restores_previous_mod(self):
        before = snapshot(self.streaming)
        original = hotfix.os.replace
        calls = 0
        def fail_second(src, dst):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('simulated swap failure')
            return original(src, dst)
        with mock.patch.object(hotfix.os, 'replace', side_effect=fail_second):
            with self.assertRaisesRegex(RuntimeError, 'previous installed mod was restored'):
                hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_interruption_after_first_swap_restores_mod(self):
        before = snapshot(self.streaming)
        original = hotfix.os.replace
        calls = 0
        def interrupt_after_first(src, dst):
            nonlocal calls
            calls += 1
            result = original(src, dst)
            if calls == 1:
                raise KeyboardInterrupt()
            return result
        with mock.patch.object(hotfix.os, 'replace', side_effect=interrupt_after_first):
            with self.assertRaisesRegex(RuntimeError, 'previous installed mod was restored'):
                hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_interruption_after_second_swap_restores_mod(self):
        before = snapshot(self.streaming)
        original = hotfix.os.replace
        calls = 0
        def interrupt_after_second(src, dst):
            nonlocal calls
            calls += 1
            result = original(src, dst)
            if calls == 2:
                raise KeyboardInterrupt()
            return result
        with mock.patch.object(hotfix.os, 'replace', side_effect=interrupt_after_second):
            with self.assertRaisesRegex(RuntimeError, 'previous installed mod was restored'):
                hotfix.install(self.streaming)
        self.assertEqual(snapshot(self.streaming), before)

    def test_unsafe_model_symlink_refused(self):
        model = self.target/hotfix.MODEL
        model.unlink()
        model.symlink_to(ROOT/'RAN-F111N-Naval-Wing'/hotfix.MODEL)
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            hotfix.install(self.streaming)
        self.assertTrue(model.is_symlink())

if __name__ == '__main__':
    unittest.main()
