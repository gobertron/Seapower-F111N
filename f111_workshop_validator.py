#!/usr/bin/env python3
"""Check a Sea Power F-111N content root before selecting it for Workshop.

This checks folder layout and known unrelated SR-71 paths, not the contents or
correctness of every game configuration and model. It never edits any files.
"""
from pathlib import Path
import re
import sys

FAMILIES = ('f', 'fb', 'rf', 'ef')
YEARS = ('', '_1985', '_1995', '_2003')


def validate_workshop_root(root):
    root = Path(root).expanduser()
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f'Not a real folder: {root}')
    info = root / '_info.ini'
    if not info.is_file() or info.is_symlink():
        raise RuntimeError(f'Missing _info.ini at the selected folder root: {root}')
    try:
        metadata = info.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        raise RuntimeError(f'Cannot read root _info.ini: {exc}') from exc
    if not re.search(r'(?im)^\s*Name\s*=\s*RAN\s+F-111N\s+Naval\s+Wing\b', metadata):
        raise RuntimeError('Root _info.ini does not identify the RAN F-111N Naval Wing')
    for directory in ('aircraft', 'assets', 'systems', 'animations', 'ammunition', 'language_en'):
        path = root / directory
        if path.is_symlink() or not path.is_dir():
            raise RuntimeError(f'Missing real {directory}/ at the selected folder root')
    count = 0
    for family in FAMILIES:
        for year in YEARS:
            uid = f'ran_{family}-111n{year}'
            for suffix in ('', '_squadrons'):
                path = root / 'aircraft' / (uid + suffix + '.ini')
                if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
                    raise RuntimeError(f'Missing or empty aircraft definition: {path.relative_to(root)}')
            count += 1
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if path.is_symlink():
            raise RuntimeError(f'Symlink inside Workshop content: {relative}')
        if relative.name.lower() == '_info.ini' and len(relative.parts) > 1:
            raise RuntimeError(f'Nested mod or wrapper detected: {relative}')
        # Catch common path spellings: SR-71, SR_71, SR71 and Blackbird.
        for part in relative.parts:
            normal = re.sub(r'[^a-z0-9]', '', part.casefold())
            if 'sr71' in normal or 'blackbird' in normal:
                raise RuntimeError(f'Unrelated SR-71 content in F-111N package: {relative}')
    return {'root': str(root.resolve()), 'aircraft': count, 'status': 'PASS'}


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print('Usage: python3 f111_workshop_validator.py "/path/to/RAN-F111N-Naval-Wing"', file=sys.stderr)
        return 2
    try:
        result = validate_workshop_root(args[0])
    except (OSError, RuntimeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f"PASS: {result['aircraft']} F-111N aircraft in {result['root']}")
    print('Select this folder itself in Sea Power. This check does not upload the mod or test it in game.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
