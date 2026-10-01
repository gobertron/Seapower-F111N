# RAN F-111N Naval Wing V7 — Complete Breakdown

**1 October 2026 correction:** all 61 custom ammunition/store names now use the native AmmunitionNames table; all 16 aircraft select a local chaff dispenser with ReloadTime=0. The carrier reader accepts Windows-encoded source INIs and repairs stale elevator/taxi references using existing lift geometry. The standalone script passed 18 replacement/recovery tests; six lift-repair tests cover representative Majestic Elevator3/Elevator4 failures, route remapping, idempotence and unavailable geometry.

This describes the completed fresh V7 remake from the verified V6 ZIP. Values describe the shipped game configuration, not tested real-world performance. The downloadable release is 84,349,039 bytes (84.35 MB / 80.44 MiB).

## Scope and changes from V6

Four families in 1980, 1985, 1995 and 2003 editions: **16 aircraft, 167 selectable presets and 61 local store definitions**. Compatibility aliases can repeat inventories; 61 definitions do not mean 61 different weapons. V6 already supplied these four dated families and presets.

V7 adds dated engine output, flight response/controls, climb/range improvements, local dated radar/FLIR/RWR/ELINT/ECM ratings, weapon readiness, estimated AIM-120C-5 ECCM, sixteen dated ECM aliases, explicit upgrade mass allowances, eight late grey liveries and expanded documentation. V6 role, gun, bay, model/landing and carrier contracts are retained.

| Family | Main role | Configured maximum Mach | Gun / offensive EW | Presets across all years |
|---|---|---:|---|---:|
| F-111N WaterPig | Fleet defence/interception | 2.5 | M61, 2,000 rounds | 16 |
| FB-111N MudPig | Maritime/land strike; all-rounder | 2.6 | M61, 2,000 rounds | 103 |
| RF-111N SprintPig | Fast reconnaissance/ELINT | 3.0 | M61, 2,000 rounds | 24 |
| EF-111N ScreamPig | Electronic attack/SEAD | 2.2 | 2 pods / 2 offensive ECM systems; no gun | 24 |

## All sixteen aircraft compared

Maximum/cruise speeds, thrust, range and response are native game settings. Range is the configured nominal Miles field, not a combat radius. Empty weights include explicit estimates for the fictional naval programme.

| Aircraft | Year | Role | Empty kg | Max Mach | Cruise Mach | Range miles | AB kN/engine | Gun / rounds | Presets | Suggested fit |
|---|---|---|---|---|---|---|---|---|---|---|
| F-111N WaterPig | 1980 | Fighter | 25,250 | 2.5 | 0.84 | 1,450 | 82.3 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 1985 | Fighter | 25,500 | 2.5 | 0.88 | 1,537 | 90.53 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 1995 | Fighter | 26,750 | 2.5 | 0.92 | 1,653 | 120 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 2003 | Fighter | 27,250 | 2.5 | 0.96 | 1,769 | 129 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| FB-111N MudPig | 1980 | Bomber | 24,900 | 2.6 | 0.84 | 1,550 | 82.3 | M61 / 2,000 | 23 | AntiShip / AntiShipHeavy / AntiShipLongRange |
| FB-111N MudPig | 1985 | Bomber | 25,150 | 2.6 | 0.88 | 1,643 | 90.53 | M61 / 2,000 | 24 | AntiShip / AntiShipHeavy / AntiShipLongRange |
| FB-111N MudPig | 1995 | Bomber | 26,400 | 2.6 | 0.92 | 1,767 | 120 | M61 / 2,000 | 26 | AntiShip / AntiShipHeavy / AntiShipLongRange |
| FB-111N MudPig | 2003 | Bomber | 26,900 | 2.6 | 0.96 | 1,891 | 129 | M61 / 2,000 | 30 | AntiShip / AntiShipHeavy / AntiShipLongRange |
| RF-111N SprintPig | 1980 | Recon,ESM | 25,350 | 3.0 | 2.52 | 2,300 | 480 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 1985 | Recon,ESM | 25,650 | 3.0 | 2.52 | 2,438 | 528 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 1995 | Recon,ESM | 27,000 | 3.0 | 2.52 | 2,622 | 600 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 2003 | Recon,ESM | 27,600 | 3.0 | 2.52 | 2,806 | 672 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| EF-111N ScreamPig | 1980 | EW,ESM | 28,250 | 2.2 | 0.84 | 1,700 | 82.3 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 1985 | EW,ESM | 28,500 | 2.2 | 0.88 | 1,802 | 90.53 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 1995 | EW,ESM | 29,750 | 2.2 | 0.92 | 1,938 | 120 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 2003 | EW,ESM | 30,250 | 2.2 | 0.96 | 2,074 | 129 | None | 6 | EWLongRange / EscortSEAD |

## Editions, service dates and weapons

| Edition | Service gate | Presets | Air-to-air | Harpoon | Strike/SEAD additions |
|---|---|---:|---|---|---|
| 1980 | 1980–1984 | 39 | AIM-9L, AIM-7F, AIM-54A | AGM-84A | Mk 82/83/84, Paveway II, Maverick B, Shrike, Standard ARM |
| 1985 | 1985–1994 | 40 | AIM-9M, AIM-7M, AIM-54C | AGM-84C | Maverick D, HARM A, GBU-15, Paveway III |
| 1995 | 1995–2002 | 42 | AIM-9M, AIM-120B, AIM-54C | AGM-84D | Maverick G, HARM C, Popeye, SLAM |
| 2003 | 2003–2050 | 46 | ASRAAM, AIM-120C-5, AIM-54C | AGM-84L Block II | SLAM-ER, GBU-31/32 JDAM, AGM-154A JSOW |

Later MudPig editions retain earlier bombing options. These choices assume funded Australian procurement and integration, including accelerated early adoption. They do not assert actual historical Australian service, export approval or F-111 certification. The exact inventories of all presets follow below.

Unsuffixed IDs are the 1980 aircraft. Later IDs end `_1985`, `_1995` or `_2003`. Saved missions using an old unsuffixed ID select 1980 equipment; choose a later edition to use its newer equipment.

## Funded propulsion, flight and mission-system investment

Every edition assumes heavy Australian funding for naval conversion, propulsion, flight controls, weapons integration, targeting and EW. Native settings improve by year. They are hypothetical programme ratings, not measured historical N-family performance.

