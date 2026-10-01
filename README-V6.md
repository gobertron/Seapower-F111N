# RAN F-111N Naval Wing V6

The original four alternate-history Australian naval aircraft, each in **1980, 1985, 1995 and 2003 editions**: 16 aircraft and 167 selectable loadout presets.

Aircraft meshes, corrected textures, landing settings and MudPig's animated three-station internal bay are preserved. Historical aircraft/fuel/weapon references replace the earlier arbitrary weights, with explicit estimated allowances for the fictional naval conversion.

## Roles and weapons

| Model | Role |
|---|---|
| F-111N WaterPig | Fleet defence fighter; period IR/BVR/Phoenix missiles and M61 Vulcan |
| FB-111N MudPig | All-round maritime and land strike; every other family's period weapon types, bombing, stand-off strike, fleet interception, EW/SEAD and recon stores; M61 Vulcan |
| RF-111N SprintPig | Fast reconnaissance and ELINT; defensive IR missiles, M61 Vulcan, four tanks or clean sprint |
| EF-111N ScreamPig | Dedicated electronic attack/SEAD; two pods and two pylon-mounted offensive ECM systems; tanks or two anti-radiation missiles |

| Edition | Main air-to-air weapons | Harpoon | Additional strike/SEAD choices |
|---|---|---|---|
| 1980 | AIM-9L, AIM-7F, AIM-54A | AGM-84A | Mk 82/83/84, Paveway II, Maverick B, Shrike, Standard ARM |
| 1985 | AIM-9M, AIM-7M, early AIM-54C | AGM-84C | Maverick D, HARM A, GBU-15, Paveway III |
| 1995 | AIM-9M, AIM-120B, AIM-54C | AGM-84D Block 1C | Maverick G, HARM C, Popeye, SLAM |
| 2003 | ASRAAM, AIM-120C-5, AIM-54C | AGM-84L Block II | SLAM-ER, GBU-31/32 JDAM, AGM-154A JSOW |

These choices assume an Australian procurement and integration programme. They do not assert actual Australian service, historical export approval or F-111 certification. Early 1985 Phoenix C/HARM/Paveway III, 1995 Popeye and 2003 ASRAAM/Block II represent accelerated integration. Later weapons such as LRASM, JASSM-ER, AARGM, Meteor and SDB are excluded. Older bombing choices remain in later editions.

## Internal bay and M61

| MudPig preset | Wings | Internal bay |
|---|---|---|
| Anti Ship | 2 defensive IR missiles + 2 Harpoons | Empty |
| Heavy Anti Ship | 4 Harpoons | 3 Harpoons |
| Long Range Anti Ship | 2 defensive IR missiles + 2 Harpoons + 2 tanks | 3 Harpoons |

Missile versions follow the selected edition. Bay coordinates, concealment and two-door animation are unchanged. The retained three-Harpoon arrangement is an explicit fictional design feature.

WaterPig, MudPig and SprintPig have a fixed forward **M61 Vulcan with 2,000 rounds** in every loadout. The separate gun/feed/housing installation does not consume a pylon or a bay station. This relocation is fictional: a historical F-111 gun used weapons-bay space. The exterior meshes are retained, so no new fairing is drawn; native gun effects originate at the separate mount.

Laser bombing carries an external designation pod and EO stand-off fits carry a control pod. Their stations and masses are included. Neither pod consumes the internal bay. ScreamPig retains its dedicated EW role; MudPig gains removable EW containers for its EW presets rather than always-active offensive jammers.

## Weight and fuel

| Estimated empty mass, kg | 1980 | 1985 | 1995 | 2003 |
|---|---:|---:|---:|---:|
| WaterPig | 25,250 | 25,350 | 25,500 | 25,650 |
| MudPig | 24,900 | 25,000 | 25,150 | 25,300 |
| SprintPig | 25,350 | 25,450 | 25,600 | 25,750 |
| ScreamPig | 28,250 | 28,350 | 28,500 | 28,650 |

These are source-based **naval estimates**, not measured historical N-family weights. Common basic reference: 23,300 kg F-111C. Allowances: naval conversion 950 kg; separate gun hardware 650 kg; fleet radar 350 kg; recon equipment 450 kg; integrated EF equipment about 4,000 kg; edition avionics growth 0/100/250/400 kg.

All aircraft have **14,897 kg internal fuel**. Each 600-US-gallon external tank adds **1,770 kg fuel** plus an estimated **150 kg dry tank**. Two tanks give 18,437 kg total fuel; four give 21,977 kg. No internal fuel tank is added to the preserved bay. Fuel capacity follows the flight-manual table reproduced by Queensland Air Museum.

