# Rebuild and verify V8

Run from the extracted release root. Python 3.10+, the packages in `requirements-authoring.txt`, and Inkscape are required for authoring. Playing the shipped mod does not require these tools.

```bash
python3 -m pip install -r requirements-authoring.txt
python3 authoring/build_mod.py
python3 authoring/usn_liveries.py
python3 authoring/preview_v8.py
python3 authoring/checksums.py
python3 authoring/validate_mod.py
python3 authoring/validate_carriers.py
python3 authoring/test_v8_replacement.py
python3 authoring/build_docs.py
python3 authoring/package_release.py
```

`build_mod.py` delegates to `era_upgrade.py`, rebuilding dated aircraft, weapons, local sensors, presets, language entries and manifests from preserved baseline/native INIs. `investment_programme.py` holds the hypothetical blocks and explicit mass allowances. Source meshes/maps shipped in the package are inputs for the late UV bake; no Workshop download is needed to rebuild V8.

`usn_liveries.py` authors surface materials and vector decals through exact original UV geometry. `preview_v8.py` renders comparison/lettering images and late selection profiles. The CPU preview omits stock weapon meshes only present in the installed game. Earlier `paint_textures.py` direct repaint commands need the older original-source tree and are not part of the V8 sequence.

Refresh hashes after any mod data/asset change. Aircraft validation checks dates, actual inventories, mass/fuel, M61 magazines, preserved role/bay/model/landing contracts, progressive native investment, pod attachment, original assets and new atlas alpha/protected regions. Carrier tests use temporary native and representative RAN/custom fixtures to check compatibility, staging, backups, idempotence and source preservation. They do not modify a real game installation.

`investment_programme.py` also owns dated horizontal radar half angles. Fleet/Phoenix use 65/70/80/85 degrees and strike radar uses 45/55/65/75 degrees. The generator retains native vertical arcs. `unit_reference.py` generates sixteen role/edition stories and actual capability details from the final aircraft/sensor/store data. Keep description values on one physical line without semicolons, comment markers or unverified markup. The supplied Unit Reference screenshot appeared to stop at the old description's first semicolon. `validate_mod.py` checks the actual shipped sectors, metadata and parser-safe card text after every rebuild.

`build_docs.py` derives all sixteen comparisons, every loadout budget, CSV, investment JSON and release notes from actual manifests and completed validation reports. `package_release.py` requires PASS reports and matching current mod hashes, skips caches/download/Git trees, checks ZIP integrity and writes a SHA-256 sidecar.

Native guidance, gun fire, ECM display, service-date filtering, AI maximum-speed orders and actual landings still require Sea Power runtime testing. Historical facts and fictional estimates are separated in the root reference and manifest files.

`bay_loadouts.py` adds dated MudPig multistore fits without adding physical stations. `bay_docs.py` derives the bay guide and combined breakdown from current manifests. Bay checks cover counts, targeting, attack modes, adapter mass/readiness and coarse closed-door horizontal footprints. Full packing, release separation and armed recovery remain runtime tests; follow `docs/INTERNAL_BAY_V8.md`.

`investment_programme.py` owns the sourced speed policy: maximum Mach 2.5 × 1.15 = 2.875; RAAF sea-level 1,345 km/h × 1.15 = 1,546.75 km/h, converted to 835.178186 native knots; cruise 778 km/h × 1.15 = 894.7 km/h, converted to Mach 0.842269 using ISA at 37,000 ft. Normal power uses the sourced cruise target; no historical maximum dry-thrust speed is claimed. Dated thrust/response and range remain estimates. Validation checks the actual INIs, metadata, source-unit conversions and preserved approach/loiter/stall values.
