#!/usr/bin/env python3
"""Patch the V9.0 F-111N bay submodel registrations; no network required.

Usage: python3 fix-f111n-v9-bay-doors.py "/path/to/Sea Power"
The game must be closed. A complete copy of the installed mod is backed up.
"""
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

FAMILIES = ('f', 'fb', 'rf')
YEARS = ('', '_1985', '_1995', '_2003')
OLD = (b'bay_l=bay_l', b'bay_r=bay_r', b'pave_body=pave_body')
NEW = (b'General_12=bay_l', b'General_13=bay_r', b'General_14=pave_body')


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


def patch_aircraft(data, label):
    # Restrict edits to the unique [Submodels] section; leave every other byte untouched.
    sections = list(re.finditer(rb'(?mi)^\[Submodels\][ \t]*\r?$', data))
    if len(sections) != 1:
        raise ValueError(f'{label}: expected exactly one [Submodels] section')
    start = sections[0].end()
    following = re.search(rb'(?m)^\[', data[start:])
    end = start + following.start() if following else len(data)
    section = data[start:end]
    lines = section.splitlines()
    old_count = [lines.count(line) for line in OLD]
    new_count = [lines.count(line) for line in NEW]
    # Treat case/whitespace variants as conflicting keys rather than silently
    # producing an ambiguous INI with two definitions of the same key.
    for key in (b'bay_l', b'bay_r', b'pave_body'):
        count = len(re.findall(rb'(?mi)^[ \t]*' + key + rb'[ \t]*=', section))
        if count != lines.count(key + b'=' + key):
            raise ValueError(f'{label}: ambiguous {key.decode()} registration')
    if old_count == [0, 0, 0] and new_count == [1, 1, 1]:
        for num in (12, 13, 14):
            if len(re.findall(rb'(?mi)^\s*General_' + str(num).encode() + rb'\s*=', section)) != 1:
                raise ValueError(f'{label}: duplicate General_{num} entry')
        return data, False
    if old_count != [1, 1, 1] or new_count != [0, 0, 0]:
        raise ValueError(f'{label}: unrecognised or partially modified bay registration')
    # Refuse occupied slots and duplicate aliases, including altered whitespace/case.
    for num in (12, 13, 14):
        if re.search(rb'(?mi)^\s*General_' + str(num).encode() + rb'\s*=', section):
            raise ValueError(f'{label}: General_{num} is already occupied')
    for old, new in zip(OLD, NEW):
        section = re.sub(rb'(?m)^' + re.escape(old) + rb'(?=\r?$)', new, section, count=1)
    return data[:start] + section + data[end:], True


def install(game):
    game = Path(game).expanduser().resolve()
    if game_is_running():
        raise RuntimeError('Close Sea Power before applying the patch.')
    target = game / 'Sea Power_Data/StreamingAssets/user/RAN-F111N-Naval-Wing'
    if not target.is_dir() or target.is_symlink():
        raise RuntimeError(f'Installed Naval Wing folder not found: {target}')
    info = target / '_info.ini'
    if not info.is_file() or not re.search(r'^Name=RAN F-111N Naval Wing V9\.0(?:\s|$)', info.read_text(errors='replace'), re.M):
        raise RuntimeError('The installed mod is not the expected RAN F-111N Naval Wing V9.0.')
    modifications = {}
    for family in FAMILIES:
        for year in YEARS:
            relative = Path('aircraft') / f'ran_{family}-111n{year}.ini'
            path = target / relative
            if not path.is_file() or path.is_symlink():
                raise RuntimeError(f'Missing or unsafe aircraft file: {relative}')
            original = path.read_bytes()
            changed, needs_patch = patch_aircraft(original, str(relative))
            if needs_patch:
                modifications[relative] = (original, changed)
    if not modifications:
        print('Already patched; no changes made.')
        return None
    backup_root = game / 'RAN-F111N-backups'
    backup_root.mkdir(exist_ok=True)
    if os.stat(backup_root).st_dev != os.stat(target.parent).st_dev:
        raise RuntimeError('The backup and installed mod must be on the same filesystem; nothing changed.')
    backup_dir = Path(tempfile.mkdtemp(prefix='bay-doors-', dir=backup_root))
    stage_dir = Path(tempfile.mkdtemp(prefix='.ran-f111n-bay-stage-', dir=target.parent))
    staged = stage_dir / target.name
    backup = backup_dir / target.name
    moved = False
    try:
        shutil.copytree(target, staged, symlinks=True)
        for relative, (original, changed) in modifications.items():
            path = staged / relative
            if path.read_bytes() != original:
                raise RuntimeError(f'Aircraft changed during preparation: {relative}')
            path.write_bytes(changed)
        if game_is_running():
            raise RuntimeError('Sea Power started during preparation; nothing changed.')
        for relative, (original, _) in modifications.items():
            if (target / relative).read_bytes() != original:
                raise RuntimeError(f'Aircraft changed during preparation: {relative}')
        os.replace(target, backup)
        moved = True
        try:
            os.replace(staged, target)
        except Exception:
            os.replace(backup, target)
            moved = False
            raise
        print(f'Patched {len(modifications)} aircraft: {target}')
        print(f'Previous complete installation saved: {backup}')
        print('Restart Sea Power and test that MudPig bay doors close, open for release, then close again.')
        return backup
    finally:
        shutil.rmtree(stage_dir, ignore_errors=True)
        if not moved:
            shutil.rmtree(backup_dir, ignore_errors=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 fix-f111n-v9-bay-doors.py "/path/to/Sea Power"', file=sys.stderr)
        sys.exit(2)
    try:
        install(sys.argv[1])
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'Patch stopped: {exc}', file=sys.stderr)
        sys.exit(1)
