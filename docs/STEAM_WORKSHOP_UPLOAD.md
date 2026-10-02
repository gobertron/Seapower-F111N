# Replace the local mod and update the existing Workshop item

Use **replace-f111n-with-v8.sh**. It downloads the corrected, pinned V8 release; verifies all 174 game files and the carrier helper; stages carrier compatibility; backs up older local Naval Wing folders; replaces the mod; and prepares a Workshop update for **3810606011**. Run with Bash from either Bash or fish, as your normal Steam user, without sudo.

Close Sea Power, then download the current script and run it against your installation:

```bash
mkdir -p ~/Downloads
curl -fL 'https://raw.githubusercontent.com/gobertron/Seapower-F111N/main/replace-f111n-with-v8.sh' -o ~/Downloads/replace-f111n-with-v8.sh
bash ~/Downloads/replace-f111n-with-v8.sh "/full/path/to/steamapps/common/Sea Power"
```

You can omit the game path when exactly one installation is found in your Steam libraries. Standard, Flatpak and additional Steam library drives are supported. `--package "/path/to/complete-V8.zip"` can use an offline release; it must contain the corrected files, carrier helper, preview and Workshop text. `--dry-run` checks replacement and Workshop preparation without writing to the game.

## Upload from Sea Power

The native mod is installed at:

```text
<Sea Power>/Sea Power_Data/StreamingAssets/user/RAN-F111N-Naval-Wing
```

1. Launch Sea Power through Steam while signed into the account that owns Workshop item **3810606011**.
2. Open the Workshop uploader in Mod Manager and select **Update Existing**. Choose your existing item **3810606011**, which may still appear as **RAN / RAAF F-111N Series**. Set Mod Name to **RAN F-111N Naval Wing V8**.
3. Use **Pick Folder** and select `\user\RAN-F111N-Naval-Wing`. This is the folder with `_info.ini`, `aircraft`, `ammunition`, `assets`, `systems` and the other native directories directly inside it.
4. Use **Pick Image** and select `\user\RAN-F111N-Naval-Wing\preview.png`. The supplied PNG is smaller than 1 MiB.
5. Paste `description.txt` into Mod Description and `update-notes.txt` into Change Log, then submit the update.

The script prints the absolute paths of these two text files and `UPLOAD_INSTRUCTIONS.txt`. Do not select the GitHub repository folder, a ZIP, the Steam Workshop download cache, or the parent `user` folder as the upload payload.

## Optional terminal upload through SteamCMD

If Valve's SteamCMD is installed, add `--upload` to the same replacement command:

```bash
bash ~/Downloads/replace-f111n-with-v8.sh "/full/path/to/steamapps/common/Sea Power" --upload
```

The script prompts for the Steam login name that owns item **3810606011**. SteamCMD handles password and Steam Guard prompts through your terminal. The script accepts no password argument, stores no password/API key, and saves no login transcript. An account name can be supplied with `--steam-user YOUR_STEAM_LOGIN`. If SteamCMD is not on PATH, supply `--steamcmd "/path/to/steamcmd.sh"`.

The upload configuration fixes `appid` to **1286220** and `publishedfileid` to **3810606011**, so it updates the existing item. It uploads the prepared native content and preview, changes the title and description to V8, and adds a short V8 change note. Existing Workshop visibility is preserved. The full description and longer update notes are also supplied for the in-game uploader above.

Valve documents SteamCMD Workshop publishing as a testing interface; the in-game uploader remains available if SteamCMD cannot publish for your account or this game. A real upload has not been tested here.

To retry an upload without another download or folder replacement, use the exact command printed by the script:

```bash
bash ~/Downloads/replace-f111n-with-v8.sh --upload-prepared "/full/path/to/Sea Power/RAN-F111N-workshop/3810606011/<timestamp>"
```

The prepared payload and VDF are checked before SteamCMD starts. The script reports `STEAM WORKSHOP UPDATED` only when SteamCMD confirms publication of **3810606011**; a zero exit status alone is insufficient. A failed upload leaves the installed V8 and prepared payload available for retry or in-game upload.

## Backups and prepared files

Older recognised local versions are moved intact into:

```text
<Sea Power>/RAN-F111N-backups/<timestamp>/
```

The prepared update is saved outside the game's mod search folders:

```text
<Sea Power>/RAN-F111N-workshop/3810606011/<timestamp>/
    content/                    native mod files; matches the installed local copy
    preview.png                 Workshop preview
    description.txt             full V8 Steam BBCode description
    update-notes.txt             full V8 change notes
    upload.vdf                  existing-item SteamCMD update
    workshop-sha256.json         checksums for the prepared content/configuration
    UPLOAD_INSTRUCTIONS.txt      exact in-game choices and retry command
    carrier-report.local.json   detailed local carrier source report
```

Personal absolute carrier source paths are retained only in `carrier-report.local.json`, outside the uploaded `content/`. The in-game folder and terminal payload contain the same portable compatibility report and game files. A failed preparation or folder swap restores the previous local installation. Existing original game files, Workshop cache files and unrelated mods are not replaced.

Enable V8, disable earlier Naval Wing copies, and give V8 priority over carrier mods. Keep carrier/source asset mods and your Anchor Chain setup enabled, then restart after changing enabled mods. Generated custom-carrier overrides still require the original carrier mods' models and assets. This script prepares files and upload configuration; runtime flight behaviour, guidance and carrier landings still require Sea Power testing.

References: [Sea Power manual](https://store.steampowered.com/manual/1286220/), [Valve's Workshop implementation guide](https://partner.steamgames.com/doc/features/workshop/implementation#SteamCmdIntegration), [Valve SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD).
