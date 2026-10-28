# V8 Australian investment programme

Every edition assumes heavy Australian funding for naval conversion, propulsion, flight controls, weapons integration, targeting and EW. Native settings improve by year. They are hypothetical programme ratings, not measured historical N-family performance.

| Setting | 1980 | 1985 | 1995 | 2003 |
|---|---|---|---|---|
| Engine for all roles | TF30-P-109 reference | TF30 naval uprating (fictional) | F110-GE-400-class naval adaptation | F110-GE-129-class naval adaptation |
| Dry thrust N/engine for all roles | 43600 | 47960 | 60000 | 65000 |
| Afterburning thrust N/engine for all roles | 82300 | 90530 | 120000 | 129000 |
| Velocity/thrust response multiplier | 1 | 1.1 | 1.25 | 1.4 |
| Pitch/heading/bank gain multiplier | 1 | 1.05 | 1.1 | 1.15 |
| Nominal cruise-range factor | 1 | 1.06 | 1.14 | 1.22 |
| Cruise Mach for all roles | 0.842269 | 0.842269 | 0.842269 | 0.842269 |
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

## Forward radar coverage

| Edition | WaterPig / Phoenix azimuth | Total degrees | MudPig / SprintPig / ScreamPig azimuth | Total degrees |
|---|---|---|---|---|
| 1980 | -65,65 | 130 | -45,45 | 90 |
| 1985 | -70,70 | 140 | -55,55 | 110 |
| 1995 | -80,80 | 160 | -65,65 | 130 |
| 2003 | -85,85 | 170 | -75,75 | 150 |

Coverage widens with funded antenna and processing upgrades in the alternate timeline. These are fictional gameplay ratings, not historical F-111 scan limits. Phoenix control follows the fleet radar sector in every edition, including MudPig's wing and bay controllers. Native vertical arcs, target altitude limits, radar roles and datalink policy are retained. [Unit Reference details and test](RADAR_REFERENCE_V8.md).

F uses AWG-9 donor geometry/settings, labelled as a hypothetical APG-71-class digital adaptation from 1995. The other roles use APQ-161 native settings to represent naval multimode radar. No new radar/flight simulation engine, interactive digital cockpit or MFD mesh is introduced. The nominal range factor does not guarantee an equivalent increase in combat radius.

| RF propulsion setting | 1980 | 1985 | 1995 | 2003 |
|---|---|---|---|---|
| Dry N per engine | 43600 | 47960 | 60000 | 65000 |
| Afterburning N per engine | 82300 | 90530 | 120000 | 129000 |

The speed correction supersedes the former RF-only Mach 3, Mach 2.52 cruise, oversized thrust and triple response. All roles use maximum Mach 2.875, sourced cruise Mach 0.842269 and an 835.178186-knot sea-level cap. The normal-power game command follows cruise; it is not a claimed historical maximum dry-thrust speed. Dated propulsion and response remain estimated. Landing, loiter and stall settings retain the original values. Use independent orders and suitable altitude to assess maximum speed; actual AI flight needs runtime testing.

GE's historical status report supplies the 120 kN F110-GE-400 and 129 kN F110-GE-129 afterburning classes, available before the assigned editions. F-111 adaptation, installed dry thrust, TF30 uprating, mass allowances, thermal upgrades and control/sensor ratings are estimates. [GE reference](https://www.geaerospace.com/news/press-releases/defense-engines/ge-aircraft-engines-military-engine-status-report). The 15% speed increase is a requested fictional gameplay rating. NASA describes Mach 2.5 capability for the F-111A: [technical report](https://ntrs.nasa.gov/api/citations/19730021074/downloads/19730021074.pdf). RAAF reference sea-level 1,345 km/h and cruise 778 km/h are boosted to 1,546.75 and 894.7 km/h. The cruise Mach conversion assumes ISA at 37,000 ft; [RAAF reference](https://www.airforce.gov.au/sites/default/files/2023-07/F111%20A8-142.pdf). The source does not establish a maximum dry-thrust speed; the normal-power command is conservatively set to the sourced cruise target. These speed targets do not turn the estimated propulsion, fuel/range or flight model into a certified real-world envelope.

[Aircraft comparison](AIRCRAFT_COMPARISON.md) · [Full mass/loadout breakdown](../COMPLETE_BREAKDOWN_V8.md)
