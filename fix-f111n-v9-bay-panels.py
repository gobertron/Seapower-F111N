#!/usr/bin/env python3
"""Back up and repair the aircraft-only V9.0 bomb-bay panel meshes.

Usage: python3 fix-f111n-v9-bay-panels.py "/path/to/Sea Power/Sea Power_Data/StreamingAssets"
The game must be closed. The currently installed mod is backed up in full.
This does not create or change carrier-vessel compatibility overrides.
"""
import fcntl
import hashlib
import configparser
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

"""Add two full skins using the existing bay-door hinges and hull UV atlas.

The skins are alternate-history geometry, generated with the Python standard
library. Their outline follows the native leaves' measured world footprint.
The original objects and all non-bay vertices and faces are kept unchanged.
"""
import re

NAMES = ('ran_bay_panel_l', 'ran_bay_panel_r')
OLD = ('bay_l', 'bay_r')

# (world z, half-width). The stock door pivots are (±.00993,-.012672,.063121).
# Samples trace the pre-existing door outline; adjacent samples are interpolated.
OUTLINE = ((.03230,.01032),(.03300,.01101),(.04000,.01077),
           (.05000,.01042),(.06000,.01007),(.07000,.00968),
           (.08000,.00927),(.08500,.00906),(.09000,.00762),
           (.09300,.00678),(.09500,.00623),(.09680,.00572))

def patch_obj(text):
    present = [bool(re.search(r'(?m)^o '+re.escape(name)+r'\s*$', text)) for name in NAMES]
    if all(present):
        return text
    if any(present):
        raise ValueError('partial generated panel geometry detected')
    for name in OLD:
        if len(re.findall(r'(?m)^o '+name+r'\s*$', text)) != 1:
            raise ValueError('expected original OBJ object '+name)
    counts = {prefix: len(re.findall(r'(?m)^'+prefix+r' ', text)) for prefix in ('v','vt','vn')}
    chunks = [text.rstrip('\n')+'\n']
    for side, name, pivot_x, uv_u, uv_v in (
        (1, NAMES[0], .009929, .4956, .0821),
        (-1, NAMES[1], -.009936, .4919, .4159),
    ):
        chunks.append('\n# Naval Wing V9 closed-bay surface; local to original hinge\no '+name+'\n')
        v0, t0, n0 = counts['v'], counts['vt'], counts['vn']
        for thickness in (0., .00018):
            for z,width in OUTLINE:
                # The centre seam is lowest; outside rises with the belly.
                # The back face is offset so it is not coplanar with the skin.
                for world_x, world_y in ((0.,-.01422), (side*width,-.01306)):
                    chunks.append('v %.7f %.7f %.7f\n' % (world_x-pivot_x,world_y+thickness+.012672,z-.063121))
        for z,width in OUTLINE:
            # Nondegenerate UVs stay inside a plain, opaque nearby belly patch.
            t = (z-OUTLINE[0][0])/(OUTLINE[-1][0]-OUTLINE[0][0])
            chunks.append('vt %.7f %.7f\nvt %.7f %.7f\n' % (uv_u-.00035,uv_v+(t-.5)*.0007,uv_u+.00035,uv_v+(t-.5)*.0007))
        # Opposing normals and faces permit the door to be seen while open.
        chunks.append('vn %.6f -0.993000 0.000000\n' % (side*.118))
        chunks.append('vn %.6f 0.993000 0.000000\n' % (-side*.118))
        def face(i,j,k,n,inside=False):
            return 'f '+' '.join('%d/%d/%d' % (v0+q+(len(OUTLINE)*2 if inside else 0),t0+q,n0+n) for q in (i,j,k))+'\n'
        for i in range(len(OUTLINE)-1):
            a,b,c,d=2*i+1,2*i+2,2*i+3,2*i+4
            tris=((a,b,d),(a,d,c)) if side==1 else ((a,d,b),(a,c,d))
            for p in tris:
                chunks.append(face(*p,1));chunks.append(face(p[2],p[1],p[0],2,True))
        counts['v'] += len(OUTLINE)*4
        counts['vt'] += len(OUTLINE)*2
        counts['vn'] += 2
    return ''.join(chunks)