| Setting | 1980 | 1985 | 1995 | 2003 |
|---|---|---|---|---|
| Engine for F/FB/EF | TF30-P-109 reference | TF30 naval uprating (fictional) | F110-GE-400-class naval adaptation | F110-GE-129-class naval adaptation |
| Dry thrust N/engine for F/FB/EF | 43600 | 47960 | 60000 | 65000 |
| Afterburning thrust N/engine for F/FB/EF | 82300 | 90530 | 120000 | 129000 |
| Velocity/thrust response multiplier | 1 | 1.1 | 1.25 | 1.4 |
| Pitch/heading/bank gain multiplier | 1 | 1.05 | 1.1 | 1.15 |
| Nominal cruise-range factor | 1 | 1.06 | 1.14 | 1.22 |
| Cruise Mach for F/FB/EF | 0.84 | 0.88 | 0.92 | 0.96 |
| Climb-setting multiplier | 1 | 1.05 | 1.15 | 1.25 |
| Additional systems/control mass kg | 0 | 150 | 650 | 850 |
| Propulsion-retrofit allowance kg | 0 | 0 | 600 | 750 |
| RF thermal allowance kg | 0 | 50 | 150 | 250 |
| Radar gain addition | 0 | 1 | 2.5 | 4 |
| Radar range factor | 1 | 1.06 | 1.14 | 1.22 |
| Main radar target channels | 1 | 2 | 4 | 6 |
| Main radar weapon channels | 2 | 4 | 6 | 8 |
| Radar look-down multiplier | 0.85 | 0.9 | 0.96 | 1 |
| FLIR range multiplier | 2 | 2.1 | 2.4 | 2.7 |
| RWR/ELINT gain | 5 | 5.5 | 6.5 | 7.5 |
| RWR bearing-resolution setting | 25 | 22 | 17 | 12 |
| ELINT bearing-resolution setting | 10 | 8 | 6 | 4 |
| Defensive ECM JamChance | 0.4 | 0.48 | 0.6 | 0.72 |
| Offensive ECM PeakPower field | 1000 | 1250 | 1700 | 2200 |
| Offensive ECM MaxRange field | 240 | 260 | 300 | 340 |
| Offensive ECM Gain | 6 | 6.5 | 7 | 7.5 |
| Offensive ECM channels per system | 1 | 2 | 3 | 4 |
| FB weapon ReadyUpTime | 30 | 25 | 20 | 15 |
| Other weapon ReadyUpTime | 20 | 18 | 15 | 12 |
| Weapon CoolDownTime | 60 | 55 | 45 | 40 |

The main radar values above apply to the fleet/strike donor. Separate Phoenix targeting retains six target and six weapon channels. Radar RangeResolution is 30 / 25 / 18 / 12; HasDataLink is False / False / True / True. Offensive ECM has two separate systems, each with the dated channel setting; system count remains two. Native power/range fields are not independently calibrated engineering ratings.

F uses AWG-9 donor geometry/settings, labelled as a hypothetical APG-71-class digital adaptation from 1995. The other roles use APQ-161 native settings to represent naval multimode radar. No new radar/flight simulation engine, interactive digital cockpit or MFD mesh is introduced. The nominal range factor does not guarantee an equivalent increase in combat radius.

| RF propulsion setting | 1980 | 1985 | 1995 | 2003 |
|---|---|---|---|---|
| Dry N per engine | 320000 | 352000 | 400000 | 448000 |
| Afterburning N per engine | 480000 | 528000 | 600000 | 672000 |

RF keeps Mach 2.52 cruise and Mach 3 maximum throughout. VelocityGain and ThrustGain stay three times WaterPig's matching edition, with the same dated improvement factor. This is not triple maximum airspeed. Use ReconFast, independent orders and appropriate altitude for a sprint; actual AI flight needs runtime testing.

These upgrades improve native settings and retain original cockpit/model geometry. No new interactive digital cockpit, custom flight DLL or independently calibrated sensor simulation is added.

## Bay, guns and pylons

The retained FB three-station bay, concealment and door animations are unchanged. AntiShip carries two wing Harpoons and two IR missiles with an empty bay. AntiShipHeavy carries four wing and three bay Harpoons. AntiShipLongRange carries two wing and three bay Harpoons, two IR missiles and two tanks. All variants follow the edition.

F/FB/RF retain a forward M61 with 2,000 rounds. Its separate fictional installation does not use a bay or pylon station. EF has no gun and retains exactly two physical pylon ECM pods and two offensive ECM systems. FB receives two removable pods only in EW fits. External laser-designation and EO-control pods are counted in station and mass budgets.

## Liveries

Eight dedicated 1995/2003 3072 × 2048 maps use USN-inspired darker upper/intermediate side/light underside tactical greys with Australian roundels, NAVY lettering, A8 serials, flying-pig badges and subdued checks. Fuel tanks and selection profiles match; 2003 adds modest wear. Main lettering was checked on both sides of rendered aircraft. Original UVs, alpha, protected cockpit/mechanical pixels, normal/specular maps, earlier liveries, meshes and landing animations are retained. The colours are screen approximations, not certified paint standards.

## Carrier installation and use

All sixteen IDs retain carrier capability. The release installer creates source-preserving overrides for discovered installed stock, RAN and custom decks, including the retained fictional helicopter-deck arrested-recovery conversion. Existing air groups and helicopter/VTOL approaches are preserved. Select the dated aircraft in the carrier air group manually. This configuration does not prove successful recovery on every installed carrier.

On CachyOS/Linux, close the game, extract the complete release ZIP and run `bash install-ran-f111n.sh` from its V7 folder. An optional first argument specifies the Sea Power install path. Enable V7, disable older Naval Wing copies, give V7 priority over carrier mods, keep source carrier mods enabled for assets and restart. Rerun after carrier-mod updates. For Windows/manual installation, use the included `carrier_compatibility.py` and the release README instructions.

For RF sprint, use `ReconFast` and independent orders above 37,000 ft; a formation leader can limit speed. Mach settings do not force the AI to hold that airspeed.

## Validation and limits

| Check | Status | Count |
|---|---|---:|
| Mod data, mass, stores, sensors and retained design | PASS | 32,093 |
| Carrier/installer fixtures | PASS | 2,243 |
| New late-edition texture audits | PASS | 8 |
| Runtime flight, weapons and landings | Not tested | — |

