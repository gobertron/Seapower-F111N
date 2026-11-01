#!/usr/bin/env python3
"""Check the folder selected for upload, not just a generated VDF."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from f111_workshop_validator import validate_workshop_root


class WorkshopRootTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'RAN-F111N-Naval-Wing'
        self.root.mkdir()
        (self.root / '_info.ini').write_text('[Language_en]\nName=RAN F-111N Naval Wing V9.0\n')
        for name in ('aircraft', 'assets', 'systems', 'animations', 'ammunition', 'language_en'):
            (self.root / name).mkdir()
        for family in ('f', 'fb', 'rf', 'ef'):
            for year in ('', '_1985', '_1995', '_2003'):
                for suffix in ('', '_squadrons'):
                    (self.root / 'aircraft' / f'ran_{family}-111n{year}{suffix}.ini').write_text('[General]\n')

    def test_correct_root(self):
        self.assertEqual(validate_workshop_root(self.root)['aircraft'], 16)

    def test_wrapper_user_parent_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'Missing _info.ini'):
            validate_workshop_root(self.root.parent)

    def test_unrelated_sr71_paths_rejected(self):
        (self.root / 'aircraft' / 'usn_sr-71a.ini').write_text('fake')
        with self.assertRaisesRegex(RuntimeError, 'SR-71'):
            validate_workshop_root(self.root)

    def test_nested_other_mod_rejected(self):
        other = self.root / 'other-mod'
        other.mkdir()
        (other / '_info.ini').write_text('fake')
        with self.assertRaisesRegex(RuntimeError, 'Nested mod'):
            validate_workshop_root(self.root)

    def test_missing_edition_rejected(self):
        (self.root / 'aircraft' / 'ran_ef-111n_2003.ini').unlink()
        with self.assertRaisesRegex(RuntimeError, 'Missing or empty'):
            validate_workshop_root(self.root)

    def test_symlink_rejected(self):
        (self.root / 'assets' / 'foreign').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'Symlink'):
            validate_workshop_root(self.root)

    def test_wrong_info_rejected(self):
        (self.root / '_info.ini').write_text('[Language_en]\nName=userdata\n')
        with self.assertRaisesRegex(RuntimeError, 'does not identify'):
            validate_workshop_root(self.root)


if __name__ == '__main__':
    unittest.main()
