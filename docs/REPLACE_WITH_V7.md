# Replace an older F-111N installation with V7

Close Sea Power. Save **replace-f111n-with-v7.sh** in Downloads and run this from your terminal, including fish:

    bash ~/Downloads/replace-f111n-with-v7.sh

Run as your normal Steam user, without sudo. The script needs Bash and Python 3. It downloads the corrected V7 release, checks all 174 native game files, backs up recognised older local versions, and installs into:

    <Sea Power>/Sea Power_Data/StreamingAssets/user/RAN-F111N-Naval-Wing

Old local folders are saved intact under:

    <Sea Power>/RAN-F111N-backups/<date-and-time>/

The script handles both the Naval Wing title and the **RAN / RAAF F-111N Series** title shown in your screenshot, requiring the programme's aircraft IDs. Backups sit outside the game's mod search folders. Unrecognised destination contents stop the replacement. Failed replacement attempts restore the old folders and record the result in replacement.json.

It finds standard and Flatpak Steam installations and reads Steam's library configuration for additional drives. If more than one Sea Power installation is found, specify the one you use:

    bash ~/Downloads/replace-f111n-with-v7.sh "/full/path/to/steamapps/common/Sea Power"

The carrier reader handles UTF-8, Windows-1252, Latin-1 and BOM-marked UTF-16 source files. This fixes the reported invalid UTF-8 byte 0xA0 error. Source game, Workshop and carrier-mod files remain unchanged. Overrides are written inside the new V7 folder. Carrier preparation must finish before old local copies are moved.

The current helper also repairs recovery and taxi references to missing elevators, including the reported Elevator3/Elevator4 Majestic failures. It selects an existing usable lift, preferring a defined deck route, preserves existing coordinates, disables routes to absent lifts, and remaps surviving path indices. Repairs are recorded in CARRIER_COMPATIBILITY.json. If a carrier has no usable lift geometry, installation stops with its source path before moving the old mod.

If you already downloaded an earlier replacement script, overwrite it before rerunning:

    curl -fL 'https://raw.githubusercontent.com/gobertron/Seapower-F111N/main/replace-f111n-with-v7.sh' -o ~/Downloads/replace-f111n-with-v7.sh
    bash ~/Downloads/replace-f111n-with-v7.sh "/full/path/to/steamapps/common/Sea Power"

The corrected package includes all 61 native weapon/store display names and a Naval Wing chaff dispenser with ReloadTime=0 on all sixteen aircraft. The verified download is pinned to a specific corrected V7 commit; later repository changes do not silently alter the installed aircraft.

To use a current corrected V7 ZIP from this repository:

    bash ~/Downloads/replace-f111n-with-v7.sh --package ~/Downloads/RAN-F111N-Naval-Wing-V7.zip

A current GitHub source ZIP or clean extracted corrected package works. For an extracted package, supply the folder containing MOD_SHA256.txt, carrier_compatibility.py and RAN-F111N-Naval-Wing. The script does not modify the supplied package. An older ZIP, a package with an older carrier helper, or a package modified by a previous carrier-generation run fails the release checks. Running without --package downloads the corrected version automatically.

To verify and preview replacement without changing installed mod files:

    bash ~/Downloads/replace-f111n-with-v7.sh --package ~/Downloads/RAN-F111N-Naval-Wing-V7.zip --dry-run

Append **--carrier-source "/full/path/to/carrier/mod"** to prefer a particular carrier mod. This option may be repeated. Run the replacement again after carrier-mod updates to rebuild overrides.

After installation, enable **RAN F-111N Naval Wing V7**, disable older Naval Wing copies and give V7 priority over carrier mods. Keep carrier/source asset mods and your existing Anchor Chain setup enabled. Restart Sea Power.

The current replacement script also prepares the Workshop payload, preview and publication text. For item **3810606011**, select **Update Existing → RAN / RAAF F-111N Series**, then **Pick Folder → \user\RAN-F111N-Naval-Wing** and **Pick Image → \user\RAN-F111N-Naval-Wing\preview.png**. Paste the generated description and change notes, then submit. If SteamCMD is installed, `--upload` can submit the prepared content directly; SteamCMD handles authentication. See [complete Workshop upload instructions](STEAM_WORKSHOP_UPLOAD.md).

The script passed 18 replacement/recovery tests and six lift-repair tests. The Majestic cases reproduce the reported missing references on representative native layouts; the user's exact RAN definitions are not available here. The script replaces local files and prepares carrier configuration. Flight performance and carrier landings still require in-game testing.
