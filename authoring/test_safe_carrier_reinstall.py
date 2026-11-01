#!/usr/bin/env python3
"""Tests for the installer that omits carrier-vessel overrides."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import types
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'clean-reinstall-f111n-v9-safe-carriers.sh').read_text()
s=s.split("<<'V9_REPLACEMENT_PY'\n",1)[1].rsplit('\nV9_REPLACEMENT_PY',1)[0]
mod=types.ModuleType('safe_carrier_installer')
exec(compile(s,'clean-reinstall-f111n-v9-safe-carriers.sh','exec'),mod.__dict__)

class SafeInstall(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.game=Path(self.tmp.name)/'steamapps/common/Sea Power'
        self.streaming=self.game/'Sea Power_Data/StreamingAssets'
        (self.streaming/'original/vessels').mkdir(parents=True)
        (self.streaming/'original/vessels/usn_cvn_enterprise.ini').write_text('base carrier')
        (self.streaming/'user/missions').mkdir(parents=True)
        (self.streaming/'user/missions/save.ini').write_text('keep')
        self.other=self.streaming/'OtherCarrier/vessels';self.other.mkdir(parents=True)
        (self.other/'usn_cvn_enterprise.ini').write_text('other carrier')
        self.old=self.streaming/'RAN-F111N-Naval-Wing'
        shutil.copytree(ROOT/'RAN-F111N-Naval-Wing',self.old)
        self.run=mock.patch.object(mod,'game_is_running',return_value=False);self.run.start();self.addCleanup(self.run.stop)

    def install(self,**kwargs):
        with contextlib.redirect_stdout(io.StringIO()): return mod.install(ROOT,self.game,**kwargs)

    def test_full_install_replaces_no_carriers_and_workshop_safe(self):
        backup=self.install(prepare_upload=True)
        self.assertTrue((backup/'RAN-F111N-Naval-Wing/vessels/usn_cvn_enterprise.ini').is_file())
        self.assertFalse((self.old/'vessels').exists())
        self.assertTrue((self.old/'aircraft/ran_f-111n.ini').is_file())
        self.assertEqual((self.streaming/'original/vessels/usn_cvn_enterprise.ini').read_text(),'base carrier')
        self.assertEqual((self.other/'usn_cvn_enterprise.ini').read_text(),'other carrier')
        self.assertEqual((self.streaming/'user/missions/save.ini').read_text(),'keep')
        bundles=list((self.game/'RAN-F111N-workshop/3810606011').iterdir());self.assertEqual(len(bundles),1)
        bundle=bundles[0]
        self.assertFalse((bundle/'content/vessels').exists())
        self.assertEqual(mod.validate_workshop_root(bundle/'content')['aircraft'],16)
        description=(bundle/'description.txt').read_text()
        self.assertLessEqual(len(description.encode('utf-8')),8000)
        self.assertNotIn('installer creates compatibility overrides',description)
        self.assertIn('removes carrier vessel overrides',description)
        self.assertIn('Carrier Compatibility Repair',(bundle/'update-notes.txt').read_text())
        self.assertIn('Carrier overrides removed', (bundle/'upload.vdf').read_text())
        mod.verify_workshop_bundle(bundle)
        self.assertEqual(json.loads((self.old/'CARRIER_COMPATIBILITY.json').read_text())['mode'],'carrier_vessel_overrides_removed')
        self.install(prepare_upload=True)
        self.assertFalse((self.old/'vessels').exists())
        self.assertEqual((self.other/'usn_cvn_enterprise.ini').read_text(),'other carrier')

    def test_dry_run_keeps_old_vessels_and_carriers(self):
        self.install(dry_run=True,prepare_upload=True)
        self.assertTrue((self.old/'vessels/usn_cvn_enterprise.ini').is_file())
        self.assertEqual((self.other/'usn_cvn_enterprise.ini').read_text(),'other carrier')
        self.assertFalse((self.game/'RAN-F111N-backups').exists())

    def test_missing_bundled_description_aborts_before_swap(self):
        with mock.patch.object(mod,'prepare_workshop',side_effect=RuntimeError('injected')):
            with self.assertRaisesRegex(RuntimeError,'injected'):
                self.install(prepare_upload=True)
        self.assertTrue((self.old/'vessels/usn_cvn_enterprise.ini').is_file())
        self.assertEqual((self.other/'usn_cvn_enterprise.ini').read_text(),'other carrier')

if __name__=='__main__':unittest.main()
