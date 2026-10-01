# V7 Australian investment programme

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

GE's historical status report supplies the 120 kN F110-GE-400 and 129 kN F110-GE-129 afterburning classes, available before the assigned editions. F-111 adaptation, installed dry thrust, TF30 uprating, mass allowances, thermal upgrades and control/sensor ratings are estimates. [GE reference](https://www.geaerospace.com/news/press-releases/defense-engines/ge-aircraft-engines-military-engine-status-report). The RF package is entirely fictional.

[Aircraft comparison](AIRCRAFT_COMPARISON.md) · [Full mass/loadout breakdown](../COMPLETE_BREAKDOWN_V7.md)
