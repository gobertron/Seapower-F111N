#!/usr/bin/env python3
"""Reversibly remove the V9 Naval Wing's carrier overrides.

Usage: python3 fix-f111n-v9-carrier-overrides.py "/path/to/Sea Power/Sea Power_Data/StreamingAssets"
Close Sea Power first. Original carrier mods and aircraft are not edited.
"""
import fcntl
import os
from pathlib import Path
import re
import sys
import tempfile

MOD_NAME = "RAN-F111N-Naval-Wing"


def game_is_running():
    proc = Path("/proc")
    if not proc.is_dir():
        return False
    for process in proc.iterdir():
        if not process.name.isdigit():
            continue
        try:
            command = (process / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        for index, value in enumerate(command):
            name = value.decode(errors="replace").replace("\\", "/").rsplit("/", 1)[-1]
            name = re.sub(r"[\s_-]", "", name).casefold()
            if name in {"seapower.exe", "seapower.x86_64"} or (index == 0 and name == "seapower"):
                return True
    return False


def resolve_paths(path):
    selected = Path(path).expanduser().resolve()
    if selected.name == "StreamingAssets" and selected.parent.name == "Sea Power_Data":
        streaming, game = selected, selected.parent.parent
    else:
        game, streaming = selected, selected / "Sea Power_Data" / "StreamingAssets"
    if not (streaming / "original").is_dir():
        raise RuntimeError("Sea Power's StreamingAssets/original folder was not found: " + str(streaming))
    return game, streaming


def validate_mod(streaming):
    target = streaming / MOD_NAME
    if target.is_symlink() or not target.is_dir():
        raise RuntimeError("The installed Naval Wing folder was not found or is a symlink: " + str(target))
    info = target / "_info.ini"
    if info.is_symlink() or not info.is_file():
        raise RuntimeError("The installed mod does not have a safe _info.ini: " + str(target))
    metadata = info.read_text(encoding="utf-8-sig")
    if not re.search(r"(?im)^\s*Name\s*=\s*RAN\s+F-111N\s+Naval\s+Wing\s+V9\.0(?:\s|$)", metadata):
        raise RuntimeError("The selected folder is not the expected RAN F-111N Naval Wing V9.0.")
    for family in ("f", "fb", "rf", "ef"):
        for edition in ("", "_1985", "_1995", "_2003"):
            path = target / "aircraft" / f"ran_{family}-111n{edition}.ini"
            if not path.is_file() or path.is_symlink():
                raise RuntimeError("Expected Naval Wing aircraft definition not found: " + str(path))
    return target


def install(path):
    game, streaming = resolve_paths(path)
    if game_is_running():
        raise RuntimeError("Close Sea Power before running this repair.")
    target = validate_mod(streaming)
    vessels = target / "vessels"
    if vessels.is_symlink():
        raise RuntimeError("The Naval Wing vessels folder is a symlink; nothing changed.")
    if not vessels.exists():
        print("No Naval Wing carrier override folder found; no files changed.")
        print("Check for other enabled F-111N copies, including the Steam Workshop copy.")
        return None
    if not vessels.is_dir():
        raise RuntimeError("The Naval Wing vessels path is not a directory; nothing changed.")
    backup_root = game / "RAN-F111N-backups"
    if backup_root.is_symlink():
        raise RuntimeError("Backup folder is a symlink; nothing changed.")
    backup_root.mkdir(exist_ok=True)
    if backup_root.stat().st_dev != vessels.stat().st_dev:
        raise RuntimeError("The mod and backup must be on the same filesystem; nothing changed.")
    with (backup_root / ".carrier-repair.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another carrier repair is already running.")
        if game_is_running():
            raise RuntimeError("Sea Power started during preparation; nothing changed.")
        validate_mod(streaming)
        if vessels.is_symlink() or not vessels.is_dir():
            raise RuntimeError("The vessels folder changed during preparation; nothing changed.")
        backup = Path(tempfile.mkdtemp(prefix="carrier-overrides-", dir=backup_root))
        try:
            vessels.rename(backup / "vessels")
        except BaseException as failure:
            saved = backup / "vessels"
            if saved.exists() and not vessels.exists():
                try:
                    saved.rename(vessels)
                except OSError as error:
                    raise RuntimeError("Repair interrupted; restore the carrier overrides from " + str(saved) + ": " + str(error)) from failure
            try:
                backup.rmdir()
            except OSError:
                pass
            raise
    print("Carrier overrides moved out of the F-111N mod.")
    print("Backup:", backup / "vessels")
    print("Aircraft, original carrier mods and game files were not edited.")
    print("Restart Sea Power. Enable the local Naval Wing, and disable any older or Workshop F-111N copies while testing.")
    print("Check carrier visuals and adding a normal air group. F-111N carrier use still needs in-game testing.")
    print("Previously prepared Workshop packages still contain the old overrides. Do not upload them; update from the repaired local mod folder.")
    return backup


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python3 fix-f111n-v9-carrier-overrides.py "/path/to/Sea Power/Sea Power_Data/StreamingAssets"', file=sys.stderr)
        sys.exit(2)
    try:
        install(sys.argv[1])
    except (OSError, RuntimeError, UnicodeError) as exc:
        print("Repair stopped:", exc, file=sys.stderr)
        sys.exit(1)
