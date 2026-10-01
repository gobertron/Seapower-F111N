# V8 release notes

Fresh remake from the saved V6 base: sixteen aircraft, 167 selectable presets, dated Australian investment and eight USN-inspired late liveries. Original role/model/bay/landing contracts and M61/ECM/carrier arrangements are retained. Native modern-weapon approximations and explicit hypothetical naval masses remain documented.

| Verification | Status | Checks/maps |
|---|---|---|
| VALIDATION.json | PASS | 32093 |
| CARRIER_VALIDATION.json | PASS | 2243 |
| REPLACEMENT_VALIDATION.json | PASS | 18 replacement/recovery tests + 6 lift-repair tests |
| USN_TEXTURE_VALIDATION.json | PASS | 8 |

Heaviest full-fuel budget: ran_rf-111n_2003 / ReconLongRange at 50,897 kg, margin 948 kg. Python compilation and installer shell syntax are checked separately. ZIP integrity and SHA-256 are supplied with the package.

Carrier validation uses native and representative RAN/custom deck fixtures, not the user's exact installed RAN carriers. Representative Majestic cases reproduce stale Elevator3/Elevator4 associations and taxi paths; generated overrides use existing lift geometry and preserve source files. Installation checks cover staging, backups, source preservation and idempotence. Preview images render the shipped assets and omit stock weapon meshes unavailable outside the game.

**Runtime tested: no.** Sea Power is not installed here. Actual gun fire, guidance/release, date filtering, Mach 3 flight, ECM display and landings require in-game verification. No new DLL, interactive cockpit, real GPS weapon simulation or real carrier certification is claimed.

The README, all-aircraft/system comparisons, every loadout/mass breakdown, CSV/JSON data, references, Steam description, credits, authoring sources and validation reports are included. GitHub publication is separate from this downloadable release.