Carrier tests use native and representative RAN/custom fixtures; they are not a test of every carrier in the user’s installation. Gun fire, guidance/release, Mach 3 flight, ECM display, date filtering and actual carrier landings still need Sea Power runtime testing.

Native guidance limits: AMRAAM has no platform midcourse correction; ASRAAM adds no helmet sight/LOAL; EO weapons add no manual retargeting; Block II Harpoon models ship attack; JDAM/JSOW use native CEP/ballistic/glide approximations rather than full GPS/INS. Naval conversion, relocated gun, three-Harpoon bay, RF propulsion and small-deck recovery remain alternate history.

## Every preset, store and mass budget

Generated from the shipped INIs and manifests. All 16 aircraft, all 167 selectable presets and all 61 local store definitions are listed. Compatible aliases may carry identical stores. Values are rounded carried-mass budgets; fictional naval equipment and retrofit allowances are explicit.

## Empty mass components

The basic reference is 23,300 kg F-111C. The retained fictional bay is not re-engineered. Every version has 14,897 kg internal fuel; tank fuel and M61 ammunition are separate from empty mass.

| Aircraft | Year | Basic reference kg | Naval kg | Role kg | Gun hardware kg | Edition avionics kg | Systems/controls kg | Propulsion kg | RF thermal kg | Total kg |
|---|---|---|---|---|---|---|---|---|---|---|
| F-111N | 1980 | 23,300 | 950 | 350 | 650 | 0 | 0 | 0 | 0 | 25,250 |
| F-111N | 1985 | 23,300 | 950 | 350 | 650 | 100 | 150 | 0 | 0 | 25,500 |
| F-111N | 1995 | 23,300 | 950 | 350 | 650 | 250 | 650 | 600 | 0 | 26,750 |
| F-111N | 2003 | 23,300 | 950 | 350 | 650 | 400 | 850 | 750 | 0 | 27,250 |
| FB-111N | 1980 | 23,300 | 950 | 0 | 650 | 0 | 0 | 0 | 0 | 24,900 |
| FB-111N | 1985 | 23,300 | 950 | 0 | 650 | 100 | 150 | 0 | 0 | 25,150 |
| FB-111N | 1995 | 23,300 | 950 | 0 | 650 | 250 | 650 | 600 | 0 | 26,400 |
| FB-111N | 2003 | 23,300 | 950 | 0 | 650 | 400 | 850 | 750 | 0 | 26,900 |
| RF-111N | 1980 | 23,300 | 950 | 450 | 650 | 0 | 0 | 0 | 0 | 25,350 |
| RF-111N | 1985 | 23,300 | 950 | 450 | 650 | 100 | 150 | 0 | 50 | 25,650 |
| RF-111N | 1995 | 23,300 | 950 | 450 | 650 | 250 | 650 | 600 | 150 | 27,000 |
| RF-111N | 2003 | 23,300 | 950 | 450 | 650 | 400 | 850 | 750 | 250 | 27,600 |
| EF-111N | 1980 | 23,300 | 950 | 4,000 | 0 | 0 | 0 | 0 | 0 | 28,250 |
| EF-111N | 1985 | 23,300 | 950 | 4,000 | 0 | 100 | 150 | 0 | 0 | 28,500 |
| EF-111N | 1995 | 23,300 | 950 | 4,000 | 0 | 250 | 650 | 600 | 0 | 29,750 |
| EF-111N | 2003 | 23,300 | 950 | 4,000 | 0 | 400 | 850 | 750 | 0 | 30,250 |

## Budget rules

- Each 600-US-gallon tank: 1,770 kg fuel plus estimated 150 kg dry shell. Two tanks give 18,437 kg total fuel; four give 21,977 kg.
- Fixed M61 hardware/feed/housing allowance: 650 kg within F/FB/RF empty mass. Loaded 2,000-round magazine: another 544 kg. EF has no gun.
- Mk 82 six-bomb racks include one-sixth of an estimated 100 kg rack per bomb.
- Full-fuel takeoff budget = empty mass + dry stores/rack allowances + internal/external fuel + gun ammunition.
- Every preset is checked against the 51,845 kg F-111C reference maximum. This is not a carrier catapult/arrestor certification.

## F-111N WaterPig — 1980

ID: `ran_f-111n`. Role: Fighter. Empty: 25,250 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,497 | 10,348 |
| AirToAir | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,497 | 10,348 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54A Phoenix | Empty | 1,358 | 18,437 | 45,589 | 6,256 |
| FleetIntercept | 2 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | 2 × AIM-54A Phoenix | Empty | 1,520 | 14,897 | 42,211 | 9,634 |

## F-111N WaterPig — 1985

ID: `ran_f-111n_1985`. Role: Fighter. Empty: 25,500 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,747 | 10,098 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,747 | 10,098 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,398 | 18,437 | 45,879 | 5,966 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | 2 × AIM-54C Phoenix | Empty | 1,560 | 14,897 | 42,501 | 9,344 |

## F-111N WaterPig — 1995

ID: `ran_f-111n_1995`. Role: Fighter. Empty: 26,750 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,839 | 9,006 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,839 | 9,006 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,398 | 18,437 | 47,129 | 4,716 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | 2 × AIM-54C Phoenix | Empty | 1,402 | 14,897 | 43,593 | 8,252 |

## F-111N WaterPig — 2003

ID: `ran_f-111n_2003`. Role: Fighter. Empty: 27,250 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 43,347 | 8,498 |
| AirToAir | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 43,347 | 8,498 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,402 | 18,437 | 47,633 | 4,212 |
| FleetIntercept | 2 × ASRAAM; 2 × AIM-120C-5 AMRAAM | 2 × AIM-54C Phoenix | Empty | 1,406 | 14,897 | 44,097 | 7,748 |

## FB-111N MudPig — 1980