Weapons have their own carried masses. GP bombs use nominal class weights; guided weapons include guidance equipment. Real fuzes and subvariants can alter these rounded values. Mk 82 six-bomb racks include an estimated 100 kg per rack. Gun ammunition contributes 544 kg separately from empty mass. Every preset's full-fuel gross mass is checked against the **51,845 kg F-111C reference takeoff maximum**; the heaviest preset is 49,047 kg. This is a static mass budget, not a carrier catapult/arrestor certification or an unsupported new game parameter.

Non-recon engines use the published F-111C 43.6 kN dry / 82.3 kN afterburning thrust per engine. SprintPig keeps its requested fictional **Mach 2.52 cruise, Mach 3 maximum**, thrust and acceleration. Use `ReconFast` for a clean sprint and independent orders above 37,000 ft; formation-leader speed can limit it.

## Native simulation

All added ammunition IDs are local to this mod. `weapon_catalog.json` records their masses, period floor, donor and simulation assumptions. AMRAAM/ASRAAM use native active-radar/IR homing and simple original dimensional models. Phoenix C/HARM C retain donor geometry with variant mass/seeker estimates. Modern EO weapons approximate terminal homing without manual man-in-the-loop control. Block II Harpoon models radar-homing ship attack without its GPS route planning/land-attack mode.

**JDAM/JSOW use native ballistic/CEP accuracy and glide approximations, not full GPS/INS guidance.** They appear under level bombing; no unsupported GPS guidance enum or DLL is introduced. Their release trajectories and accuracy need in-game checking.

## Installation on CachyOS / Linux

1. Close Sea Power and extract the complete ZIP.
2. Open a terminal in `RAN-F111N-Naval-Wing-V6` and run `bash install-ran-f111n.sh` (works from fish).
3. Enable **RAN F-111N Naval Wing V6**, disable older Naval Wing copies, and give V6 priority over carrier mods. Keep source carrier mods enabled for their assets.
4. Restart and select the desired dated aircraft/loadout. Add it to the carrier air group in the mission editor.

For several Steam installations:

```bash
bash install-ran-f111n.sh "/full/path/to/steamapps/common/Sea Power"
```

An optional second argument selects a preferred carrier mod folder. The installer stages and verifies the update, backs up recognised previous local Naval Wing versions outside StreamingAssets, and creates carrier overrides in this mod without editing original/Workshop files. Rerun it after carrier-mod updates. An existing Anchor Chain setup can remain enabled.

## Carriers, dates and validation

All 16 aircraft retain carrier capability. Deck permissions and carrier role/class detect stock, RAN and custom carriers, including nonstandard names. Helicopter-only carriers retain the previous fictional arrested recovery conversion. Existing air groups are preserved; select the dated aircraft manually.

The original four unsuffixed IDs represent 1980. Later IDs end `_1985`, `_1995`, `_2003`. Service gates are 1980–1984, 1985–1994, 1995–2002 and 2003–2050. Saved missions using an old ID now refer to the 1980 edition; reselect its newer edition to get later weapons.

For Windows/manual installation, run `python carrier_compatibility.py "C:\path\to\Sea Power"` in the extracted folder, then copy `RAN-F111N-Naval-Wing` into `Sea Power_Data/StreamingAssets/user/` and enable it with carrier priority.

`VALIDATION.json` records dates, weapon union, M61 magazines, retained bay/landing/model contracts, mass arithmetic, references, pod attachment, asset hashes and checksums. `CARRIER_VALIDATION.json` covers all 16 IDs, native and representative RAN/custom decks, source preservation, staging and backups. `TEXTURE_VALIDATION.json` is the earlier audit for the eight unchanged maps.

Sea Power is not installed here. Actual gun fire, guidance/release, date filtering, Mach 3 flight, ECM display and landings remain untested in-game. Full source notes are in `HISTORICAL_REFERENCES.md`.

Models/liveries: [Workshop 3587484531](https://steamcommunity.com/sharedfiles/filedetails/?id=3587484531), [Workshop 3689650533](https://steamcommunity.com/sharedfiles/filedetails/?id=3689650533), preceding Naval Wing release. Roundel: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Roundel_of_Australia.svg). Native reference: [SEST-HOBBY export](https://github.com/SEST-HOBBY/Seapower-mods/tree/feature/northern-front-iii-export/mods-source/_vanilla/original). Target remains native 0.8.x content.
