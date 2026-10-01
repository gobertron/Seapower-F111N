#!/usr/bin/env python3
"""Install only this local mod. Preserve replaced versions outside StreamingAssets."""
from pathlib import Path
import sys, re, shutil, tempfile, hashlib, datetime

PACKAGE=Path(__file__).resolve().parent
SOURCE=PACKAGE/'RAN-F111N-Naval-Wing'
IDS={'ran_f-111n','ran_fb-111n','ran_rf-111n','ran_ef-111n'}

def discover():
    home=Path.home();libs=set()
    for root in [home/'.local/share/Steam',home/'.steam/steam',home/'.steam/root']:
        if root.is_dir():libs.add(root.resolve())
        vdf=root/'steamapps/libraryfolders.vdf'
        if vdf.is_file():
            for value in re.findall(r'"path"\s+"([^"]+)"',vdf.read_text(errors='replace')):
                libs.add(Path(value.replace('\\\\','\\')).expanduser())
    return sorted({(p/'steamapps/common/Sea Power').resolve() for p in libs
                   if (p/'steamapps/common/Sea Power/Sea Power_Data/StreamingAssets').is_dir()})

def verify():
    manifest=PACKAGE/'MOD_SHA256.txt'
    if not manifest.is_file():raise RuntimeError('MOD_SHA256.txt is missing; extract the complete package.')
    for line in manifest.read_text().splitlines():
        digest,name=line.split('  ',1);p=SOURCE/name
        if not p.is_file():raise RuntimeError('Missing package file: '+name)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise RuntimeError('Package checksum failed: '+name)

def own_mod(folder):
    if not (folder/'_info.ini').is_file():return False
    description=(folder/'_info.ini').read_text(errors='replace').lower()
    if 'ran f-111n naval wing' not in description:return False
    aircraft=folder/'aircraft'
    return aircraft.is_dir() and any((aircraft/(u+'.ini')).is_file() for u in IDS)

def main():
    if not SOURCE.is_dir():raise RuntimeError('Extract the complete ZIP before running the installer.')
    verify()
    if len(sys.argv)>1:
        game=Path(sys.argv[1]).expanduser().resolve()
    else:
        candidates=discover()
        if len(candidates)!=1:
            print('Choose the Sea Power installation explicitly:')
            for p in candidates:print(' ',p)
            print('Usage: python3 install-ran-f111n.py "/full/path/to/Sea Power"')
            return 2
        game=candidates[0]
    streaming=game/'Sea Power_Data/StreamingAssets'
    if not streaming.is_dir():raise RuntimeError('This path is not a Sea Power installation: '+str(game))
    target=streaming/'user/RAN-F111N-Naval-Wing';target.parent.mkdir(parents=True,exist_ok=True)
    if SOURCE.resolve()==target.resolve():raise RuntimeError('Run the installer from the extracted download, outside the installed mod.')
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup=game/'RAN-F111N-backups'/stamp
    # Stage a complete copy first. Do not disturb the previous installation if copying fails.
    stage=Path(tempfile.mkdtemp(prefix='ran-f111n-stage-',dir=game))/'RAN-F111N-Naval-Wing'
    shutil.copytree(SOURCE,stage)
    from carrier_compatibility import generate
    try:
        carrier_report=generate(game,stage,sys.argv[2:])
        if carrier_report['errors']:
            raise RuntimeError('Carrier compatibility could not be generated: '+str(carrier_report['errors']))
    except Exception:
        shutil.rmtree(stage.parent)
        raise
    existing=[]
    for base in [streaming,streaming/'user']:
        if not base.is_dir():continue
        for p in base.iterdir():
            if p.is_dir() and p.name not in ['original','user'] and own_mod(p):existing.append(p)
    if target.exists() and target not in existing:
        shutil.rmtree(stage.parent)
        raise RuntimeError('The destination exists but is not recognised as this mod; leaving it unchanged.')
    moved=[]
    try:
        for p in existing:
            dest=backup/p.relative_to(streaming);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(p),str(dest));moved.append((p,dest))
        shutil.move(str(stage),str(target))
    except Exception:
        if target.exists():shutil.rmtree(target)
        for p,dest in reversed(moved):
            p.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(dest),str(p))
        raise
    finally:
        if stage.parent.exists():shutil.rmtree(stage.parent)
    print('Installed:',target)
    if moved:print('Previous versions saved:',backup)
    print('Carrier definitions prepared:',len(carrier_report['carriers']))
    print('In Sea Power Mod Manager: enable RAN F-111N Naval Wing V8 and disable older RAN Naval Wing copies.')
    print('Give Naval Wing priority over carrier mods; keep source carrier mods enabled for their meshes.')
    print('Keep your existing Anchor Chain setup enabled. Restart Sea Power after changing the mod list.')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print('Installation stopped:',e,file=sys.stderr);sys.exit(1)