ID: `ran_fb-111n`. Role: Bomber. Empty: 24,900 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 2 × AGM-84A Harpoon | Empty | Empty | 1,224 | 14,897 | 41,565 | 10,280 |
| AirToAir | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,147 | 10,698 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54A Phoenix | Empty | Empty | 1,358 | 18,437 | 45,239 | 6,606 |
| FleetIntercept | 2 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow; 2 × AIM-54A Phoenix | Empty | Empty | 1,520 | 14,897 | 41,861 | 9,984 |
| AntiShip | 2 × AIM-9L Sidewinder; 2 × AGM-84A Harpoon | Empty | Empty | 1,224 | 14,897 | 41,565 | 10,280 |
| AntiShipHeavy | 4 × AGM-84A Harpoon | Empty | 3 × AGM-84A Harpoon | 3,682 | 14,897 | 44,023 | 7,822 |
| AntiShipLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84A Harpoon | Empty | 3 × AGM-84A Harpoon | 3,102 | 18,437 | 46,983 | 4,862 |
| Strike | 2 × AIM-9L Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | Empty | 6,020 | 14,897 | 46,361 | 5,484 |
| StrikeLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | Empty | 3,396 | 18,437 | 47,277 | 4,568 |
| StrikeHeavy | 2 × AIM-9L Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | Empty | 3,800 | 14,897 | 44,141 | 7,704 |
| StrikeHeavyLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | Empty | 2,286 | 18,437 | 46,167 | 5,678 |
| StrikeMedium | 2 × AIM-9L Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | Empty | 1,988 | 14,897 | 42,329 | 9,516 |
| StrikePrecision | 2 × AIM-9L Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 3,124 | 14,897 | 43,465 | 8,380 |
| StrikePrecisionLight | 2 × AIM-9L Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,153 | 14,897 | 41,494 | 10,351 |
| StrikePrecisionMedium | 2 × AIM-9L Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,807 | 14,897 | 42,148 | 9,697 |
| StrikePrecisionLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,556 | 18,437 | 45,437 | 6,408 |
| MaverickStrike | 2 × AIM-9L Sidewinder; 4 × AGM-65B Maverick | Empty | Empty | 1,004 | 14,897 | 41,345 | 10,500 |
| SEAD | 2 × AIM-9L Sidewinder; 4 × AGM-78 Standard ARM | Empty | Empty | 2,652 | 14,897 | 42,993 | 8,852 |
| SEADShrike | 2 × AIM-9L Sidewinder; 4 × AGM-45 Shrike | Empty | Empty | 884 | 14,897 | 41,225 | 10,620 |
| EW | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 44,873 | 6,972 |
| EWLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 44,873 | 6,972 |
| EscortSEAD | 2 × AIM-9L Sidewinder; 2 × AGM-78 Standard ARM; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 1,932 | 14,897 | 42,273 | 9,572 |
| ReconLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,193 | 3,652 |

## FB-111N MudPig — 1985

ID: `ran_fb-111n_1985`. Role: Bomber. Empty: 25,150 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × AGM-84C Harpoon | Empty | Empty | 1,224 | 14,897 | 41,815 | 10,030 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,397 | 10,448 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,398 | 18,437 | 45,529 | 6,316 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow; 2 × AIM-54C Phoenix | Empty | Empty | 1,560 | 14,897 | 42,151 | 9,694 |
| AntiShip | 2 × AIM-9M Sidewinder; 2 × AGM-84C Harpoon | Empty | Empty | 1,224 | 14,897 | 41,815 | 10,030 |
| AntiShipHeavy | 4 × AGM-84C Harpoon | Empty | 3 × AGM-84C Harpoon | 3,682 | 14,897 | 44,273 | 7,572 |
| AntiShipLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84C Harpoon | Empty | 3 × AGM-84C Harpoon | 3,102 | 18,437 | 47,233 | 4,612 |
| Strike | 2 × AIM-9M Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | Empty | 6,020 | 14,897 | 46,611 | 5,234 |
| StrikeLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | Empty | 3,396 | 18,437 | 47,527 | 4,318 |
| StrikeHeavy | 2 × AIM-9M Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | Empty | 3,800 | 14,897 | 44,391 | 7,454 |
| StrikeHeavyLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | Empty | 2,286 | 18,437 | 46,417 | 5,428 |
| StrikeMedium | 2 × AIM-9M Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | Empty | 1,988 | 14,897 | 42,579 | 9,266 |
| StrikePrecision | 2 × AIM-9M Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 3,124 | 14,897 | 43,715 | 8,130 |
| StrikePrecisionLight | 2 × AIM-9M Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,153 | 14,897 | 41,744 | 10,101 |
| StrikePrecisionMedium | 2 × AIM-9M Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,807 | 14,897 | 42,398 | 9,447 |
| StrikePrecisionLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,556 | 18,437 | 45,687 | 6,158 |
| MaverickStrike | 2 × AIM-9M Sidewinder; 4 × AGM-65D Maverick | Empty | Empty | 1,044 | 14,897 | 41,635 | 10,210 |
| SEAD | 2 × AIM-9M Sidewinder; 4 × AGM-88A HARM | Empty | Empty | 1,616 | 14,897 | 42,207 | 9,638 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 45,123 | 6,722 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 45,123 | 6,722 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88A HARM; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 1,414 | 14,897 | 42,005 | 9,840 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,443 | 3,402 |
| EOGlideStrike | 2 × AIM-9M Sidewinder; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,692 | 14,897 | 43,283 | 8,562 |
| StrikePavewayIII | 2 × AIM-9M Sidewinder; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | Empty | 3,574 | 14,897 | 44,165 | 7,680 |

## FB-111N MudPig — 1995

