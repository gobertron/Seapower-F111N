#!/usr/bin/env bash
# Standalone replacement and Workshop preparation for CachyOS/Linux.
# Close Sea Power, then run: bash replace-f111n-with-v8.sh
# Optional: bash replace-f111n-with-v8.sh "/full/path/to/Sea Power"
# Optional SteamCMD upload: append --upload (Steam handles login itself).
set -euo pipefail
if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' "Python 3 is required. On CachyOS: sudo pacman -S python"
    exit 1
fi
exec python3 - "$@" <<'V8_REPLACEMENT_PY'
"""Install verified V8 after backing up recognised older local Naval Wing folders."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import types
import urllib.error
import urllib.request
import zipfile

RELEASE_COMMIT = "c4d10030046d72e66e48df06777e44ae1e853a13"
DOWNLOAD = "https://codeload.github.com/gobertron/Seapower-F111N/zip/" + RELEASE_COMMIT
MOD_NAME = "RAN-F111N-Naval-Wing"
MANIFEST_SHA256 = "1585a6d503949c520a9662e90d74e4070a5e7cdc645d7d7a644d3c8e380923bd"
CARRIER_SHA256 = "7ab5f7acffbae0c6a1b7abf73d6673ce0c4ca70f9db91bbfdc214b12badd7c41"
AIRCRAFT_IDS = ("ran_f-111n", "ran_fb-111n", "ran_rf-111n", "ran_ef-111n")
MAX_ARCHIVE_BYTES = 220 * 1024 * 1024
MAX_EXTRACTED_BYTES = 400 * 1024 * 1024
WORKSHOP_ID = "3810606011"
APP_ID = "1286220"
RELEASE_VERSION = "V8"
WORKSHOP_TITLE = "RAN F-111N Naval Wing V8"
WORKSHOP_ASSETS = {
    "RAN-F111N-preview.png": "9ba4795b87f7c18958a93af7f89458de23e9096e38a1b69334b96c9b1a4fc752",
    "WORKSHOP_DESCRIPTION.txt": "7bb1643466b69f2340d7fa44a2eb6a01c501d67e3e2ca3210bbae889d7b1ae46",
    "WORKSHOP_UPDATE_NOTES_V8.txt": "852b12323c9d26cf7103ea163948819271d17e5e81ebbb3f56216da565b6288a",
}
UPLOAD_NOTE = (
    "V8: 16 aircraft across 1980, 1985, 1995 and 2003; 167 loadouts; "
    "progressive systems upgrades and late tactical-grey liveries. "
    "Corrected weapon names, zero-reload chaff and repaired carrier lift routes."
)


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
    request = urllib.request.Request(DOWNLOAD, headers={"User-Agent": "RAN-F111N-V8-installer"})
    print("Downloading verified V8 from GitHub...", flush=True)
    with urllib.request.urlopen(request, timeout=45) as response, path.open("wb") as output:
        size = last_notice = 0
        while True:
            data = response.read(1024 * 1024)
            if not data:
                break
            size += len(data)
            if size > MAX_ARCHIVE_BYTES:
                raise RuntimeError("The download exceeds the expected V8 archive size.")
            output.write(data)
            if size - last_notice >= 20 * 1024 * 1024:
                print("  Downloaded", size // (1024 * 1024), "MiB", flush=True)
                last_notice = size


def extract_archive(archive, destination):
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if len(members) > 3000 or sum(m.file_size for m in members) > MAX_EXTRACTED_BYTES:
            raise RuntimeError("Archive size or file count is outside the V8 limits.")
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
        raise RuntimeError("Cannot find the complete V8 package. Use the full ZIP or extracted package.")
    return candidates[0]


def verify_package(package):
    manifest = package / "MOD_SHA256.txt"
    carrier = package / "carrier_compatibility.py"
    if not manifest.is_file() or digest(manifest) != MANIFEST_SHA256:
        raise RuntimeError("Package is not the corrected V8 release: manifest checksum failed. Use a current GitHub ZIP or run without --package.")
    if not carrier.is_file() or digest(carrier) != CARRIER_SHA256:
        raise RuntimeError("The package's carrier installer checksum failed. Run without --package to download V8 with the elevator repair.")
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
        raise RuntimeError("Corrected V8 must contain exactly the 174 verified game files.")
    for checksum, name in entries:
        if digest(source / name) != checksum:
            raise RuntimeError("V8 game-file checksum failed: " + name)
    print("Verified all 174 corrected V8 game files and the carrier installer.", flush=True)
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


def verify_workshop_assets(package):
    for name, checksum in WORKSHOP_ASSETS.items():
        path = package / name
        if not path.is_file() or path.is_symlink() or digest(path) != checksum:
            raise RuntimeError("Workshop asset checksum failed: " + name + ". Run without --package for the complete release.")
    preview = package / "RAN-F111N-preview.png"
    if preview.stat().st_size >= 1024 * 1024 or not preview.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Workshop preview must be a PNG smaller than 1 MiB.")


def vdf_quote(value):
    value = str(value)
    if any(ord(char) < 32 for char in value):
        raise RuntimeError("Workshop configuration contains a control character.")
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def workshop_vdf(bundle, description=None):
    if description is None:
        description = (bundle / "description.txt").read_text(encoding="utf-8")
    # BBCode headings/lists retain their structure in a single VDF string.
    # Preserve visibility while updating the title and description to this version.
    description = " ".join(description.split())
    fields = [
        ("appid", APP_ID), ("publishedfileid", WORKSHOP_ID),
        ("contentfolder", bundle / "content"), ("previewfile", bundle / "preview.png"),
        ("title", WORKSHOP_TITLE), ("description", description),
        ("changenote", UPLOAD_NOTE),
    ]
    return '"workshopitem"\n{\n' + "".join(
        "    " + vdf_quote(key) + " " + vdf_quote(value) + "\n" for key, value in fields
    ) + "}\n"


def prepare_workshop(package, mod, staged_bundle, final_bundle, report):
    """Create a flat native payload and metadata outside the game's mod scan."""
    verify_workshop_assets(package)
    portable = json.loads(json.dumps(report))
    for item in portable.get("carriers", []):
        source = item.pop("source", "")
        if source:
            item["source_label"] = "/".join(Path(source).parts[-3:])
        item.pop("other_source_candidates", None)
    # Keep personal absolute paths only in the local bundle, outside contentfolder.
    (mod / "CARRIER_COMPATIBILITY.json").write_text(json.dumps(portable, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(package / "RAN-F111N-preview.png", mod / "preview.png")
    staged_bundle.mkdir()
    shutil.copytree(mod, staged_bundle / "content")
    for source in mod.rglob("*"):
        if source.is_file() and digest(source) != digest(staged_bundle / "content" / source.relative_to(mod)):
            raise RuntimeError("Workshop payload copy failed verification: " + source.relative_to(mod).as_posix())
    for source, destination in [
        ("RAN-F111N-preview.png", "preview.png"),
        ("WORKSHOP_DESCRIPTION.txt", "description.txt"),
        ("WORKSHOP_UPDATE_NOTES_V8.txt", "update-notes.txt"),
    ]:
        shutil.copy2(package / source, staged_bundle / destination)
    (staged_bundle / "carrier-report.local.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (staged_bundle / "upload.vdf").write_text(workshop_vdf(final_bundle, (staged_bundle / "description.txt").read_text(encoding="utf-8")), encoding="utf-8")
    paths = list((staged_bundle / "content").rglob("*")) + [
        staged_bundle / name for name in ("preview.png", "description.txt", "update-notes.txt", "upload.vdf")
    ]
    manifest = {
        "appid": APP_ID, "publishedfileid": WORKSHOP_ID, "release_commit": RELEASE_COMMIT, "version": RELEASE_VERSION,
        "files": {p.relative_to(staged_bundle).as_posix(): digest(p) for p in sorted(paths) if p.is_file()},
    }
    (staged_bundle / "workshop-sha256.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    instructions = (
        "V8 is installed and this Workshop payload is ready. It has not been uploaded.\n\n"
        "IN-GAME UPLOAD\n"
        "Launch Sea Power with Steam. Mod Manager > Upload Mod > Update Existing.\n"
        "Select your existing item " + WORKSHOP_ID + ".\n"
        "Pick Folder: \\user\\RAN-F111N-Naval-Wing\n"
        "Pick Image: \\user\\RAN-F111N-Naval-Wing\\preview.png\n"
        "Paste description.txt into Mod Description and update-notes.txt into Change Log.\n"
        "Submit the update while signed into the Steam account that owns the item.\n\n"
        "OPTIONAL TERMINAL UPLOAD\n"
        "With SteamCMD installed, run:\n"
        "bash ~/Downloads/replace-f111n-with-v8.sh --upload-prepared " + shlex.quote(str(final_bundle)) + "\n"
        "Enter your Steam account name when prompted. SteamCMD handles password and Steam Guard.\n"
        "No password or API key is stored by this script.\n"
        "SteamCMD sends content/ and preview.png, and updates the title and description to Version 8. Visibility is preserved.\n"
        "The complete description and notes above are supplied for the in-game uploader.\n\n"
        "Enable V8, disable older Naval Wing copies, give V8 priority over carrier mods,\n"
        "and retain carrier/source mods and Anchor Chain. Restart after mod-list changes.\n"
        "Carrier overrides still rely on their original carrier mods for those models/assets.\n"
        "Flight behaviour and landings remain untested in Sea Power.\n"
    )
    (staged_bundle / "UPLOAD_INSTRUCTIONS.txt").write_text(instructions, encoding="utf-8")
    verify_workshop_bundle(staged_bundle, expected_location=final_bundle)
    return manifest


def verify_workshop_bundle(bundle, expected_location=None):
    bundle = Path(bundle).expanduser().resolve()
    marker = bundle / "workshop-sha256.json"
    if not marker.is_file() or marker.is_symlink():
        raise RuntimeError("Not a prepared V8 Workshop bundle: " + str(bundle))
    manifest = json.loads(marker.read_text(encoding="utf-8"))
    if (manifest.get("appid"), manifest.get("publishedfileid"), manifest.get("release_commit"), manifest.get("version")) != (APP_ID, WORKSHOP_ID, RELEASE_COMMIT, RELEASE_VERSION):
        raise RuntimeError("This bundle does not target the existing Sea Power Workshop item " + WORKSHOP_ID)
    expected = manifest.get("files", {})
    actual = set()
    for path in (bundle / "content").rglob("*"):
        if path.is_symlink():
            raise RuntimeError("Workshop content contains a symlink: " + str(path))
        if path.is_file():
            actual.add(path.relative_to(bundle).as_posix())
    if actual != {name for name in expected if name.startswith("content/")} or "content/_info.ini" not in actual:
        raise RuntimeError("Prepared Workshop content has changed; run the replacement script again.")
    for name, checksum in expected.items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            raise RuntimeError("Unsafe Workshop manifest path: " + name)
        path = bundle / name
        if path.is_symlink() or not path.is_file() or digest(path) != checksum:
            raise RuntimeError("Prepared Workshop checksum failed: " + name)
    if (bundle / "upload.vdf").read_text(encoding="utf-8") != workshop_vdf(expected_location or bundle, (bundle / "description.txt").read_text(encoding="utf-8")):
        raise RuntimeError("Workshop upload configuration was changed or moved; prepare it again.")
    return bundle


def find_steamcmd(supplied=None):
    if supplied:
        path = Path(supplied).expanduser().resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise RuntimeError("SteamCMD executable was not found: " + str(path))
        return str(path)
    found = shutil.which("steamcmd") or shutil.which("steamcmd.sh")
    if found:
        return found
    for path in (Path.home() / "steamcmd/steamcmd.sh", Path.home() / ".local/share/SteamCMD/steamcmd.sh"):
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    raise RuntimeError(
        "SteamCMD is not installed or not on PATH. Your prepared folder can be uploaded "
        "with Sea Power's Mod Manager; see UPLOAD_INSTRUCTIONS.txt. "
        "Or install Valve's SteamCMD and use --steamcmd /path/to/steamcmd.sh."
    )


def upload_workshop(bundle, username=None, executable=None):
    bundle = verify_workshop_bundle(bundle)
    executable = find_steamcmd(executable)
    if username is None:
        if not sys.stdin.isatty():
            raise RuntimeError("Run from a terminal or supply --steam-user with the item owner's Steam account name.")
        username = input("Steam account name that owns item " + WORKSHOP_ID + ": ").strip()
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.@-]{0,63}", username):
        raise RuntimeError("Invalid Steam account name. Supply the login name, without a password.")
    print("Uploading V8 to existing Workshop item " + WORKSHOP_ID + ".", flush=True)
    print("SteamCMD will handle password and Steam Guard prompts directly.", flush=True)
    command = [executable, "+login", username, "+workshop_build_item", vdf_quote(bundle / "upload.vdf"), "+quit"]
    output = bytearray()
    # Keep stdin attached to the user's terminal. Do not save a login transcript.
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        try:
            while True:
                chunk = os.read(process.stdout.fileno(), 4096)
                if not chunk:
                    break
                sys.stdout.write(chunk.decode("utf-8", errors="replace"))
                sys.stdout.flush()
                output.extend(chunk)
                if len(output) > 4 * 1024 * 1024:
                    del output[:-4 * 1024 * 1024]
            status = process.wait()
        except BaseException:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            raise
    text = output.decode("utf-8", errors="replace")
    success = re.search(r"Success\.\s+Published item\s+" + WORKSHOP_ID + r"\b", text, re.I)
    if status != 0 or not success:
        raise RuntimeError(
            "SteamCMD did not confirm a successful update of item " + WORKSHOP_ID
            + ". The installed V8 and prepared payload remain available at " + str(bundle)
            + ". Retry with the owning account or use Sea Power's in-game uploader."
        )
    print("STEAM WORKSHOP UPDATED: https://steamcommunity.com/sharedfiles/filedetails/?id=" + WORKSHOP_ID)


def carrier_overrides(package, game, staged, sources):
    helper = package / "carrier_compatibility.py"
    checksum = digest(helper)
    if checksum != CARRIER_SHA256:
        raise RuntimeError("Carrier installer changed after verification.")
    code = helper.read_text(encoding="utf-8")
    module = types.ModuleType("v8_carrier_compatibility")
    module.__file__ = str(helper)
    exec(compile(code, str(helper), "exec"), module.__dict__)
    module.read_source_text = read_source_text
    report = module.generate(game, staged, sources)
    if report["errors"]:
        details = "; ".join(item.get("source", item["file"]) + ": " + item["reason"] for item in report["errors"])
        raise RuntimeError("Carrier preparation failed; old installation kept intact. " + details)
    return report


def install(package, game, sources=(), dry_run=False, prepare_upload=False):
    streaming = game / "Sea Power_Data/StreamingAssets"
    target, existing = check_target(streaming)
    entries = verify_package(package)
    if prepare_upload:
        verify_workshop_assets(package)
    source = package / MOD_NAME
    if source.resolve() == target.resolve() or any(source.is_relative_to(p.resolve()) for p in existing):
        raise RuntimeError("Use a downloaded package outside the installed mod folders.")
    print("Sea Power:", game)
    print("Destination:", target)
    for old in existing:
        print("Replace old local copy:", old)
    if dry_run:
        with tempfile.TemporaryDirectory(prefix="ran-f111n-v8-check-") as temporary:
            staged = Path(temporary) / MOD_NAME
            shutil.copytree(source, staged)
            report = carrier_overrides(package, game, staged, sources)
            if prepare_upload:
                prepare_workshop(package, staged, Path(temporary) / "workshop", game / "RAN-F111N-workshop" / WORKSHOP_ID / "dry-run", report)
        print("DRY RUN OK:", len(report["carriers"]), "carrier definitions prepared.")
        print("No installed game or mod files were changed.")
        return None
    if game_is_running():
        raise RuntimeError("Close Sea Power before replacing the mod.")
    required = sum((source / name).stat().st_size for _, name in entries) * (2 if prepare_upload else 1) + 20 * 1024 * 1024
    if shutil.disk_usage(game).free < required:
        raise RuntimeError("Not enough free space to stage V8 before replacing the old mod.")
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
        with tempfile.TemporaryDirectory(prefix="ran-f111n-v8-stage-", dir=game) as temporary:
            staged = Path(temporary) / MOD_NAME
            shutil.copytree(source, staged)
            for checksum, name in entries:
                if digest(staged / name) != checksum:
                    raise RuntimeError("Staged V8 checksum failed: " + name)
            report = carrier_overrides(package, game, staged, sources)
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            workshop_bundle = game / "RAN-F111N-workshop" / WORKSHOP_ID / stamp if prepare_upload else None
            if prepare_upload:
                prepare_workshop(package, staged, Path(temporary) / "workshop", workshop_bundle, report)
                workshop_bundle.parent.mkdir(parents=True, exist_ok=True)
            if game_is_running():
                raise RuntimeError("Sea Power started during preparation. Close it and run again.")
            backup = backup_parent / stamp
            backup.mkdir()
            record = {
                "release_commit": RELEASE_COMMIT, "version": RELEASE_VERSION, "status": "replacing",
                "installed": str(target), "previous_local_folders": [
                    {"original": str(p), "backup": str(backup / p.relative_to(streaming))}
                    for p in existing
                ],
            }
            if prepare_upload:
                record["workshop_bundle"] = str(workshop_bundle)
            record_path = backup / "replacement.json"
            record_path.write_text(json.dumps(record, indent=2) + "\n")
            moved = []
            installed = False
            workshop_saved = False
            try:
                for old in existing:
                    saved = backup / old.relative_to(streaming)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    old.rename(saved)
                    moved.append((old, saved))
                staged.rename(target)
                installed = True
                if prepare_upload:
                    (Path(temporary) / "workshop").rename(workshop_bundle)
                    workshop_saved = True
                record["status"] = "installed"
                record_path.write_text(json.dumps(record, indent=2) + "\n")
            except BaseException as failure:
                recovery_errors = []
                if workshop_saved:
                    try:
                        shutil.rmtree(workshop_bundle)
                    except OSError as error:
                        recovery_errors.append(str(error))
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
    print("\nV8 INSTALLED:", target)
    print("Dated backup and replacement record:", backup)
    print("Carrier definitions prepared:", len(report["carriers"]))
    for carrier in report["carriers"]:
        if carrier.get("elevator_repairs"):
            print("Repaired existing lift routes:", carrier["file"])
    print("\nOpen Sea Power Mod Manager: enable RAN F-111N Naval Wing V8.")
    print("Disable older Naval Wing copies. Give V8 priority over carrier mods.")
    print("Keep carrier/source asset mods and your existing Anchor Chain setup enabled.")
    print("Restart Sea Power after changing the mod list.")
    print("\nFor your existing Workshop item 3810606011, use Update Existing,")
    print("then Pick Folder: \\user\\RAN-F111N-Naval-Wing")
    if prepare_upload:
        verify_workshop_bundle(workshop_bundle)
        print("Pick Image: \\user\\RAN-F111N-Naval-Wing\\preview.png")
        print("WORKSHOP PAYLOAD READY:", workshop_bundle)
        print("Description:", workshop_bundle / "description.txt")
        print("Change log:", workshop_bundle / "update-notes.txt")
        print("Upload instructions:", workshop_bundle / "UPLOAD_INSTRUCTIONS.txt")
        print("Optional terminal upload: bash ~/Downloads/replace-f111n-with-v8.sh --upload-prepared", shlex.quote(str(workshop_bundle)))
    print("Local preparation is complete. Steam has not been updated yet.")
    return backup


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Replace older local RAN F-111N folders with verified V8, keep backups and prepare an update for Steam Workshop item 3810606011."
    )
    parser.add_argument("game", nargs="?", help="Sea Power installation folder (auto-detected if omitted)")
    parser.add_argument("--package", type=Path, help="complete local V8 ZIP or extracted folder instead of downloading")
    parser.add_argument("--carrier-source", action="append", default=[], help="preferred carrier-mod folder; may be repeated")
    parser.add_argument("--dry-run", action="store_true", help="verify and preview without changing installed mod files")
    parser.add_argument("--upload", action="store_true", help="after replacement, upload to existing item 3810606011 through SteamCMD")
    parser.add_argument("--upload-prepared", type=Path, help="upload an already prepared bundle without downloading or replacing again")
    parser.add_argument("--steam-user", help="Steam login name that owns item 3810606011; password is handled only by SteamCMD")
    parser.add_argument("--steamcmd", type=Path, help="path to an installed SteamCMD executable")
    args = parser.parse_args(argv)
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        raise RuntimeError("Run this as your normal Steam user, without sudo.")
    if args.upload_prepared:
        if args.game or args.package or args.carrier_source or args.dry_run or args.upload:
            parser.error("--upload-prepared cannot be combined with installation options")
        upload_workshop(args.upload_prepared, args.steam_user, args.steamcmd)
        return 0
    if args.dry_run and args.upload:
        parser.error("--dry-run cannot upload to Steam")
    if not args.upload and (args.steam_user or args.steamcmd):
        parser.error("use --upload or --upload-prepared with SteamCMD options")
    if game_is_running() and not args.dry_run:
        raise RuntimeError("Close Sea Power, then run this script again.")
    games = [Path(args.game).expanduser().resolve()] if args.game else discover_games()
    if len(games) != 1:
        print("Specify the Sea Power installation you want to update:")
        for candidate in games:
            print(" ", candidate)
        if not games:
            print("No installation was found in your Steam library configuration.")
        print('Usage: bash replace-f111n-with-v8.sh "/full/path/to/steamapps/common/Sea Power"')
        return 2
    game = games[0]
    if not (game / "Sea Power_Data/StreamingAssets").is_dir():
        raise RuntimeError("This is not a Sea Power installation: " + str(game))
    check_target(game / "Sea Power_Data/StreamingAssets")
    sources = [Path(p).expanduser().resolve() for p in args.carrier_source]
    for source in sources:
        if not (source / "vessels").is_dir():
            raise RuntimeError("Carrier source has no vessels folder: " + str(source))
    with tempfile.TemporaryDirectory(prefix="ran-f111n-v8-download-") as temporary:
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
            archive = temporary / "V8.zip"
            fetch_archive(archive)
            unpacked = temporary / "extracted"
            extract_archive(archive, unpacked)
            package = package_root(unpacked)
        backup = install(package, game, sources, args.dry_run, prepare_upload=True)
        if args.upload:
            record = json.loads((backup / "replacement.json").read_text())
            upload_workshop(Path(record["workshop_bundle"]), args.steam_user, args.steamcmd)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped by user.", file=sys.stderr)
        raise SystemExit(130)
    except urllib.error.URLError as error:
        print("Replacement stopped: GitHub download failed:", error, file=sys.stderr)
        print("Use --package with the complete current V8 ZIP, or retry the download.", file=sys.stderr)
        raise SystemExit(1)
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile) as error:
        print("Replacement stopped:", error, file=sys.stderr)
        raise SystemExit(1)
V8_REPLACEMENT_PY