def patch_aircraft(text):
    for old,new in zip(OLD,NAMES):
        pattern=r'(?ms)(^\['+old+r'\]\s*\n)(.*?)(?=^\[|\Z)'
        matches=list(re.finditer(pattern,text))
        if len(matches)!=1:
            raise ValueError('expected one section '+old)
        section=matches[0].group(2)
        values=re.findall(r'(?m)^Mesh=([^\r\n]*)',section)
        if values == [new]: continue
        if values != [old]: raise ValueError('unexpected '+old+' mesh')
        replacement=re.sub(r'(?m)^Mesh='+old+r'[ \t]*\r?$', 'Mesh='+new, section,count=1)
        text=text[:matches[0].start(2)]+replacement+text[matches[0].end(2):]
    return text


MOD_NAME = 'RAN-F111N-Naval-Wing'
MODEL = Path('assets/ran_f111n/models/f-111f/f-111f.obj')
SOURCE_MODEL_SHA256 = 'bbddbf9b15e011ae88366ad820889afbf4d0b38f0b5496e6887c369c007e910d'
SOURCE_INI_SHA256 = {
    'aircraft/ran_f-111n.ini':'246cf9752b45238f16dbe47bde57ecae9c7bfbd04fabe6720acd01fc4539585c',
    'aircraft/ran_f-111n_1985.ini':'3b909024e806de5e884c8e70b679629a3613cb842f31c103bd24d4c8a76993ee',
    'aircraft/ran_f-111n_1995.ini':'777ba1d6ad4496677f7d7cd3adb09dfdcd0984c96725bf258fa1b849adf65c6e',
    'aircraft/ran_f-111n_2003.ini':'20a65ffc9f02104e56ddc2f55e6d028afad22e330243ae14551c00f01b8a6be6',
    'aircraft/ran_fb-111n.ini':'261e25693d20c1ab8698ed4622be26ebb4545b022a4bd9e09b538c362aa07f6a',
    'aircraft/ran_fb-111n_1985.ini':'2c73fc5c680581f1f7d79fc2f52af9c081377290d460a848694fbead31003b0a',
    'aircraft/ran_fb-111n_1995.ini':'3e39463b0b7703c171a7c6c7f5c02e2fcb95133c8a61fa1ce94addf5752e40f6',
    'aircraft/ran_fb-111n_2003.ini':'c7b6c7c24bc18598ef17d5981ae512c8817069fcfaedc703a9c46a1bf06596b3',
    'aircraft/ran_rf-111n.ini':'6d327cff3274b452c0bf259bd8402212996d082a9cfdfa9f5cc5f555de6aed6c',
    'aircraft/ran_rf-111n_1985.ini':'52bb5d69bdaf5f35290a36def98b12fd8174bbae47da464131150c9a82be119c',
    'aircraft/ran_rf-111n_1995.ini':'70e672e9b7e1926a5cdb664aff8b4b7da3dc45b38d7bb74d027112f931f3fa1b',
    'aircraft/ran_rf-111n_2003.ini':'bf875525293f9449a7fba701a85a069fb472670c2434b66bea78820c968754db',
}
PATCHED_MODEL_SHA256 = 'c92fe89547f2f8d86e3a372d08997067041143350b6581ebc61832a47fa7545d'
PATCHED_INI_SHA256 = {
    'aircraft/ran_f-111n.ini': '11c6a013d95f2fd848aee8c0b70eb49170884d9d487b459942576a0f5d30972c',
    'aircraft/ran_f-111n_1985.ini': '42fe0d46f16fafc4efa71089d6c7fcbba92bbaa4a8c9c58b7c10eefc943eeddc',
    'aircraft/ran_f-111n_1995.ini': '476b17bad32a517d0cccfff17c1eca029d9234f655576efd5c98a7139e34b31d',
    'aircraft/ran_f-111n_2003.ini': '60f0a7197a9c5f5a723ce32b3da57f990da31069508a526982a0a3e0e8c92a87',
    'aircraft/ran_fb-111n.ini': '796e146b5ca57335f46b868ba2669ad5570c2cf6b34cf895b939253e1b2fb879',
    'aircraft/ran_fb-111n_1985.ini': '3a5d9c211c2a4b64c67cde6e2da8779e0ef46d894976225c9549cd896130fc7f',
    'aircraft/ran_fb-111n_1995.ini': 'dea3d8b1c2ef56c0472ce451177fb2216f1ce5ea676b549eab30d749c6c2c0d7',
    'aircraft/ran_fb-111n_2003.ini': '9444489f9bbe794cdf3afba46424d22c6118db94a3e95265341cbd82f086401e',
    'aircraft/ran_rf-111n.ini': '71dc2e697bf1e3aa04cf4cc4c04d966d696ce93199ff91a3e2da9afa82c40a24',
    'aircraft/ran_rf-111n_1985.ini': '971069c9bc14a17a3c7f1a2f76b0cbc1370d4085c6c826f1eeafe03c531b86eb',
    'aircraft/ran_rf-111n_1995.ini': 'a46d0d988e9baccdc7a8cc35455e7c4d0c411cbf12c2a01b17d3399db29d6cb2',
    'aircraft/ran_rf-111n_2003.ini': '08c36788b8d9ed37dc8807a43ab5f53f1074994161f8097c983db7be6ee25585',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def game_is_running():
    proc = Path('/proc')
    if not proc.is_dir():
        return False
    for process in proc.iterdir():
        if not process.name.isdigit():
            continue
        try:
            command = (process / 'cmdline').read_bytes().split(b'\0')
        except OSError:
            continue
        for index, value in enumerate(command):
            name = value.decode(errors='replace').replace('\\', '/').rsplit('/', 1)[-1]
            normal = re.sub(r'[\s_-]', '', name).casefold()
            if normal in {'seapower.exe', 'seapower.x86_64'} or (index == 0 and normal == 'seapower'):
                return True
    return False


def resolve_game(path):
    selected = Path(path).expanduser().resolve()
    if selected.name == 'StreamingAssets' and selected.parent.name == 'Sea Power_Data':
        game, streaming = selected.parent.parent, selected
    else:
        game, streaming = selected, selected / 'Sea Power_Data/StreamingAssets'
    if not (streaming / 'original').is_dir():
        raise RuntimeError('Sea Power StreamingAssets/original not found: ' + str(streaming))
    return game, streaming


def safe_regular_file(root, relative):
    path = root
    for part in Path(relative).parts:
        path = path / part
        if path.is_symlink():
            raise RuntimeError('Refusing a symlink in mod file path: ' + str(path))
    if not path.is_file():
        raise RuntimeError('Required mod file missing: ' + str(path))
    return path


def read_ini_bytes(data, label):
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    parser.optionxform = str
    try:
        parser.read_string(data.decode('utf-8-sig'))
    except (configparser.Error, UnicodeError) as error:
        raise RuntimeError('Invalid INI ' + str(label) + ': ' + str(error)) from error
    return parser


def validate_animations(target, aircraft_bytes):
    """Verify actual per-aircraft references, door bindings and MudPig cycle.

    Preserve compatible local animation changes: no animation hash is imposed.
    This is a static check; rendering and release remain in-game tests.
    """
    refs = {}
    for name, data in aircraft_bytes.items():
        ini = read_ini_bytes(data, name)
        try:
            count = int(ini['Animations']['NumberOfAnimationReferences'])
            names = [ini['Animations']['AnimationFile_' + str(i)] for i in range(1, count + 1)]
        except (KeyError, ValueError, configparser.Error) as error:
            raise RuntimeError('Invalid animation references in ' + str(name)) from error
        if count < 1 or any(not re.fullmatch(r'[A-Za-z0-9_-]+', n) for n in names):
            raise RuntimeError('Unsafe or missing animation reference in ' + str(name))
        is_mudpig = Path(name).name.startswith('ran_fb-111n')
        if is_mudpig:
            try:
                bay = ini['WeaponSystem3']
                if (bay['OpenSystemAnimation'], bay['CloseSystemAnimation']) != ('Bay_Open', 'Bay_Close'):
                    raise RuntimeError('MudPig weapon bay does not reference Bay_Open and Bay_Close: ' + str(name))
            except (KeyError, configparser.Error) as error:
                raise RuntimeError('MudPig weapon bay animation references are missing: ' + str(name)) from error
        for file in names:
            refs[file] = refs.get(file, False) or is_mudpig

    snapshots = {}
    for file, mudpig in refs.items():
        rel = Path('animations') / (file + '.ini')
        snapshots[rel] = safe_regular_file(target, rel).read_bytes()
        anim = read_ini_bytes(snapshots[rel], rel)
        try:
            count = int(anim['Animations']['NumberOfAnimations'])
            registered = [anim['Animations']['Animation' + str(i)] for i in range(1, count + 1)]
            for action in ('Bay_Open', 'Bay_Close'):
                if action not in registered:
                    raise ValueError('action not registered: ' + action)
                group = anim[action]
                seq_count = int(group['NumberOfSequencesToPlay'])
                bindings = {}
                for i in range(1, seq_count + 1):
                    seq = group['Sequence' + str(i)]
                    model = group['Sequence' + str(i) + '_Model']
                    if seq not in anim:
                        raise ValueError('missing sequence: ' + seq)
                    if model in ('bay_l', 'bay_r'):
                        if model in bindings:
                            raise ValueError('duplicate target: ' + model)
                        bindings[model] = seq
                if set(bindings) != {'bay_l', 'bay_r'}:
                    raise ValueError(action + ' must target both bay_l and bay_r')
                if mudpig:
                    for side, sign in (('bay_l', 1), ('bay_r', -1)):
                        seq = anim[bindings[side]]
                        n = int(seq['NumberOfSteps'])
                        if n < 2:
                            raise ValueError('door sequence needs at least two steps')
                        first, last = seq['Step1'].split('|'), seq['Step' + str(n)].split('|')
                        first_time, last_time = float(first[0]), float(last[0])
                        first_angle = float(first[2].split(',')[2])
                        last_angle = float(last[2].split(',')[2])
                        if not all(math.isfinite(x) for x in (first_time, last_time, first_angle, last_angle)) or last_time <= first_time:
                            raise ValueError('invalid door animation timing or angle')
                        closed, opened = (first_angle, last_angle) if action == 'Bay_Open' else (last_angle, first_angle)
                        if abs(closed) > 0.01 or not 60 <= sign * opened <= 110:
                            raise ValueError(action + ' must rotate ' + side + ' between closed and outward-open')
        except (KeyError, IndexError, ValueError, configparser.Error) as error:
            raise RuntimeError('Incompatible bay animations in ' + str(rel) + ': ' + str(error)) from error
    return snapshots


def modifications(target):
    info = safe_regular_file(target, '_info.ini').read_text(encoding='utf-8-sig')
    if not re.search(r'(?im)^\s*Name\s*=\s*RAN\s+F-111N\s+Naval\s+Wing\s+V9\.0(?:\s|$)', info):
        raise RuntimeError('Folder is not the expected RAN F-111N Naval Wing V9.0.')
    rels = [MODEL] + [Path(f) for f in SOURCE_INI_SHA256]
    old = {r: safe_regular_file(target, r).read_bytes() for r in rels}
    animations = validate_animations(target, {r: old[r] for r in rels[1:]})
    hashes = {r: digest(b) for r, b in old.items()}
    source_hashes = {MODEL: SOURCE_MODEL_SHA256, **{Path(k): v for k,v in SOURCE_INI_SHA256.items()}}
    patched_hashes = {MODEL: PATCHED_MODEL_SHA256, **{Path(k): v for k,v in PATCHED_INI_SHA256.items()}}
    if hashes == patched_hashes:
        return {}, {**old, **animations}
    if hashes != source_hashes:
        bad = [str(k) for k in rels if hashes[k] != source_hashes.get(k)]
        raise RuntimeError('Installed source differs from tested V9.0 files or is partly patched; no changes made: ' + ', '.join(bad))
    replacement = {MODEL: patch_obj(old[MODEL].decode('utf-8')).encode('utf-8')}
    for rel in rels[1:]:
        replacement[rel] = patch_aircraft(old[rel].decode('utf-8')).encode('utf-8')
    if {r: digest(b) for r,b in replacement.items()} != patched_hashes:
        raise RuntimeError('Generated panel files differ from the tested output; no changes made.')
    return replacement, {**old, **animations}


def install(path):
    game, streaming = resolve_game(path)
    if game_is_running():
        raise RuntimeError('Close Sea Power before applying this repair.')
    target = streaming / MOD_NAME
    if target.is_symlink() or not target.is_dir():
        raise RuntimeError('Installed Naval Wing folder missing or a symlink: ' + str(target))
    replacement, original = modifications(target)
    if not replacement:
        print('This tested bay-panel repair is already installed; no changes made.')
        return None
    backup_root = game / 'RAN-F111N-backups'
    if backup_root.is_symlink():
        raise RuntimeError('Backup directory is a symlink; no changes made.')
    backup_root.mkdir(exist_ok=True)
    if backup_root.stat().st_dev != target.parent.stat().st_dev:
        raise RuntimeError('Backup and mod must be on the same filesystem; no changes made.')
    with (backup_root / '.bay-panel-repair.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Another bay-panel repair is running.')
        replacement2, original2 = modifications(target)
        if original != original2 or replacement != replacement2:
            raise RuntimeError('The mod changed during preparation; no changes made.')
        with tempfile.TemporaryDirectory(prefix='.f111n-bay-stage-', dir=target.parent) as temp:
            staged = Path(temp) / MOD_NAME
            shutil.copytree(target, staged, symlinks=True)
            validate_animations(staged, {Path(r): original[Path(r)] for r in SOURCE_INI_SHA256})
            for rel in original.keys() - replacement.keys():
                if safe_regular_file(staged, rel).read_bytes() != original[rel]:
                    raise RuntimeError('Staged animation changed during preparation: ' + str(rel))
            for rel, data in replacement.items():
                staged_file = safe_regular_file(staged, rel)
                if staged_file.read_bytes() != original[rel]:
                    raise RuntimeError('Staged file changed during preparation: ' + str(rel))
                staged_file.write_bytes(data)
            if game_is_running():
                raise RuntimeError('Sea Power started during preparation; no changes made.')
            for rel, data in original.items():
                if safe_regular_file(target, rel).read_bytes() != data:
                    raise RuntimeError('The mod changed during preparation: ' + str(rel))
            validate_animations(target, {Path(r): original[Path(r)] for r in SOURCE_INI_SHA256})
            backup_dir = Path(tempfile.mkdtemp(prefix='bay-panels-', dir=backup_root))
            backup = backup_dir / MOD_NAME
            try:
                os.replace(target, backup)
                os.replace(staged, target)
            except BaseException as failure:
                try:
                    if backup.exists():
                        if target.exists():
                            if staged.exists():
                                raise RuntimeError('Unexpected target appeared during replacement')
                            os.replace(target, staged)
                        os.replace(backup, target)
                    if not backup.exists():
                        backup_dir.rmdir()
                except BaseException as recovery_error:
                    raise RuntimeError('Repair stopped; manual recovery may be needed from ' + str(backup) + ': ' + str(recovery_error)) from failure
                raise RuntimeError('Repair stopped; previous installed mod was restored.') from failure
    print('Candidate bay panels installed in:', target)
    print('Full previous mod saved:', backup)
    print('No carrier-vessel configuration was generated or edited.')
    print('In Sea Power check closed panels, hidden stores, opening for release and reclosing.')
    print('The change and weapon release remain unverified in game.')
    print('Any previously prepared Workshop bundle is stale; select the patched local folder after testing.')
    return backup


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 fix-f111n-v9-bay-panels.py "/path/to/Sea Power/Sea Power_Data/StreamingAssets"', file=sys.stderr)
        raise SystemExit(2)
    try:
        install(sys.argv[1])
    except (OSError, RuntimeError, ValueError, UnicodeError) as exc:
        print('Repair stopped:', exc, file=sys.stderr)
        raise SystemExit(1)
