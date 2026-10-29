> Archived V8 document. See the [current Version 9.0 document](RELEASE_NOTES_V9_0.md).

# V8 release notes

Version 8 radar and Unit Reference update: progressive forward coverage across all sixteen aircraft, with sixteen expanded role- and edition-specific stories and capability descriptions. Fleet/Phoenix horizontal sectors progress through 130/140/160/170 degrees and strike sectors through 90/110/130/150 degrees. Plain single-line descriptions avoid semicolons that appeared to truncate the in-game card. Common maximum Mach 2.875, all 211 presets, dated weapons, original models and carrier/landing arrangements are retained. Coverage growth and the naval development story belong to the alternate-history programme. [Coverage and reference-card details](docs/RADAR_REFERENCE_V8.md).

| Verification | Status | Checks/maps |
|---|---|---|
| VALIDATION.json | PASS | 35490 |
| CARRIER_VALIDATION.json | PASS | 2243 |
| USN_TEXTURE_VALIDATION.json | PASS | 8 |

Heaviest full-fuel budget: ran_rf-111n_2003 / ReconLongRange at 50,897 kg, margin 948 kg. Python compilation and installer shell syntax are checked separately. ZIP integrity and SHA-256 are supplied with the package.

Carrier validation uses native and representative RAN/custom deck fixtures, not the user's exact installed RAN carriers. Installation checks cover staging, backups, source preservation and idempotence. Preview images render the shipped assets and omit stock weapon meshes unavailable outside the game.

**Runtime tested: no.** Sea Power is not installed here. Actual gun fire, guidance/release, date filtering, maximum-speed flight, ECM display and landings require in-game verification. No new DLL, interactive cockpit, real GPS weapon simulation or real carrier certification is claimed.

The README, all-aircraft/system comparisons, every loadout/mass breakdown, CSV/JSON data, references, Steam description, credits, authoring sources and validation reports are included. GitHub publication is separate from this downloadable release.