ID: `ran_fb-111n_1995`. Role: Bomber. Empty: 26,400 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × AGM-84D Harpoon Block 1C | Empty | Empty | 1,224 | 14,897 | 43,065 | 8,780 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,489 | 9,356 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,398 | 18,437 | 46,779 | 5,066 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM; 2 × AIM-54C Phoenix | Empty | Empty | 1,402 | 14,897 | 43,243 | 8,602 |
| AntiShip | 2 × AIM-9M Sidewinder; 2 × AGM-84D Harpoon Block 1C | Empty | Empty | 1,224 | 14,897 | 43,065 | 8,780 |
| AntiShipHeavy | 4 × AGM-84D Harpoon Block 1C | Empty | 3 × AGM-84D Harpoon Block 1C | 3,682 | 14,897 | 45,523 | 6,322 |
| AntiShipLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84D Harpoon Block 1C | Empty | 3 × AGM-84D Harpoon Block 1C | 3,102 | 18,437 | 48,483 | 3,362 |
| Strike | 2 × AIM-9M Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | Empty | 6,020 | 14,897 | 47,861 | 3,984 |
| StrikeLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | Empty | 3,396 | 18,437 | 48,777 | 3,068 |
| StrikeHeavy | 2 × AIM-9M Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | Empty | 3,800 | 14,897 | 45,641 | 6,204 |
| StrikeHeavyLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | Empty | 2,286 | 18,437 | 47,667 | 4,178 |
| StrikeMedium | 2 × AIM-9M Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | Empty | 1,988 | 14,897 | 43,829 | 8,016 |
| StrikePrecision | 2 × AIM-9M Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 3,124 | 14,897 | 44,965 | 6,880 |
| StrikePrecisionLight | 2 × AIM-9M Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,153 | 14,897 | 42,994 | 8,851 |
| StrikePrecisionMedium | 2 × AIM-9M Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,807 | 14,897 | 43,648 | 8,197 |
| StrikePrecisionLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,556 | 18,437 | 46,937 | 4,908 |
| MaverickStrike | 2 × AIM-9M Sidewinder; 4 × AGM-65G Maverick | Empty | Empty | 1,380 | 14,897 | 43,221 | 8,624 |
| SEAD | 2 × AIM-9M Sidewinder; 4 × AGM-88C HARM | Empty | Empty | 1,616 | 14,897 | 43,457 | 8,388 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 46,373 | 5,472 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 46,373 | 5,472 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 1,414 | 14,897 | 43,255 | 8,590 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 49,693 | 2,152 |
| EOGlideStrike | 2 × AIM-9M Sidewinder; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,692 | 14,897 | 44,533 | 7,312 |
| StrikePavewayIII | 2 × AIM-9M Sidewinder; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | Empty | 3,574 | 14,897 | 45,415 | 6,430 |
| PopeyeStrike | 2 × AIM-9M Sidewinder; 2 × AGM-142 Popeye / Have Nap; 1 × EO weapon control pod | Empty | Empty | 3,152 | 14,897 | 44,993 | 6,852 |
| SLAMStrike | 2 × AIM-9M Sidewinder; 2 × AGM-84E SLAM; 1 × EO weapon control pod | Empty | Empty | 1,688 | 14,897 | 43,529 | 8,316 |

## FB-111N MudPig — 2003

ID: `ran_fb-111n_2003`. Role: Bomber. Empty: 26,900 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 2 × AGM-84L Harpoon Block II | Empty | Empty | 1,228 | 14,897 | 43,569 | 8,276 |
| AirToAir | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 42,997 | 8,848 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,402 | 18,437 | 47,283 | 4,562 |
| FleetIntercept | 2 × ASRAAM; 2 × AIM-120C-5 AMRAAM; 2 × AIM-54C Phoenix | Empty | Empty | 1,406 | 14,897 | 43,747 | 8,098 |
| AntiShip | 2 × ASRAAM; 2 × AGM-84L Harpoon Block II | Empty | Empty | 1,228 | 14,897 | 43,569 | 8,276 |
| AntiShipHeavy | 4 × AGM-84L Harpoon Block II | Empty | 3 × AGM-84L Harpoon Block II | 3,682 | 14,897 | 46,023 | 5,822 |
| AntiShipLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × AGM-84L Harpoon Block II | Empty | 3 × AGM-84L Harpoon Block II | 3,106 | 18,437 | 48,987 | 2,858 |
| Strike | 2 × ASRAAM; 24 × Mk 82 on six-bomb rack | Empty | Empty | 6,024 | 14,897 | 48,365 | 3,480 |
| StrikeLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | Empty | 3,400 | 18,437 | 49,281 | 2,564 |
| StrikeHeavy | 2 × ASRAAM; 4 × Mk 84 2000-lb GP bomb | Empty | Empty | 3,804 | 14,897 | 46,145 | 5,700 |
| StrikeHeavyLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | Empty | 2,290 | 18,437 | 48,171 | 3,674 |
| StrikeMedium | 2 × ASRAAM; 4 × Mk 83 1000-lb GP bomb | Empty | Empty | 1,992 | 14,897 | 44,333 | 7,512 |
| StrikePrecision | 2 × ASRAAM; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 3,128 | 14,897 | 45,469 | 6,376 |
| StrikePrecisionLight | 2 × ASRAAM; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,157 | 14,897 | 43,498 | 8,347 |
| StrikePrecisionMedium | 2 × ASRAAM; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,811 | 14,897 | 44,152 | 7,693 |
| StrikePrecisionLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | Empty | 1,560 | 18,437 | 47,441 | 4,404 |
| MaverickStrike | 2 × ASRAAM; 4 × AGM-65G Maverick | Empty | Empty | 1,384 | 14,897 | 43,725 | 8,120 |
| SEAD | 2 × ASRAAM; 4 × AGM-88C HARM | Empty | Empty | 1,620 | 14,897 | 43,961 | 7,884 |
| EW | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 46,877 | 4,968 |
| EWLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 46,877 | 4,968 |
| EscortSEAD | 2 × ASRAAM; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 1,418 | 14,897 | 43,759 | 8,086 |
| ReconLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,197 | 1,648 |
| EOGlideStrike | 2 × ASRAAM; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,696 | 14,897 | 45,037 | 6,808 |
| StrikePavewayIII | 2 × ASRAAM; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | Empty | 3,578 | 14,897 | 45,919 | 5,926 |
| PopeyeStrike | 2 × ASRAAM; 2 × AGM-142 Popeye / Have Nap; 1 × EO weapon control pod | Empty | Empty | 3,156 | 14,897 | 45,497 | 6,348 |
| SLAMStrike | 2 × ASRAAM; 2 × AGM-84E SLAM; 1 × EO weapon control pod | Empty | Empty | 1,692 | 14,897 | 44,033 | 7,812 |
| SLAMERStrike | 2 × ASRAAM; 2 × AGM-84K SLAM-ER; 1 × EO weapon control pod | Empty | Empty | 1,786 | 14,897 | 44,127 | 7,718 |
| JDAMHeavy | 2 × ASRAAM; 4 × GBU-31 JDAM Mk 84 | Empty | Empty | 3,876 | 14,897 | 46,217 | 5,628 |
| JDAMMedium | 2 × ASRAAM; 4 × GBU-32 JDAM Mk 83 | Empty | Empty | 2,020 | 14,897 | 44,361 | 7,484 |
| JSOWStrike | 2 × ASRAAM; 4 × AGM-154A JSOW | Empty | Empty | 2,108 | 14,897 | 44,449 | 7,396 |

## RF-111N SprintPig — 1980

ID: `ran_rf-111n`. Role: Recon,ESM. Empty: 25,350 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| AirToAir | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| Recon | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| ReconLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| ReconFast | 2 × AIM-9L Sidewinder | Empty | Empty | 172 | 14,897 | 40,963 | 10,882 |

