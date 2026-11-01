#!/usr/bin/env python3
"""Exercise clean reinstall against isolated Sea Power fixtures only."""
import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import types
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
script=(ROOT/'clean-reinstall-f111n-v9.sh').read_text()
source=script.split("<<'V9_REPLACEMENT_PY'\n",1)[1].rsplit('\nV9_REPLACEMENT_PY',1)[0]
mod=types.ModuleType('clean_reinstall')
exec(compile(source,'clean-reinstall-f111n-v9.sh','exec'),mod.__dict__)

def seed(path,kind):
    (path/'aircraft').mkdir(parents=True)
    (path/'_info.ini').write_text('[General]\nName='+('RAN F-111N Naval Wing V8' if kind=='f' else 'SR-71 Blackbird V2')+'\n')
    (path/'aircraft'/('ran_f-111n.ini' if kind=='f' else 'bb1_usaf_sr-71a.ini')).write_text('aircraft contents')
    (path/'keep-in-backup.txt').write_text('payload')

def snapshot(folder):
    return {str(p.relative_to(folder)):p.read_bytes() for p in folder.rglob('*') if p.is_file()}

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.game=Path(self.tmp.name)/'Sea Power';self.streaming=self.game/'Sea Power_Data/StreamingAssets'
        (self.streaming/'original').mkdir(parents=True)
        self.user=self.streaming/'user'; self.user.mkdir()
        self.wrapper=self.user/'userdata'; self.f=self.wrapper/'RAN-F111N-Naval-Wing';self.sr=self.wrapper/'SR71-Blackbird-Prototype-1'
        seed(self.f,'f');seed(self.sr,'sr')
        (self.wrapper/'aircraft').mkdir(parents=True)
        (self.wrapper/'aircraft/bb1_usaf_sr-71a.ini').write_text('loose wrapper')
        (self.wrapper/'other-mod/aircraft').mkdir(parents=True)
        (self.wrapper/'other-mod/aircraft/other.ini').write_text('other')
        (self.user/'missions').mkdir();(self.user/'missions/keep.ini').write_text('save')
        (self.user/'aircraft').mkdir();(self.user/'aircraft/ran_f-111n.ini').write_text('loose')
        (self.user/'aircraft/other.ini').write_text('untouched')
        (self.user/'assets/ran_f111n/models').mkdir(parents=True)
        (self.user/'assets/ran_f111n/models/asset.obj').write_text('model')
        (self.user/'systems').mkdir();(self.user/'systems/weapons.ini').write_text('shared')
        self.ran=mock.patch.object(mod,'game_is_running',return_value=False);self.ran.start();self.addCleanup(self.ran.stop)
    def call(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):return mod.install(ROOT,self.game,**kwargs)
    def test_clean_install_and_restoration(self):
        f=snapshot(self.f);sr=snapshot(self.sr)
        backup=self.call(prepare_upload=True)
        target=self.streaming/'RAN-F111N-Naval-Wing';restored=self.streaming/'SR71-Blackbird-Prototype-1'
        self.assertTrue((target/'_info.ini').is_file());self.assertEqual(snapshot(restored),sr)
        self.assertEqual(snapshot(backup/self.f.relative_to(self.streaming)),f)
        self.assertEqual(snapshot(backup/self.sr.relative_to(self.streaming)),sr)
        self.assertFalse(self.f.exists());self.assertFalse(self.sr.exists())
        self.assertEqual((self.user/'missions/keep.ini').read_text(),'save')
        self.assertEqual((self.user/'aircraft/other.ini').read_text(),'untouched')
        self.assertEqual((self.user/'systems/weapons.ini').read_text(),'shared')
        self.assertTrue((self.wrapper/'other-mod/aircraft/other.ini').is_file())
        self.assertFalse((self.user/'aircraft/ran_f-111n.ini').exists())
        self.assertFalse((self.wrapper/'aircraft/bb1_usaf_sr-71a.ini').exists())
        self.assertEqual((backup/'user/userdata/aircraft/bb1_usaf_sr-71a.ini').read_text(),'loose wrapper')
        self.assertFalse((self.user/'assets/ran_f111n').exists())
        self.assertEqual((backup/'user/aircraft/ran_f-111n.ini').read_text(),'loose')
        payload=next((self.game/'RAN-F111N-workshop/3810606011').glob('*/content'))
        self.assertEqual(mod.validate_workshop_root(payload)['aircraft'],16)
        self.assertFalse(any('sr71' in str(p).lower().replace('-','') for p in payload.rglob('*')))
    def test_dry_run_is_read_only(self):
        before=snapshot(self.game);self.call(dry_run=True,prepare_upload=True);self.assertEqual(snapshot(self.game),before)
    def test_sr_conflict_stops_before_changes(self):
        seed(self.streaming/'SR71-Blackbird-Prototype-1','sr');before=snapshot(self.game)
        with self.assertRaisesRegex(RuntimeError,'same destination'):self.call()
        self.assertEqual(snapshot(self.game),before)
    def test_failed_sr_restore_rolls_back_everything(self):
        before=snapshot(self.streaming);real=shutil.copytree
        def bad(source,dest,*args,**kw):
            if Path(dest)==self.streaming/'SR71-Blackbird-Prototype-1':
                Path(dest).mkdir();raise OSError('simulated disk full')
            return real(source,dest,*args,**kw)
        with mock.patch.object(shutil,'copytree',bad):
            with self.assertRaisesRegex(RuntimeError,'restored'):self.call()
        self.assertEqual(snapshot(self.streaming),before)
    def test_mixed_mod_is_not_removed(self):
        mixed=self.user/'mixed';seed(mixed,'f');(mixed/'aircraft/other.ini').write_text('other')
        before=snapshot(mixed);self.call();self.assertEqual(snapshot(mixed),before)

if __name__=='__main__':unittest.main()
