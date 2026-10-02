# V8 changes from V6

## Version 8 internal-bay update — 2 October 2026

- Expanded the 167-preset baseline to 211 presets, with 44 new MudPig bay mission fits across the four editions.
- Added bay anti-ship, Mk 82/Mk 84 bombing, GBU-12 precision and Phoenix interception presets with long-range companions. The 2003 edition also gains GBU-31/32 JDAM bay presets.
- Added extra bay stores to existing bombing, precision, Maverick, Shrike, SLAM and JDAM fits. Retained the original standard/heavy/long-range Harpoon inventories.
- Kept three physical bay stations, concealment, door animations and carrier/landing geometry. Added one-store Phoenix/Shrike suspension offsets and Phoenix targeting references.
- Added explicit 40/50/60/75 kg estimated bay-upgrade allowances and dated bay readiness. All full-fuel takeoff budgets remain below the existing 51,845 kg reference.
- Extended validation to cover bay inventory, capacity, targeting, attack modes and coarse native/local-mesh stowage footprints. Armed carrier recovery and release still require in-game tests.
- Refreshed loadout tables, CSV/JSON, Workshop text, checksums and the pinned V8 download workflow. Added an armed recovery test guide.

## Version 8 release naming — 1 October 2026

- Updated release branding, filenames, native mod metadata, previews, authoring scripts, documentation and Workshop text to V8.
- Refreshed all affected installer checksums and download verification data. Optional SteamCMD upload now updates the existing item's V8 title and description while preserving its visibility.
- Aircraft IDs, dated variants and gameplay configuration are retained.

## V8 Workshop preparation — 1 October 2026

- Extended the standalone replacement script to prepare a native Workshop payload matching the installed V8 folder, with a verified preview and the full description/update text.
- Added a fixed existing-item SteamCMD configuration for Sea Power 1286220 / Workshop item 3810606011. Version 8 updates the release title and description during terminal upload; visibility is preserved.
- Added optional `--upload` and `--upload-prepared` paths. SteamCMD handles authentication; publication is reported only for a confirmed success on the expected item ID.
- Staged Workshop preparation before the old-folder swap, with rollback when saving the payload fails. Personal absolute carrier paths stay outside published content.
- Added publication/recovery tests and step-by-step in-game/terminal upload documentation. Live Steam publication remains untested.

## V8 naming and installer correction — 1 October 2026

- Corrected all 61 custom ammunition/store names to the game's flat AmmunitionNames table. Missile names now have the native display-name, nickname, category and description fields used by loadout tooltips, weapon references and launched-weapon labels.
- Added a Naval Wing chaff dispenser with ReloadTime=0 and selected it on all sixteen aircraft. Existing chaff quantities and burst spacing are retained.
- Fixed carrier-file reading for UTF-8, Windows-1252, Latin-1 and BOM-marked UTF-16, including the reported invalid byte 0xA0 failure.
- Repaired stale recovery-elevator and launch/taxi references in generated overrides, using existing lifts and coordinates. Invalid paths are disabled and remaining path indices remapped. No replacement lift or carrier geometry is invented. Representative ran_cv_majestic1968/Elevator3 and ran_majestic_59/Elevator4 cases pass.
- Added a standalone CachyOS/Linux replacement script with a verified download, complete staged copy, dated backups, dry run and rollback checks.
- Pinned the replacement download and helper checksum to the lift repair; older helpers are rejected before replacement. Carrier failures now identify the source file and do not show an unrelated download warning. Eighteen replacement/recovery tests and six lift-repair tests passed.

## Original V8 remake

This V8 is a fresh remake from the saved V6 package. Four families, sixteen dated aircraft and 167 presets are retained.

- Added dated engine output, native velocity/thrust response, control gains, climb and nominal cruise-range improvements.
- Added local year-specific radar, FLIR, RWR/ELINT, defensive ECM and offensive ECM settings, with improved weapon readiness.
- Added sixteen dated ECM-container aliases for EF and removable FB EW fits; physical pod/system counts stay two.
- Improved estimated AIM-120C-5 ECCM relative to AIM-120B.
- Added explicit systems/control, engine-retrofit and RF thermal mass allowances. The heaviest full-fuel budget is 50,897 kg.
- Added eight dedicated 1995/2003 USN-inspired grey maps, matching tank textures and selection profiles, with subdued Australian markings.
- Preserved original UVs/alpha/protected mechanical areas, normal/specular maps, models, bay/landing animations and earlier maps.
- Retained separate M61 installations, RF Mach 3/triple-response settings, the exact three-Harpoon FB bay and all-year carrier compatibility.
- Added all-aircraft/system comparison tables, every loadout/mass budget, CSV/JSON data, provenance, authoring utilities, Steam description and release/test notes.

V6's native modern-weapon approximations remain. Runtime guidance, gun fire, Mach 3 flight, ECM display, date filtering and landings still need in-game testing.