## RF-111N SprintPig — 1985

ID: `ran_rf-111n_1985`. Role: Recon,ESM. Empty: 25,650 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| AirToAir | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| Recon | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| ReconFast | 2 × AIM-9M Sidewinder | Empty | Empty | 172 | 14,897 | 41,263 | 10,582 |

## RF-111N SprintPig — 1995

ID: `ran_rf-111n_1995`. Role: Recon,ESM. Empty: 27,000 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| AirToAir | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| Recon | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| ReconFast | 2 × AIM-9M Sidewinder | Empty | Empty | 172 | 14,897 | 42,613 | 9,232 |

## RF-111N SprintPig — 2003

ID: `ran_rf-111n_2003`. Role: Recon,ESM. Empty: 27,600 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| AirToAir | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| AirToAirLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| Recon | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| ReconLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| ReconFast | 2 × ASRAAM | Empty | Empty | 176 | 14,897 | 43,217 | 8,628 |

## EF-111N ScreamPig — 1980

ID: `ran_ef-111n`. Role: EW,ESM. Empty: 28,250 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| AirToAir | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EW | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EWLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EscortSEAD | 2 × AIM-9L Sidewinder; 2 × AGM-78 Standard ARM; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 1,932 | 14,897 | 45,079 | 6,766 |

## EF-111N ScreamPig — 1985

ID: `ran_ef-111n_1985`. Role: EW,ESM. Empty: 28,500 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| AirToAir | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88A HARM; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 1,414 | 14,897 | 44,811 | 7,034 |

## EF-111N ScreamPig — 1995

ID: `ran_ef-111n_1995`. Role: EW,ESM. Empty: 29,750 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| AirToAir | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 1,414 | 14,897 | 46,061 | 5,784 |

## EF-111N ScreamPig — 2003

ID: `ran_ef-111n_2003`. Role: EW,ESM. Empty: 30,250 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| AirToAir | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EW | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EWLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EscortSEAD | 2 × ASRAAM; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 1,418 | 14,897 | 46,565 | 5,280 |

## Every local store definition

Dated aliases use the same physical store geometry and mass with year-specific sensors. Unselected legacy definitions are retained for compatibility; 61 definitions do not mean 61 different weapon designs. Tank shell mass excludes fuel.

| ID | Name | Mass kg | Fuel kg | Earliest edition | Used in presets | Simulation/geometry notes |
|---|---|---|---|---|---|---|
| ran_nw_aim9l | AIM-9L Sidewinder | 86 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_aim9m | AIM-9M Sidewinder | 86 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_aim7f | AIM-7F Sparrow | 231 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_aim7m | AIM-7M Sparrow | 231 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_aim54a | AIM-54A Phoenix | 443 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_aim54c | AIM-54C Phoenix | 463 | 0 | 1985 | Yes | Native AIM-54A geometry and flight profile with C mass and estimated improved ECCM |
| ran_nw_aim120b | AIM-120B AMRAAM | 152 | 0 | 1995 | Yes | Active radar homing; no simulated launch-platform midcourse datalink; engagement range is a game estimate, not a published missile limit |
| ran_nw_aim120c5 | AIM-120C-5 AMRAAM | 152 | 0 | 2003 | Yes | Active radar homing; no simulated launch-platform midcourse datalink; engagement range is a game estimate, not a published missile limit; C-5 ECCM is an estimated improvement over B |
| ran_nw_asraam | ASRAAM | 88 | 0 | 2003 | Yes | Native IR homing approximation; no helmet sight or lock-on-after-launch simulation |
| ran_nw_harpoona | AGM-84A Harpoon | 526 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_harpoonc | AGM-84C Harpoon | 526 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_harpoond | AGM-84D Harpoon Block 1C | 526 | 0 | 1995 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_harpoonl | AGM-84L Harpoon Block II | 526 | 0 | 2003 | Yes | Block II acquisition/integration assumed. Native radar-homing ship attack only; GPS route planning and coastal land-attack mode are not simulated |
| ran_nw_maverickb | AGM-65B Maverick | 208 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_maverickd | AGM-65D Maverick | 218 | 0 | 1985 | Yes | Native Maverick geometry with IIR homing and selected variant mass |
| ran_nw_maverickg | AGM-65G Maverick | 302 | 0 | 1995 | Yes | Native Maverick geometry with IIR homing and selected variant mass |
| ran_nw_standardarm | AGM-78 Standard ARM | 620 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_shrike | AGM-45 Shrike | 178 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_harma | AGM-88A HARM | 361 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_harmc | AGM-88C HARM | 361 | 0 | 1995 | Yes | Native HARM-A geometry/flight model with estimated C seeker resilience |
| ran_nw_mk82 | Mk 82 500-lb GP bomb | 227 | 0 | 1980 | Compatibility definition | Native guidance; rounded historical carried mass |
| ran_nw_mk83 | Mk 83 1000-lb GP bomb | 454 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_mk84 | Mk 84 2000-lb GP bomb | 907 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_gbu10 | GBU-10 Paveway II | 934 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_gbu12 | GBU-12 Paveway II | 277 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_gbu16 | GBU-16 Paveway II | 495 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_gbu15 | GBU-15 electro-optical glide bomb | 1,130 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_gbu24 | GBU-24 Paveway III | 1,084 | 0 | 1985 | Yes | Native guidance; rounded historical carried mass |
| ran_nw_popeye | AGM-142 Popeye / Have Nap | 1,360 | 0 | 1995 | Yes | Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated |
| ran_nw_slam | AGM-84E SLAM | 628 | 0 | 1995 | Yes | Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated |
| ran_nw_slamer | AGM-84K SLAM-ER | 675 | 0 | 2003 | Yes | Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated |
| ran_nw_gbu31 | GBU-31 JDAM Mk 84 | 925 | 0 | 2003 | Yes | Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation |
| ran_nw_gbu32 | GBU-32 JDAM Mk 83 | 461 | 0 | 2003 | Yes | Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation |
| ran_nw_jsowa | AGM-154A JSOW | 483 | 0 | 2003 | Yes | Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation |
| ran_tank_600_f111n | 600 US-gallon fuel tank | 150 | 1770 | 1980 | Yes | Fuel from flight-manual capacity table; dry shell mass is an engineering allowance |
| ran_tank_600_fb111n | 600 US-gallon fuel tank | 150 | 1770 | 1980 | Yes | Fuel from flight-manual capacity table; dry shell mass is an engineering allowance |
| ran_tank_600_rf111n | 600 US-gallon fuel tank | 150 | 1770 | 1980 | Yes | Fuel from flight-manual capacity table; dry shell mass is an engineering allowance |
| ran_tank_600_ef111n | 600 US-gallon fuel tank | 150 | 1770 | 1980 | Yes | Fuel from flight-manual capacity table; dry shell mass is an engineering allowance |
| ran_alq-131n_1 | Naval offensive ECM pod 1 | 260 | 0 | 1980 | Compatibility definition | Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation |
| ran_nw_ecmpod_1 | MudPig removable offensive ECM pod 1 | 260 | 0 | 1980 | Compatibility definition | Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation |
| ran_alq-131n_2 | Naval offensive ECM pod 2 | 260 | 0 | 1980 | Compatibility definition | Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation |
| ran_nw_ecmpod_2 | MudPig removable offensive ECM pod 2 | 260 | 0 | 1980 | Compatibility definition | Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation |
| ran_nw_datalink | EO weapon control pod | 260 | 0 | 1985 | Yes | Estimated pod mass with existing pod geometry and native sensor; full historical pod shape is not reproduced |
| ran_nw_laserpod | External laser designation pod | 150 | 0 | 1980 | Yes | Estimated pod mass with existing pod geometry and native sensor; full historical pod shape is not reproduced |
| ran_nw_mk82_mer | Mk 82 on six-bomb rack | 243.7 | 0 | 1980 | Yes | 227 kg nominal bomb plus one-sixth of an estimated 100 kg detachable MER; no separate unsupported hardpoint mass key |
| ran_alq-131n_1_1980 | Naval offensive ECM pod 1 (1980) | 260 | 0 | 1980 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_1_1980 | Naval offensive ECM pod 1 (1980) | 260 | 0 | 1980 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_2_1980 | Naval offensive ECM pod 2 (1980) | 260 | 0 | 1980 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_2_1980 | Naval offensive ECM pod 2 (1980) | 260 | 0 | 1980 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_1_1985 | Naval offensive ECM pod 1 (1985) | 260 | 0 | 1985 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_1_1985 | Naval offensive ECM pod 1 (1985) | 260 | 0 | 1985 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_2_1985 | Naval offensive ECM pod 2 (1985) | 260 | 0 | 1985 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_2_1985 | Naval offensive ECM pod 2 (1985) | 260 | 0 | 1985 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_1_1995 | Naval offensive ECM pod 1 (1995) | 260 | 0 | 1995 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_1_1995 | Naval offensive ECM pod 1 (1995) | 260 | 0 | 1995 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_2_1995 | Naval offensive ECM pod 2 (1995) | 260 | 0 | 1995 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_2_1995 | Naval offensive ECM pod 2 (1995) | 260 | 0 | 1995 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_1_2003 | Naval offensive ECM pod 1 (2003) | 260 | 0 | 2003 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_1_2003 | Naval offensive ECM pod 1 (2003) | 260 | 0 | 2003 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_alq-131n_2_2003 | Naval offensive ECM pod 2 (2003) | 260 | 0 | 2003 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |
| ran_nw_ecmpod_2_2003 | Naval offensive ECM pod 2 (2003) | 260 | 0 | 2003 | Yes | Two physical pods with dated native jammer power/channels; fictional programme ratings. |

