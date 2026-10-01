# Rebuild and verify V7

Run from the extracted release root. Python 3.10+, the packages in `requirements-authoring.txt`, and Inkscape are required for authoring. Playing the shipped mod does not require these tools.

```bash
python3 -m pip install -r requirements-authoring.txt
python3 authoring/build_mod.py
python3 authoring/usn_liveries.py
python3 authoring/preview_v7.py
python3 authoring/checksums.py
python3 authoring/validate_mod.py
python3 authoring/validate_carriers.py
python3 authoring/build_docs.py
python3 authoring/package_release.py
```

`build_mod.py` delegates to `era_upgrade.py`, rebuilding dated aircraft, weapons, local sensors, presets, language entries and manifests from preserved baseline/native INIs. `investment_programme.py` holds the hypothetical blocks and explicit mass allowances. Source meshes/maps shipped in the package are inputs for the late UV bake; no Workshop download is needed to rebuild V7.

`usn_liveries.py` authors surface materials and vector decals through exact original UV geometry. `preview_v7.py` renders comparison/lettering images and late selection profiles. The CPU preview omits stock weapon meshes only present in the installed game. Earlier `paint_textures.py` direct repaint commands need the older original-source tree and are not part of the V7 sequence.

Refresh hashes after any mod data/asset change. Aircraft validation checks dates, actual inventories, mass/fuel, M61 magazines, preserved role/bay/model/landing contracts, progressive native investment, pod attachment, original assets and new atlas alpha/protected regions. Carrier tests use temporary native and representative RAN/custom fixtures to check compatibility, staging, backups, idempotence and source preservation. They do not modify a real game installation.

`build_docs.py` derives all sixteen comparisons, every loadout budget, CSV, investment JSON and release notes from actual manifests and completed validation reports. `package_release.py` requires PASS reports and matching current mod hashes, skips caches/download/Git trees, checks ZIP integrity and writes a SHA-256 sidecar.

Native guidance, gun fire, ECM display, service-date filtering, AI Mach 3 orders and actual landings still require Sea Power runtime testing. Historical facts and fictional estimates are separated in the root reference and manifest files.
