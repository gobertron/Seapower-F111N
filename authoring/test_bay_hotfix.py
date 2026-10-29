#!/usr/bin/env python3
"""Exercise the offline hotfix against disposable V9 installations."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bay_hotfix', ROOT / 'fix-f111n-v9-bay-doors.py')
hotfix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotfix)

class HotfixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.game = Path(self.tmp.name) / 'Sea Power'
        self.target = self.game / 'Sea Power_Data/StreamingAssets/user/RAN-F111N-Naval-Wing'
        self.target.mkdir(parents=True)
        (self.target / '_info.ini').write_text('[Language_en]\nName=RAN F-111N Naval Wing V9.0 - 1980 / 1985\n')
        (self.target / 'aircraft').mkdir()
        self.originals = {}
        for family in hotfix.FAMILIES:
            for year in hotfix.YEARS:
                rel = Path('aircraft') / f'ran_{family}-111n{year}.ini'
                data = (b'[Submodels]\r\nGeneral_1=hull\r\nbay_l=bay_l\r\n'
                        b'bay_r=bay_r\r\npave_body=pave_body\r\n[bay_l]\r\nMesh=bay_l\r\n')
                (self.target / rel).write_bytes(data)
                self.originals[rel] = data
        (self.target / 'aircraft/ran_ef-111n.ini').write_bytes(b'Unchanged EF model')
        (self.target / 'carrier-custom.ini').write_bytes(b'Unchanged carrier configuration')
        self.running = patch.object(hotfix, 'game_is_running', return_value=False)
        self.running.start()
        self.addCleanup(self.running.stop)

    def test_patch_backup_and_idempotence(self):
        backup = hotfix.install(self.game)
        for rel, original in self.originals.items():
            self.assertEqual((backup / rel).read_bytes(), original)
            actual = (self.target / rel).read_bytes()
            expected = original.replace(b'bay_l=bay_l', b'General_12=bay_l').replace(b'bay_r=bay_r', b'General_13=bay_r').replace(b'pave_body=pave_body', b'General_14=pave_body')
            self.assertEqual(actual, expected)
        for rel in ('aircraft/ran_ef-111n.ini', 'carrier-custom.ini'):
            self.assertEqual((self.target / rel).read_bytes(), (backup / rel).read_bytes())
        self.assertIsNone(hotfix.install(self.game))
        self.assertEqual(len(list((self.game / 'RAN-F111N-backups').iterdir())), 1)

    def test_unknown_input_and_occupied_slot_are_rejected_before_changes(self):
        path = self.target / 'aircraft/ran_fb-111n_2003.ini'
        path.write_bytes(path.read_bytes().replace(b'bay_l=bay_l', b'General_12=another_mesh'))
        before = {p: p.read_bytes() for p in self.target.rglob('*') if p.is_file()}
        with self.assertRaises(ValueError):
            hotfix.install(self.game)
        self.assertEqual(before, {p: p.read_bytes() for p in self.target.rglob('*') if p.is_file()})
        self.assertFalse((self.game / 'RAN-F111N-backups').exists())

    def test_mismatched_version_and_running_game_are_rejected(self):
        (self.target / '_info.ini').write_text('Name=RAN F-111N Naval Wing V8\n')
        with self.assertRaises(RuntimeError): hotfix.install(self.game)
        with patch.object(hotfix, 'game_is_running', return_value=True):
            with self.assertRaises(RuntimeError): hotfix.install(self.game)
        self.assertFalse((self.game / 'RAN-F111N-backups').exists())

    def test_failed_commit_restores_original_mod(self):
        real_replace = hotfix.os.replace
        def fail_install(src, dst):
            if Path(src).name == self.target.name and '.ran-f111n-bay-stage-' in str(src):
                raise OSError('simulated failure')
            return real_replace(src, dst)
        with patch.object(hotfix.os, 'replace', side_effect=fail_install):
            with self.assertRaises(OSError): hotfix.install(self.game)
        for rel, original in self.originals.items():
            self.assertEqual((self.target / rel).read_bytes(), original)
        self.assertFalse(list(self.target.parent.glob('.ran-f111n-bay-stage-*')))

if __name__ == '__main__': unittest.main()