## Preserved design and simulation limits

MudPig AntiShip is two wing Harpoons/two IR missiles with empty bay; AntiShipHeavy is four wing and three bay Harpoons; AntiShipLongRange is two wing and three bay Harpoons, two IR missiles and two tanks. Bay stations, concealment and doors are exact original definitions. The separately relocated M61 is fictional; no new gun fairing is drawn.

EF retains two physical pylon ECM pods and two offensive sensors. FB only carries removable offensive containers in its EW presets. Designation and EO control pods occupy counted external stations. Existing cockpit, model and landing animation geometry remains.

Native modern-weapon approximations: AMRAAM lacks platform midcourse correction; ASRAAM lacks helmet sight/LOAL; EO weapons lack manual man-in-the-loop retargeting; Block II Harpoon models radar-homing ship attack; JDAM/JSOW use CEP/ballistic/glide settings instead of full GPS/INS. Period choices assume funded Australian integration, including accelerated early procurement.

Static checks do not prove gun fire, release trajectories, AI Mach 3 behaviour, ECM display, date filtering or carrier landings. These still need Sea Power runtime testing. References (`HISTORICAL_REFERENCES.md` in the release) · Aircraft comparison (`docs/AIRCRAFT_COMPARISON.md` in the release) · Investment (`docs/INVESTMENT_PROGRAMME.md` in the release)

## Source references and credits

The following reference list is supplied with the release. N-family performance and naval modifications remain explicitly hypothetical.

V6 references checked 30 September 2026; V7 engine references checked 1 October 2026. All N-family procurement, integration and naval engineering are alternate-history assumptions. The historical reference baseline and estimated additions are separated in `loadout_manifest.json`.

