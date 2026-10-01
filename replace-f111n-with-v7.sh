#!/usr/bin/env bash
# Standalone replacement for CachyOS/Linux; run from bash or fish.
# Close Sea Power, then run: bash replace-f111n-with-v7.sh
# Optional: bash replace-f111n-with-v7.sh "/full/path/to/Sea Power"
set -euo pipefail
if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' "Python 3 is required. On CachyOS: sudo pacman -S python"
    exit 1
fi
exec python3 - "$@" <<'V7_REPLACEMENT_PY'
"""Install verified V7 after backing up recognised older local Naval Wing folders."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import types
import urllib.error
import urllib.request
import zipfile

RELEASE_COMMIT = "3d00015b9d76788da746c32682e4c0cafa553479"
DOWNLOAD = "https://codeload.github.com/gobertron/Seapower-F111N/zip/" + RELEASE_COMMIT
MOD_NAME = "RAN-F111N-Naval-Wing"
MANIFEST_SHA256 = "5e8fed244755d2abc7b43a0de98eeb9817f259d280f5783b1cb787925840583b"
CARRIER_SHA256 = "aa8f4380a70d03929285ba8936ffae82c1cfc9c4a9f63a2995b07a8deb5b10ff"
LEGACY_CARRIER_SHA256 = "b86a83271be0b717a4ef79b8a923146b4a2cbd1835c9cb9e29a7a9b4371ed15f"
AIRCRAFT_IDS = ("ran_f-111n", "ran_fb-111n", "ran_rf-111n", "ran_ef-111n")
MAX_ARCHIVE_BYTES = 220 * 1024 * 1024
MAX_EXTRACTED_BYTES = 400 * 1024 * 1024


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def steam_libraries(home=None):
    home = Path.home() if home is None else Path(home)
    libraries = set()
    roots = [
        home / ".local/share/Steam", home / ".steam/steam", home / ".steam/root",
        home / ".var/app/com.valvesoftware.Steam/.local/share/Steam",
    ]
    for root in roots:
        if root.is_dir():
            libraries.add(root.resolve())
        vdf = root / "steamapps/libraryfolders.vdf"
        if vdf.is_file():
            text = vdf.read_text(errors="replace")
            paths = re.findall(r'"path"\s+"([^"]+)"', text)
            paths += re.findall(r'"\d+"\s+"([^"]+)"', text)
            for value in paths:
                path = Path(value.replace("\\\\", "\\")).expanduser()
                if path.is_absolute() and path.is_dir():
                    libraries.add(path.resolve())
    return sorted(libraries)


def discover_games(home=None):
    games = set()
    for library in steam_libraries(home):
        common = library / "steamapps/common"
        candidates = [common / "Sea Power"]
        manifest = library / "steamapps/appmanifest_1286220.acf"
        if manifest.is_file():
            match = re.search(
                r'"installdir"\s+"([^"]+)"', manifest.read_text(errors="replace")
            )
            if match:
                candidates.append(common / match.group(1))
        for game in candidates:
            if (game / "Sea Power_Data/StreamingAssets").is_dir():
                games.add(game.resolve())
    return sorted(games)


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
            normal = re.sub(r"[\s_-]", "", name).casefold()
            if normal in {"seapower.exe", "seapower.x86_64"}:
                return True
            if index == 0 and normal == "seapower":
                return True
    return False


def own_mod(folder):
    """Require our aircraft IDs and a matching folder or mod title."""
    if not folder.is_dir():
        return False
    aircraft = folder / "aircraft"
    if not aircraft.is_dir():
        return False
    ids = {p.stem.casefold() for p in aircraft.glob("*.ini") if p.is_file()}
    if not any(unit in ids for unit in AIRCRAFT_IDS):
        return False
    name = re.sub(r"[^a-z0-9]", "", folder.name.casefold())
    known_folder = bool(re.fullmatch(r"ranf111nnavalwing(?:v[0-9]+)*", name))
    info = folder / "_info.ini"
    title = ""
    if info.is_file():
        match = re.search(r"(?mi)^\s*Name\s*=(.*)$", info.read_text(errors="replace"))
        if match:
            title = re.sub(r"[^a-z0-9]", "", match.group(1).casefold())
    return known_folder or "ranf111nnavalwing" in title or "ranraaff111nseries" in title


def local_predecessors(streaming):
    result = []
    for base in (streaming, streaming / "user"):
        if not base.is_dir():
            continue
        for folder in sorted(base.iterdir()):
            if folder.name in {"original", "user"}:
                continue
            if own_mod(folder):
                if folder.is_symlink():
                    raise RuntimeError("Old mod is a symlink; leaving it unchanged: " + str(folder))
                result.append(folder)
    return result


def check_target(streaming):
    target = streaming / "user" / MOD_NAME
    if target.is_symlink():
        raise RuntimeError("The destination is a symlink; leaving it unchanged: " + str(target))
    existing = local_predecessors(streaming)
    if target.exists() and target not in existing:
        raise RuntimeError("Destination contains unrecognised files; leaving it unchanged: " + str(target))
    return target, existing


def fetch_archive(path):
    request = urllib.request.Request(DOWNLOAD, headers={"User-Agent": "RAN-F111N-V7-installer"})
    print("Downloading verified V7 from GitHub...", flush=True)
    with urllib.request.urlopen(request, timeout=45) as response, path.open("wb") as output:
        size = last_notice = 0
        while True:
            data = response.read(1024 * 1024)
            if not data:
                break
            size += len(data)
            if size > MAX_ARCHIVE_BYTES:
                raise RuntimeError("The download exceeds the expected V7 archive size.")
            output.write(data)
            if size - last_notice >= 20 * 1024 * 1024:
                print("  Downloaded", size // (1024 * 1024), "MiB", flush=True)
                last_notice = size


def extract_archive(archive, destination):
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if len(members) > 3000 or sum(m.file_size for m in members) > MAX_EXTRACTED_BYTES:
            raise RuntimeError("Archive size or file count is outside the V7 limits.")
        seen = set()
        for member in members:
            path = PurePosixPath(member.filename)
            if (
                path.is_absolute() or ".." in path.parts or "\\" in member.filename
                or stat.S_ISLNK(member.external_attr >> 16) or member.filename in seen
            ):
                raise RuntimeError("Unsafe archive entry: " + member.filename)
            seen.add(member.filename)
        # A CRC failure stops preparation before any installed mod is moved.
        bundle.extractall(destination)


def package_root(folder):
    folder = folder.resolve()
    if (folder / MOD_NAME).is_dir() and (folder / "MOD_SHA256.txt").is_file():
        return folder
    candidates = [
        p for p in folder.iterdir()
        if p.is_dir() and (p / MOD_NAME).is_dir() and (p / "MOD_SHA256.txt").is_file()
    ]
    if len(candidates) != 1:
        raise RuntimeError("Cannot find the complete V7 package. Use the full ZIP or extracted package.")
    return candidates[0]


def verify_package(package):
    manifest = package / "MOD_SHA256.txt"
    carrier = package / "carrier_compatibility.py"
    if not manifest.is_file() or digest(manifest) != MANIFEST_SHA256:
        raise RuntimeError("Package is not the corrected V7 release: manifest checksum failed. Use a current GitHub ZIP or run without --package.")
    if not carrier.is_file() or digest(carrier) not in {CARRIER_SHA256, LEGACY_CARRIER_SHA256}:
        raise RuntimeError("The package's carrier installer checksum failed.")
    entries = []
    for line in manifest.read_text().splitlines():
        checksum, name = line.split("  ", 1)
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError("Invalid manifest path: " + name)
        entries.append((checksum, name))
    source = package / MOD_NAME
    expected = {name for _, name in entries}
    actual = set()
    for path in source.rglob("*"):
        if path.is_symlink():
            raise RuntimeError("A package file is a symlink: " + str(path))
        if path.is_file():
            actual.add(path.relative_to(source).as_posix())
    if actual != expected or len(entries) != 174:
        raise RuntimeError("Corrected V7 must contain exactly the 174 verified game files.")
    for checksum, name in entries:
        if digest(source / name) != checksum:
            raise RuntimeError("V7 game-file checksum failed: " + name)
    print("Verified all 174 corrected V7 game files and the carrier installer.", flush=True)
    return entries


def read_source_text(path):
    raw = Path(path).read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            return raw.decode("cp1252")
        except UnicodeDecodeError:
            return raw.decode("latin-1")


def carrier_overrides(package, game, staged, sources):
    helper = package / "carrier_compatibility.py"
    checksum = digest(helper)
    if checksum not in {CARRIER_SHA256, LEGACY_CARRIER_SHA256}:
        raise RuntimeError("Carrier installer changed after verification.")
    code = helper.read_text(encoding="utf-8")
    if checksum == LEGACY_CARRIER_SHA256:
        # Apply the encoding fix in memory to the original, checksum-verified
        # V7 helper. This also supports the user's already-downloaded V7 ZIP.
        old_reader = "text=p.read_text(encoding='utf-8-sig')"
        if code.count(old_reader) != 1:
            raise RuntimeError("Cannot apply the verified V7 carrier encoding fix.")
        code = code.replace(old_reader, "text=read_source_text(p)", 1)
    module = types.ModuleType("v7_carrier_compatibility")
    module.__file__ = str(helper)
    exec(compile(code, str(helper), "exec"), module.__dict__)
    module.read_source_text = read_source_text
    report = module.generate(game, staged, sources)
    if report["errors"]:
        details = "; ".join(item["file"] + ": " + item["reason"] for item in report["errors"])
        raise RuntimeError("Carrier preparation failed; old installation kept intact. " + details)
    return report


def install(package, game, sources=(), dry_run=False):
    streaming = game / "Sea Power_Data/StreamingAssets"
    target, existing = check_target(streaming)
    entries = verify_package(package)
    source = package / MOD_NAME
    if source.resolve() == target.resolve() or any(source.is_relative_to(p.resolve()) for p in existing):
        raise RuntimeError("Use a downloaded package outside the installed mod folders.")
    print("Sea Power:", game)
    print("Destination:", target)
    for old in existing:
        print("Replace old local copy:", old)
    if dry_run:
        with tempfile.TemporaryDirectory(prefix="ran-f111n-v7-check-") as temporary:
            staged = Path(temporary) / MOD_NAME
            shutil.copytree(source, staged)
            report = carrier_overrides(package, game, staged, sources)
        print("DRY RUN OK:", len(report["carriers"]), "carrier definitions prepared.")
        print("No installed game or mod files were changed.")
        return None
    if game_is_running():
        raise RuntimeError("Close Sea Power before replacing the mod.")
    required = sum((source / name).stat().st_size for _, name in entries) + 10 * 1024 * 1024
    if shutil.disk_usage(game).free < required:
        raise RuntimeError("Not enough free space to stage V7 before replacing the old mod.")
    backup_parent = game / "RAN-F111N-backups"
    backup_parent.mkdir(exist_ok=True)
    with (backup_parent / ".replacement.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another F-111N replacement is already running.")
        target, existing = check_target(streaming)
        target.parent.mkdir(parents=True, exist_ok=True)
        device = game.stat().st_dev
        if target.parent.stat().st_dev != device or any(p.stat().st_dev != device for p in existing):
            raise RuntimeError("Mod and backup directories must share a filesystem for safe replacement.")
        with tempfile.TemporaryDirectory(prefix="ran-f111n-v7-stage-", dir=game) as temporary:
            staged = Path(temporary) / MOD_NAME
            shutil.copytree(source, staged)
            for checksum, name in entries:
                if digest(staged / name) != checksum:
                    raise RuntimeError("Staged V7 checksum failed: " + name)
            report = carrier_overrides(package, game, staged, sources)
            if game_is_running():
                raise RuntimeError("Sea Power started during preparation. Close it and run again.")
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup = backup_parent / stamp
            backup.mkdir()
            record = {
                "release_commit": RELEASE_COMMIT, "status": "replacing",
                "installed": str(target), "previous_local_folders": [
                    {"original": str(p), "backup": str(backup / p.relative_to(streaming))}
                    for p in existing
                ],
            }
            record_path = backup / "replacement.json"
            record_path.write_text(json.dumps(record, indent=2) + "\n")
            moved = []
            installed = False
            try:
                for old in existing:
                    saved = backup / old.relative_to(streaming)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    old.rename(saved)
                    moved.append((old, saved))
                staged.rename(target)
                installed = True
                record["status"] = "installed"
                record_path.write_text(json.dumps(record, indent=2) + "\n")
            except BaseException as failure:
                recovery_errors = []
                if installed:
                    try:
                        shutil.rmtree(target)
                    except OSError as error:
                        recovery_errors.append(str(error))
                for old, saved in reversed(moved):
                    try:
                        saved.rename(old)
                    except OSError as error:
                        recovery_errors.append(str(error))
                record["status"] = "rollback_failed" if recovery_errors else "rolled_back"
                record["error"] = str(failure)
                record["recovery_errors"] = recovery_errors
                try:
                    record_path.write_text(json.dumps(record, indent=2) + "\n")
                except OSError:
                    pass
                if recovery_errors:
                    raise RuntimeError(
                        "Replacement stopped; manual recovery is needed from " + str(backup)
                        + ": " + "; ".join(recovery_errors)
                    ) from failure
                raise RuntimeError("Replacement stopped; previous local folders were restored.") from failure
    print("\nV7 INSTALLED:", target)
    print("Dated backup and replacement record:", backup)
    print("Carrier definitions prepared:", len(report["carriers"]))
    print("\nOpen Sea Power Mod Manager: enable RAN F-111N Naval Wing V7.")
    print("Disable older Naval Wing copies. Give V7 priority over carrier mods.")
    print("Keep carrier/source asset mods and your existing Anchor Chain setup enabled.")
    print("Restart Sea Power after changing the mod list.")
    print("\nFor your existing Workshop item 3810606011, use Update Existing,")
    print("then Pick Folder: \\user\\RAN-F111N-Naval-Wing")
    print("Local folder update is complete; submit the Workshop update separately.")
    return backup


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Replace older local RAN F-111N folders with verified V7, keeping dated backups."
    )
    parser.add_argument("game", nargs="?", help="Sea Power installation folder (auto-detected if omitted)")
    parser.add_argument("--package", type=Path, help="complete local V7 ZIP or extracted folder instead of downloading")
    parser.add_argument("--carrier-source", action="append", default=[], help="preferred carrier-mod folder; may be repeated")
    parser.add_argument("--dry-run", action="store_true", help="verify and preview without changing installed mod files")
    args = parser.parse_args(argv)
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        raise RuntimeError("Run this as your normal Steam user, without sudo.")
    if game_is_running() and not args.dry_run:
        raise RuntimeError("Close Sea Power, then run this script again.")
    games = [Path(args.game).expanduser().resolve()] if args.game else discover_games()
    if len(games) != 1:
        print("Specify the Sea Power installation you want to update:")
        for candidate in games:
            print(" ", candidate)
        if not games:
            print("No installation was found in your Steam library configuration.")
        print('Usage: bash replace-f111n-with-v7.sh "/full/path/to/steamapps/common/Sea Power"')
        return 2
    game = games[0]
    if not (game / "Sea Power_Data/StreamingAssets").is_dir():
        raise RuntimeError("This is not a Sea Power installation: " + str(game))
    check_target(game / "Sea Power_Data/StreamingAssets")
    sources = [Path(p).expanduser().resolve() for p in args.carrier_source]
    for source in sources:
        if not (source / "vessels").is_dir():
            raise RuntimeError("Carrier source has no vessels folder: " + str(source))
    with tempfile.TemporaryDirectory(prefix="ran-f111n-v7-download-") as temporary:
        temporary = Path(temporary)
        if args.package:
            supplied = args.package.expanduser().resolve()
            if supplied.is_dir():
                package = package_root(supplied)
            elif supplied.is_file():
                unpacked = temporary / "extracted"
                extract_archive(supplied, unpacked)
                package = package_root(unpacked)
            else:
                raise RuntimeError("Local package does not exist: " + str(supplied))
        else:
            archive = temporary / "V7.zip"
            fetch_archive(archive)
            unpacked = temporary / "extracted"
            extract_archive(archive, unpacked)
            package = package_root(unpacked)
        install(package, game, sources, args.dry_run)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped by user.", file=sys.stderr)
        raise SystemExit(130)
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as error:
        print("Replacement stopped:", error, file=sys.stderr)
        print("For a download failure, use --package with the complete V7 ZIP.", file=sys.stderr)
        raise SystemExit(1)
V7_REPLACEMENT_PY