| Primary/reference source | Used for |
|---|---|
| [RAAF A8-142 technical sheet](https://www.airforce.gov.au/sites/default/files/2023-07/F111%20A8-142.pdf) | 51,845 kg loaded maximum; 43.6/82.3 kN engine thrust; historical F-111C weapon capability. Its 24,270 kg empty figure includes Pave Tack; V6's common budget uses the basic reference below with an external designator instead. |
| [Queensland Air Museum specifications](https://www.qldairmuseum.au/qam-content/aircraft/specs/F-111-specs.htm) | 23,300 kg F-111C basic mass reference. |
| [Queensland Air Museum flight-manual fuel table](https://qldairmuseum.au/qam-content/aircraft/f-111/F-111-deliveries.htm) | Internal 14,897 kg and external 600 US-gallon fuel 1,770 kg at SG .78. Uses this later manual-based table rather than the inconsistent older specification-page conversions. |
| [USAF Museum EF-111A](https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/195968/general-dynamics-ef-111a-raven/) | Approximately four tons of integrated EW equipment; rounded role allowance. External naval pods are additional stores. |
| [USAF Sidewinder](https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104557/aim-9-sidewinder/) | M-model deliveries from 1983; approximately 86 kg launch mass. |
| [NAVAIR Phoenix history](https://www.navair.navy.mil/node/12701) | A before 1980, C early fleet deployment in 1985. 1985 Australian purchase is assumed; later C-plus upgrades are not silently used. |
| [USAF AMRAAM index](https://www.af.mil/About-Us/Fact-Sheets/Search/aim-120/) / [Air University 1998 review](https://www.airuniversity.af.mil/Portals/10/ASPJ/journals/Volume-12_Issue-1-4/1998_Vol12_No3.pdf) | 1991 operational introduction; appears in 1995/2003 only. Variant engagement ranges and ECCM are game estimates. |
| [MBDA ASRAAM](https://www.mbda-systems.com/products/air-dominance/asraam) / [1999 UK programme evidence](https://publications.parliament.uk/pa/cm199899/cmselect/cmdfence/544/544w09.htm) | 88 kg; period weapon programme. 2003 N-family integration is assumed. |
| [USAF Maverick](https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104577/agm-65-maverick/) | B/D/G seeker/mass differences; G deliveries from 1989. |
| [NAVAIR Harpoon](https://www.navair.navy.mil/harpoon) / [Boeing first Block II export delivery, 2002](https://boeing.mediaroom.com/2002-04-26-Boeing-Delivers-First-Harpoon-Block-II-Kits-to-Denmark) | Period maritime choices; 2003 Block II. Air-launched mass without surface booster is rounded to 526 kg. Native guidance is retained as a ship-attack approximation. |
| [US Navy HARM deployment history](https://www.history.navy.mil/about-us/leadership/director/directors-corner/in-memoriam/memoriam-newman.html) | Late-1985 HARM deployment; early Australian acquisition is fictional. |
| [USAF Gulf War Air Power Survey](https://media.defense.gov/2010/Sep/27/2001329817/-1/-1/0/AFD-100927-066.pdf) | Period guided weapons including the 3,000-pound AGM-142. Popeye carried mass 1,360 kg; 1995 Australian integration is accelerated relative to actual history. |
| [USAF TO 1-1M-34 hosted scan](https://www.scribd.com/document/793762586/TO-1-1M-34) | Guided bomb mass depends on kit/fuze. Catalogue uses rounded selected Paveway configurations: 934 / 277 / 495 / 1,084 kg for GBU-10/12/16/24. GP bombs retain nominal class mass. |
| [USAF JDAM](https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104572/joint-direct-attack-munition-gbu-313238/joint-direct-attack-munition-gbu-313238/) / [Boeing production card](https://www.boeing.com/content/dam/boeing/boeingdotcom/defense/weapons-weapons/images/jdam_product_card.pdf) | 1998 production/1999 deployment; approximately 925/461 kg GBU-31/32. Only 2003 editions. Native CEP approximation, not full GPS simulation. |
| [NAVAIR JSOW](https://www.navair.navy.mil/product/jsow) | January 1999 deployment; approximately 483 kg AGM-154A. No later C-1 maritime/datalink capability. |
| [US Navy SLAM-ER](https://www.navy.mil/DesktopModules/ArticleCS/Print.aspx?Article=2168997&ModuleId=4201&PortalId=1) | June 2000 IOC; approximately 675 kg; 2003 fit. |
| [Native Sea Power data](https://github.com/SEST-HOBBY/Seapower-mods/tree/feature/northern-front-iii-export/mods-source/_vanilla/original) | Supported schema, M61/20 mm ammunition, stock models, guidance and sensors. Native .272 kg round mass used for the gun budget. |

Estimated additions, not measured historical values: naval conversion 950 kg; relocated M61 hardware/feed/housing 650 kg; fighter radar 350 kg; recon kit 450 kg; avionics growth 0/100/250/400 kg; dry tank shell 150 kg; rack 100 kg; designator 150 kg; EO control pod 260 kg. The early naval laser fit and later modern-weapon choices assume aircraft wiring, software, control interfaces, pylon engineering and trials.

The preserved internal bay, relocated gun and SprintPig speed are explicit fictional design requirements. A historical mass reference is not proof of the aerodynamic, structural or carrier suitability of those changes.

## V7 propulsion references and estimates

[GE historical military engine status report](https://www.geaerospace.com/news/press-releases/defense-engines/ge-aircraft-engines-military-engine-status-report) gives the F110-GE-400 120 kN afterburning class in operational service from April 1988 and the F110-GE-129 129 kN class from April 1992. These support the chosen 1995/2003 supplier classes; they do not establish an actual F-111 retrofit. [GE F110 datasheet](https://www.geaerospace.com/sites/default/files/2022-02/F110-Datasheet.pdf) is additional family context; later engine upgrades are not silently assigned to early editions.

V7 adds systems/control allowances 0/150/650/850 kg; propulsion-retrofit allowances 0/0/600/750 kg; RF thermal allowances 0/50/150/250 kg, alongside the existing edition-avionics allowance. These are explicit engineering estimates. Installed dry thrust, TF30 uprating, F-111 naval adaptation, control/sensor/readiness ratings, nominal range growth and RF Mach 3 propulsion are fictional. The TPS-inspired RGB palette is an uncalibrated screen approximation, not a certified paint standard or historical USN F-111 scheme.

## Asset credits

| Source | Contribution |
|---|---|
| [Workshop 3587484531](https://steamcommunity.com/sharedfiles/filedetails/?id=3587484531) | Source aircraft/EF models and associated materials inherited through V6 |
| [Workshop 3689650533](https://steamcommunity.com/sharedfiles/filedetails/?id=3689650533) | Source F-111/RF models and materials inherited through V6 |
| Earlier RAN F-111N Naval Wing releases | Fictional naval role/model definitions, corrected RAN maps, internal bay and carrier support |
| [Australian roundel SVG](https://commons.wikimedia.org/wiki/File:Roundel_of_Australia.svg) | Original roundel vector; V7 adds a subdued colour variant |
| [SEST-HOBBY native export](https://github.com/SEST-HOBBY/Seapower-mods/tree/feature/northern-front-iii-export/mods-source/_vanilla/original) | Native schema, ammunition/sensors and representative carrier references |
| Sea Power | Stock assets and systems referenced at runtime; stock weapon models are not copied solely for previews |

V7 adds programme configuration, authored surface materials/vector decal projection, build/validation utilities, simplified modern-weapon geometry inherited from V6, and documentation. It does not transfer ownership or assign a new blanket licence to third-party assets; original rights and upstream terms remain with their respective owners. No government, armed-service, manufacturer or game-publisher affiliation is implied.
