# RAN F-111N Naval Wing V8 — Complete Breakdown

Version 8 internal-bay update, 2 October 2026. Four families in four editions: 16 aircraft, 211 selectable presets and 61 local store definitions. The 167-preset V6 baseline is expanded with 44 new MudPig bay fits. Station geometry, concealment, door actions, original models and carrier/landing settings are retained. Targeting and estimated bay-upgrade mass are updated.

Use the release installer to refresh V8. Enable it with priority over carrier mods, keep required source assets enabled and restart. Select dated aircraft in carrier air groups; unsuffixed IDs are 1980. Armed recovery and release still require in-game testing.

## V8: all sixteen aircraft compared

Four original roles, each in four funded editions. Values below come from the shipped configuration and manifests. Empty masses and naval upgrades are estimates. Maximum/cruise Mach values are settings, not verified flight results. Range is the nominal native Miles field, not combat radius.

| Aircraft | Year | Role | Empty kg | Max Mach | Cruise Mach | Range miles | AB kN/engine | Gun / rounds | Presets | Suggested fit |
|---|---|---|---|---|---|---|---|---|---|---|
| F-111N WaterPig | 1980 | Fighter | 25,250 | 2.5 | 0.84 | 1,450 | 82.3 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 1985 | Fighter | 25,500 | 2.5 | 0.88 | 1,537 | 90.53 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 1995 | Fighter | 26,750 | 2.5 | 0.92 | 1,653 | 120 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| F-111N WaterPig | 2003 | Fighter | 27,250 | 2.5 | 0.96 | 1,769 | 129 | M61 / 2,000 | 4 | FleetIntercept / AirToAirLongRange |
| FB-111N MudPig | 1980 | Bomber | 24,940 | 2.6 | 0.84 | 1,550 | 82.3 | M61 / 2,000 | 33 | AntiShipHeavy / StrikeBay / FleetInterceptBay |
| FB-111N MudPig | 1985 | Bomber | 25,200 | 2.6 | 0.88 | 1,643 | 90.53 | M61 / 2,000 | 34 | AntiShipHeavy / StrikeBay / FleetInterceptBay |
| FB-111N MudPig | 1995 | Bomber | 26,460 | 2.6 | 0.92 | 1,767 | 120 | M61 / 2,000 | 36 | AntiShipHeavy / StrikeBay / FleetInterceptBay |
| FB-111N MudPig | 2003 | Bomber | 26,975 | 2.6 | 0.96 | 1,891 | 129 | M61 / 2,000 | 44 | AntiShipHeavy / StrikeBay / FleetInterceptBay |
| RF-111N SprintPig | 1980 | Recon,ESM | 25,350 | 3.0 | 2.52 | 2,300 | 480 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 1985 | Recon,ESM | 25,650 | 3.0 | 2.52 | 2,438 | 528 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 1995 | Recon,ESM | 27,000 | 3.0 | 2.52 | 2,622 | 600 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| RF-111N SprintPig | 2003 | Recon,ESM | 27,600 | 3.0 | 2.52 | 2,806 | 672 | M61 / 2,000 | 6 | ReconFast / ReconLongRange |
| EF-111N ScreamPig | 1980 | EW,ESM | 28,250 | 2.2 | 0.84 | 1,700 | 82.3 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 1985 | EW,ESM | 28,500 | 2.2 | 0.88 | 1,802 | 90.53 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 1995 | EW,ESM | 29,750 | 2.2 | 0.92 | 1,938 | 120 | None | 6 | EWLongRange / EscortSEAD |
| EF-111N ScreamPig | 2003 | EW,ESM | 30,250 | 2.2 | 0.96 | 2,074 | 129 | None | 6 | EWLongRange / EscortSEAD |

RF uses its explicit fictional Mach 3 propulsion package and triple WaterPig velocity/thrust gains for the same year. FB carries the other families' period weapon types, while F/RF/EF preserve specialised roles. EF always has two physical ECM pods and two offensive systems; FB receives removable offensive ECM only in its EW fits.

The 211 selectable preset names include compatible Default/mission aliases with repeated inventories. Counts by year are 49 / 50 / 52 / 60. Service gates are 1980–1984, 1985–1994, 1995–2002 and 2003–2050. Unsuffixed aircraft IDs select 1980.

[Complete loadouts and weight budgets](../COMPLETE_BREAKDOWN_V8.md) · [Internal bay](INTERNAL_BAY_V8.md) · [Investment details](INVESTMENT_PROGRAMME.md) · [Release notes](../RELEASE_NOTES_V8.md)

## V8 Australian investment programme

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

[Aircraft comparison](AIRCRAFT_COMPARISON.md) · [Full mass/loadout breakdown](../COMPLETE_BREAKDOWN_V8.md)

## V8 MudPig internal bay and armed carrier recovery

Version 8 retains three physical stations, original concealment and the Bay_Open/Bay_Close door actions. Bay targeting now includes the dedicated Phoenix controller. Single-store suspension adapters offset Phoenix 10 cm rearward and Shrike 50 cm rearward to accommodate their native origin/collider envelopes. The supplied carrier configuration has no condition requiring an empty bay for launch or recovery. Actual armed recovery has not been runtime-tested.

### Investment and capacity

Real Australian F-111 investment included Pave Tack/Harpoon and the Avionics Update Program. These naval bay integrations extend that history within the hypothetical Naval Wing programme; they are not historical F-111 certifications. Estimated adapters and interfaces add 40/50/60/75 kg to MudPig empty mass for 1980/1985/1995/2003. Bay readiness improves to 30/25/20/15 seconds with the existing dated programme. External designation/control pods leave the bay available.

| Internal store | Maximum selected | Editions |
|---|---|---|
| Mk 82 | 3 | All |
| Harpoon | 3 | All; edition-specific missile |
| Mk 83 / Mk 84 | 2 | All |
| GBU-12 | 2 | All; external laser pod |
| Maverick | 2 | All; edition-specific seeker |
| Phoenix | 2 | All; dedicated air-targeting controller |
| Shrike | 2 | 1980 Shrike fit |
| SLAM | 2 | 1995 / 2003; external control pod |
| GBU-31 / GBU-32 JDAM | 2 | 2003 only |

These are bounded, estimated integrations in the existing model. The three-Harpoon fit remains a fictional design requirement. No internal MER racks or stacked ammunition are added. Popeye, SLAM-ER and JSOW stay external; their shipped deployed-wing models and integration are not qualified for these internal stations. Larger Paveway/EO bombs stay external while smaller GBU-12s supplement precision fits.

### New bay mission presets

Each listed preset has a LongRange companion with two external fuel tanks. Offensive strike stores are internal; defensive IR missiles, tanks and the precision designation pod remain external. FleetInterceptBay also carries external BVR missiles.

| Preset | Internal stores | Editions |
|---|---|---|
| AntiShipBay | 3 Harpoons | All |
| StrikeBay | 3 Mk 82 | All |
| StrikeHeavyBay | 2 Mk 84 | All |
| StrikePrecisionBay | 2 GBU-12 | All |
| FleetInterceptBay | 2 Phoenix | All |
| JDAMBay | 2 GBU-32 | 2003 |
| JDAMHeavyBay | 2 GBU-31 | 2003 |

### Every loaded-bay fit and mass budget

| Edition | Preset | Internal bay | Full-fuel takeoff kg | Reference margin kg |
|---|---|---|---|---|
| 1980 | AntiShipHeavy | 3 × AGM-84A Harpoon | 44,063 | 7,782 |
| 1980 | AntiShipLongRange | 3 × AGM-84A Harpoon | 47,023 | 4,822 |
| 1980 | Strike | 3 × Mk 82 500-lb GP bomb | 47,082 | 4,763 |
| 1980 | StrikeLongRange | 3 × Mk 82 500-lb GP bomb | 47,998 | 3,847 |
| 1980 | StrikeHeavy | 2 × Mk 84 2000-lb GP bomb | 45,995 | 5,850 |
| 1980 | StrikeHeavyLongRange | 2 × Mk 84 2000-lb GP bomb | 48,021 | 3,824 |
| 1980 | StrikeMedium | 2 × Mk 83 1000-lb GP bomb | 43,277 | 8,568 |
| 1980 | StrikePrecision | 2 × GBU-12 Paveway II | 44,059 | 7,786 |
| 1980 | StrikePrecisionLight | 2 × GBU-12 Paveway II | 42,088 | 9,757 |
| 1980 | StrikePrecisionMedium | 2 × GBU-12 Paveway II | 42,742 | 9,103 |
| 1980 | StrikePrecisionLongRange | 2 × GBU-12 Paveway II | 46,031 | 5,814 |
| 1980 | MaverickStrike | 2 × AGM-65B Maverick | 41,801 | 10,044 |
| 1980 | SEADShrike | 2 × AGM-45 Shrike | 41,621 | 10,224 |
| 1980 | AntiShipBay | 3 × AGM-84A Harpoon | 42,131 | 9,714 |
| 1980 | StrikeBay | 3 × Mk 82 500-lb GP bomb | 41,234 | 10,611 |
| 1980 | StrikeHeavyBay | 2 × Mk 84 2000-lb GP bomb | 42,367 | 9,478 |
| 1980 | StrikePrecisionBay | 2 × GBU-12 Paveway II | 41,257 | 10,588 |
| 1980 | FleetInterceptBay | 2 × AIM-54A Phoenix | 41,901 | 9,944 |
| 1980 | AntiShipBayLongRange | 3 × AGM-84A Harpoon | 45,971 | 5,874 |
| 1980 | StrikeBayLongRange | 3 × Mk 82 500-lb GP bomb | 45,074 | 6,771 |
| 1980 | StrikeHeavyBayLongRange | 2 × Mk 84 2000-lb GP bomb | 46,207 | 5,638 |
| 1980 | StrikePrecisionBayLongRange | 2 × GBU-12 Paveway II | 45,097 | 6,748 |
| 1980 | FleetInterceptBayLongRange | 2 × AIM-54A Phoenix | 45,741 | 6,104 |
| 1985 | AntiShipHeavy | 3 × AGM-84C Harpoon | 44,323 | 7,522 |
| 1985 | AntiShipLongRange | 3 × AGM-84C Harpoon | 47,283 | 4,562 |
| 1985 | Strike | 3 × Mk 82 500-lb GP bomb | 47,342 | 4,503 |
| 1985 | StrikeLongRange | 3 × Mk 82 500-lb GP bomb | 48,258 | 3,587 |
| 1985 | StrikeHeavy | 2 × Mk 84 2000-lb GP bomb | 46,255 | 5,590 |
| 1985 | StrikeHeavyLongRange | 2 × Mk 84 2000-lb GP bomb | 48,281 | 3,564 |
| 1985 | StrikeMedium | 2 × Mk 83 1000-lb GP bomb | 43,537 | 8,308 |
| 1985 | StrikePrecision | 2 × GBU-12 Paveway II | 44,319 | 7,526 |
| 1985 | StrikePrecisionLight | 2 × GBU-12 Paveway II | 42,348 | 9,497 |
| 1985 | StrikePrecisionMedium | 2 × GBU-12 Paveway II | 43,002 | 8,843 |
| 1985 | StrikePrecisionLongRange | 2 × GBU-12 Paveway II | 46,291 | 5,554 |
| 1985 | MaverickStrike | 2 × AGM-65D Maverick | 42,121 | 9,724 |
| 1985 | StrikePavewayIII | 2 × GBU-12 Paveway II | 44,769 | 7,076 |
| 1985 | AntiShipBay | 3 × AGM-84C Harpoon | 42,391 | 9,454 |
| 1985 | StrikeBay | 3 × Mk 82 500-lb GP bomb | 41,494 | 10,351 |
| 1985 | StrikeHeavyBay | 2 × Mk 84 2000-lb GP bomb | 42,627 | 9,218 |
| 1985 | StrikePrecisionBay | 2 × GBU-12 Paveway II | 41,517 | 10,328 |
| 1985 | FleetInterceptBay | 2 × AIM-54C Phoenix | 42,201 | 9,644 |
| 1985 | AntiShipBayLongRange | 3 × AGM-84C Harpoon | 46,231 | 5,614 |
| 1985 | StrikeBayLongRange | 3 × Mk 82 500-lb GP bomb | 45,334 | 6,511 |
| 1985 | StrikeHeavyBayLongRange | 2 × Mk 84 2000-lb GP bomb | 46,467 | 5,378 |
| 1985 | StrikePrecisionBayLongRange | 2 × GBU-12 Paveway II | 45,357 | 6,488 |
| 1985 | FleetInterceptBayLongRange | 2 × AIM-54C Phoenix | 46,041 | 5,804 |
| 1995 | AntiShipHeavy | 3 × AGM-84D Harpoon Block 1C | 45,583 | 6,262 |
| 1995 | AntiShipLongRange | 3 × AGM-84D Harpoon Block 1C | 48,543 | 3,302 |
| 1995 | Strike | 3 × Mk 82 500-lb GP bomb | 48,602 | 3,243 |
| 1995 | StrikeLongRange | 3 × Mk 82 500-lb GP bomb | 49,518 | 2,327 |
| 1995 | StrikeHeavy | 2 × Mk 84 2000-lb GP bomb | 47,515 | 4,330 |
| 1995 | StrikeHeavyLongRange | 2 × Mk 84 2000-lb GP bomb | 49,541 | 2,304 |
| 1995 | StrikeMedium | 2 × Mk 83 1000-lb GP bomb | 44,797 | 7,048 |
| 1995 | StrikePrecision | 2 × GBU-12 Paveway II | 45,579 | 6,266 |
| 1995 | StrikePrecisionLight | 2 × GBU-12 Paveway II | 43,608 | 8,237 |
| 1995 | StrikePrecisionMedium | 2 × GBU-12 Paveway II | 44,262 | 7,583 |
| 1995 | StrikePrecisionLongRange | 2 × GBU-12 Paveway II | 47,551 | 4,294 |
| 1995 | MaverickStrike | 2 × AGM-65G Maverick | 43,885 | 7,960 |
| 1995 | StrikePavewayIII | 2 × GBU-12 Paveway II | 46,029 | 5,816 |
| 1995 | SLAMStrike | 2 × AGM-84E SLAM | 44,845 | 7,000 |
| 1995 | AntiShipBay | 3 × AGM-84D Harpoon Block 1C | 43,651 | 8,194 |
| 1995 | StrikeBay | 3 × Mk 82 500-lb GP bomb | 42,754 | 9,091 |
| 1995 | StrikeHeavyBay | 2 × Mk 84 2000-lb GP bomb | 43,887 | 7,958 |
| 1995 | StrikePrecisionBay | 2 × GBU-12 Paveway II | 42,777 | 9,068 |
| 1995 | FleetInterceptBay | 2 × AIM-54C Phoenix | 43,303 | 8,542 |
| 1995 | AntiShipBayLongRange | 3 × AGM-84D Harpoon Block 1C | 47,491 | 4,354 |
| 1995 | StrikeBayLongRange | 3 × Mk 82 500-lb GP bomb | 46,594 | 5,251 |
| 1995 | StrikeHeavyBayLongRange | 2 × Mk 84 2000-lb GP bomb | 47,727 | 4,118 |
| 1995 | StrikePrecisionBayLongRange | 2 × GBU-12 Paveway II | 46,617 | 5,228 |
| 1995 | FleetInterceptBayLongRange | 2 × AIM-54C Phoenix | 47,143 | 4,702 |
| 2003 | AntiShipHeavy | 3 × AGM-84L Harpoon Block II | 46,098 | 5,747 |
| 2003 | AntiShipLongRange | 3 × AGM-84L Harpoon Block II | 49,062 | 2,783 |
| 2003 | Strike | 3 × Mk 82 500-lb GP bomb | 49,121 | 2,724 |
| 2003 | StrikeLongRange | 3 × Mk 82 500-lb GP bomb | 50,037 | 1,808 |
| 2003 | StrikeHeavy | 2 × Mk 84 2000-lb GP bomb | 48,034 | 3,811 |
| 2003 | StrikeHeavyLongRange | 2 × Mk 84 2000-lb GP bomb | 50,060 | 1,785 |
| 2003 | StrikeMedium | 2 × Mk 83 1000-lb GP bomb | 45,316 | 6,529 |
| 2003 | StrikePrecision | 2 × GBU-12 Paveway II | 46,098 | 5,747 |
| 2003 | StrikePrecisionLight | 2 × GBU-12 Paveway II | 44,127 | 7,718 |
| 2003 | StrikePrecisionMedium | 2 × GBU-12 Paveway II | 44,781 | 7,064 |
| 2003 | StrikePrecisionLongRange | 2 × GBU-12 Paveway II | 48,070 | 3,775 |
| 2003 | MaverickStrike | 2 × AGM-65G Maverick | 44,404 | 7,441 |
| 2003 | StrikePavewayIII | 2 × GBU-12 Paveway II | 46,548 | 5,297 |
| 2003 | SLAMStrike | 2 × AGM-84E SLAM | 45,364 | 6,481 |
| 2003 | JDAMHeavy | 2 × GBU-31 JDAM Mk 84 | 48,142 | 3,703 |
| 2003 | JDAMMedium | 2 × GBU-32 JDAM Mk 83 | 45,358 | 6,487 |
| 2003 | AntiShipBay | 3 × AGM-84L Harpoon Block II | 44,170 | 7,675 |
| 2003 | StrikeBay | 3 × Mk 82 500-lb GP bomb | 43,273 | 8,572 |
| 2003 | StrikeHeavyBay | 2 × Mk 84 2000-lb GP bomb | 44,406 | 7,439 |
| 2003 | StrikePrecisionBay | 2 × GBU-12 Paveway II | 43,296 | 8,549 |
| 2003 | FleetInterceptBay | 2 × AIM-54C Phoenix | 43,822 | 8,023 |
| 2003 | JDAMBay | 2 × GBU-32 JDAM Mk 83 | 43,514 | 8,331 |
| 2003 | JDAMHeavyBay | 2 × GBU-31 JDAM Mk 84 | 44,442 | 7,403 |
| 2003 | AntiShipBayLongRange | 3 × AGM-84L Harpoon Block II | 48,010 | 3,835 |
| 2003 | StrikeBayLongRange | 3 × Mk 82 500-lb GP bomb | 47,113 | 4,732 |
| 2003 | StrikeHeavyBayLongRange | 2 × Mk 84 2000-lb GP bomb | 48,246 | 3,599 |
| 2003 | StrikePrecisionBayLongRange | 2 × GBU-12 Paveway II | 47,136 | 4,709 |
| 2003 | FleetInterceptBayLongRange | 2 × AIM-54C Phoenix | 47,662 | 4,183 |
| 2003 | JDAMBayLongRange | 2 × GBU-32 JDAM Mk 83 | 47,354 | 4,491 |
| 2003 | JDAMHeavyBayLongRange | 2 × GBU-31 JDAM Mk 84 | 48,282 | 3,563 |

### Armed recovery test in Sea Power

1. Enable the refreshed V8 and required carrier/source mods, then restart. Use the 2003 MudPig on a stock catapult carrier first.
2. Select StrikeHeavyBay (two internal Mk 84s), launch, issue independent flight orders and return without firing. Check approach, bay doors, touchdown and deck recovery.
3. Repeat with AntiShipBay, FleetInterceptBay, StrikePrecisionBay and JDAMHeavyBay; then check the generated RAN carrier overrides.
4. Test weapon release separately. Check that doors open for release, close afterwards and do not interfere with landing gear.

All budgets include full internal fuel, every carried store, external tank fuel and gun ammunition. The 51,845 kg reference is a takeoff budget, not an arrestor/catapult or maximum carrier-landing limit. A real recovery assessment must account for fuel and the carrier's arresting limits. Native collider/local-mesh envelopes are checked against the closed-door horizontal footprint for the additional weapon types. This coarse check does not establish three-dimensional packing or release clearance; the retained three-Harpoon fit remains a fictional requirement. Static configuration checks cannot certify armed recovery or release clearance.

[Real RAAF upgrades](https://www.airforce.gov.au/sites/default/files/2023-07/F111%20A8-142.pdf) · [Every loadout](../COMPLETE_BREAKDOWN_V8.md)

## V8 release notes

Version 8 internal-bay update: sixteen aircraft and 211 selectable presets, including 44 new MudPig bay mission fits. Existing bombing/precision/Maverick/SLAM/JDAM fits receive additional internal stores. Dated Australian investment and eight USN-inspired late liveries are retained. Original role/model/bay-station/landing contracts and M61/ECM/carrier arrangements remain. Native modern-weapon approximations and explicit hypothetical naval masses are documented.

| Verification | Status | Checks/maps |
|---|---|---|
| VALIDATION.json | PASS | 35186 |
| CARRIER_VALIDATION.json | PASS | 2243 |
| USN_TEXTURE_VALIDATION.json | PASS | 8 |

Heaviest full-fuel budget: ran_rf-111n_2003 / ReconLongRange at 50,897 kg, margin 948 kg. Python compilation and installer shell syntax are checked separately. ZIP integrity and SHA-256 are supplied with the package.

Carrier validation uses native and representative RAN/custom deck fixtures, not the user's exact installed RAN carriers. Installation checks cover staging, backups, source preservation and idempotence. Preview images render the shipped assets and omit stock weapon meshes unavailable outside the game.

**Runtime tested: no.** Sea Power is not installed here. Actual gun fire, guidance/release, date filtering, Mach 3 flight, ECM display and landings require in-game verification. No new DLL, interactive cockpit, real GPS weapon simulation or real carrier certification is claimed.

The README, all-aircraft/system comparisons, every loadout/mass breakdown, CSV/JSON data, references, Steam description, credits, authoring sources and validation reports are included. GitHub publication is separate from this downloadable release.

## V8 complete aircraft, loadout and mass breakdown

Generated from the shipped INIs and manifests. All 16 aircraft, all 211 selectable presets and all 61 local store definitions are listed. Compatible aliases may carry identical stores. Values are rounded carried-mass budgets; fictional naval equipment and retrofit allowances are explicit.

### Empty mass components

The basic reference is 23,300 kg F-111C. Bay station/door geometry is retained; MudPig multistore adapters and interfaces receive explicit estimated mass allowances of 40/50/60/75 kg. Every version has 14,897 kg internal fuel; tank fuel and M61 ammunition are separate from empty mass.

| Aircraft | Year | Basic reference kg | Naval kg | Role kg | Gun hardware kg | Edition avionics kg | Bay upgrade kg | Systems/controls kg | Propulsion kg | RF thermal kg | Total kg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-111N | 1980 | 23,300 | 950 | 350 | 650 | 0 | 0 | 0 | 0 | 0 | 25,250 |
| F-111N | 1985 | 23,300 | 950 | 350 | 650 | 100 | 0 | 150 | 0 | 0 | 25,500 |
| F-111N | 1995 | 23,300 | 950 | 350 | 650 | 250 | 0 | 650 | 600 | 0 | 26,750 |
| F-111N | 2003 | 23,300 | 950 | 350 | 650 | 400 | 0 | 850 | 750 | 0 | 27,250 |
| FB-111N | 1980 | 23,300 | 950 | 0 | 650 | 0 | 40 | 0 | 0 | 0 | 24,940 |
| FB-111N | 1985 | 23,300 | 950 | 0 | 650 | 100 | 50 | 150 | 0 | 0 | 25,200 |
| FB-111N | 1995 | 23,300 | 950 | 0 | 650 | 250 | 60 | 650 | 600 | 0 | 26,460 |
| FB-111N | 2003 | 23,300 | 950 | 0 | 650 | 400 | 75 | 850 | 750 | 0 | 26,975 |
| RF-111N | 1980 | 23,300 | 950 | 450 | 650 | 0 | 0 | 0 | 0 | 0 | 25,350 |
| RF-111N | 1985 | 23,300 | 950 | 450 | 650 | 100 | 0 | 150 | 0 | 50 | 25,650 |
| RF-111N | 1995 | 23,300 | 950 | 450 | 650 | 250 | 0 | 650 | 600 | 150 | 27,000 |
| RF-111N | 2003 | 23,300 | 950 | 450 | 650 | 400 | 0 | 850 | 750 | 250 | 27,600 |
| EF-111N | 1980 | 23,300 | 950 | 4,000 | 0 | 0 | 0 | 0 | 0 | 0 | 28,250 |
| EF-111N | 1985 | 23,300 | 950 | 4,000 | 0 | 100 | 0 | 150 | 0 | 0 | 28,500 |
| EF-111N | 1995 | 23,300 | 950 | 4,000 | 0 | 250 | 0 | 650 | 600 | 0 | 29,750 |
| EF-111N | 2003 | 23,300 | 950 | 4,000 | 0 | 400 | 0 | 850 | 750 | 0 | 30,250 |

### Budget rules

- Each 600-US-gallon tank: 1,770 kg fuel plus estimated 150 kg dry shell. Two tanks give 18,437 kg total fuel; four give 21,977 kg.
- Fixed M61 hardware/feed/housing allowance: 650 kg within F/FB/RF empty mass. Loaded 2,000-round magazine: another 544 kg. EF has no gun.
- Mk 82 six-bomb racks include one-sixth of an estimated 100 kg rack per bomb.
- Full-fuel takeoff budget = empty mass + dry stores/rack allowances + internal/external fuel + gun ammunition.
- Every preset is checked against the 51,845 kg F-111C reference maximum. This is not a carrier catapult/arrestor certification.

### F-111N WaterPig — 1980

ID: `ran_f-111n`. Role: Fighter. Empty: 25,250 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,497 | 10,348 |
| AirToAir | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,497 | 10,348 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54A Phoenix | Empty | 1,358 | 18,437 | 45,589 | 6,256 |
| FleetIntercept | 2 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | 2 × AIM-54A Phoenix | Empty | 1,520 | 14,897 | 42,211 | 9,634 |

### F-111N WaterPig — 1985

ID: `ran_f-111n_1985`. Role: Fighter. Empty: 25,500 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,747 | 10,098 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,747 | 10,098 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,398 | 18,437 | 45,879 | 5,966 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | 2 × AIM-54C Phoenix | Empty | 1,560 | 14,897 | 42,501 | 9,344 |

### F-111N WaterPig — 1995

ID: `ran_f-111n_1995`. Role: Fighter. Empty: 26,750 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,839 | 9,006 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,839 | 9,006 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,398 | 18,437 | 47,129 | 4,716 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | 2 × AIM-54C Phoenix | Empty | 1,402 | 14,897 | 43,593 | 8,252 |

### F-111N WaterPig — 2003

ID: `ran_f-111n_2003`. Role: Fighter. Empty: 27,250 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.5; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 43,347 | 8,498 |
| AirToAir | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 43,347 | 8,498 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | 2 × AIM-54C Phoenix | Empty | 1,402 | 18,437 | 47,633 | 4,212 |
| FleetIntercept | 2 × ASRAAM; 2 × AIM-120C-5 AMRAAM | 2 × AIM-54C Phoenix | Empty | 1,406 | 14,897 | 44,097 | 7,748 |

### FB-111N MudPig — 1980

ID: `ran_fb-111n`. Role: Bomber. Empty: 24,940 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 2 × AGM-84A Harpoon | Empty | Empty | 1,224 | 14,897 | 41,605 | 10,240 |
| AirToAir | 4 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | Empty | 806 | 14,897 | 41,187 | 10,658 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54A Phoenix | Empty | Empty | 1,358 | 18,437 | 45,279 | 6,566 |
| FleetIntercept | 2 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow; 2 × AIM-54A Phoenix | Empty | Empty | 1,520 | 14,897 | 41,901 | 9,944 |
| AntiShip | 2 × AIM-9L Sidewinder; 2 × AGM-84A Harpoon | Empty | Empty | 1,224 | 14,897 | 41,605 | 10,240 |
| AntiShipHeavy | 4 × AGM-84A Harpoon | Empty | 3 × AGM-84A Harpoon | 3,682 | 14,897 | 44,063 | 7,782 |
| AntiShipLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84A Harpoon | Empty | 3 × AGM-84A Harpoon | 3,102 | 18,437 | 47,023 | 4,822 |
| Strike | 2 × AIM-9L Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 6,701 | 14,897 | 47,082 | 4,763 |
| StrikeLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 4,077 | 18,437 | 47,998 | 3,847 |
| StrikeHeavy | 2 × AIM-9L Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 5,614 | 14,897 | 45,995 | 5,850 |
| StrikeHeavyLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 4,100 | 18,437 | 48,021 | 3,824 |
| StrikeMedium | 2 × AIM-9L Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | 2 × Mk 83 1000-lb GP bomb | 2,896 | 14,897 | 43,277 | 8,568 |
| StrikePrecision | 2 × AIM-9L Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 3,678 | 14,897 | 44,059 | 7,786 |
| StrikePrecisionLight | 2 × AIM-9L Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,707 | 14,897 | 42,088 | 9,757 |
| StrikePrecisionMedium | 2 × AIM-9L Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,361 | 14,897 | 42,742 | 9,103 |
| StrikePrecisionLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,110 | 18,437 | 46,031 | 5,814 |
| MaverickStrike | 2 × AIM-9L Sidewinder; 4 × AGM-65B Maverick | Empty | 2 × AGM-65B Maverick | 1,420 | 14,897 | 41,801 | 10,044 |
| SEAD | 2 × AIM-9L Sidewinder; 4 × AGM-78 Standard ARM | Empty | Empty | 2,652 | 14,897 | 43,033 | 8,812 |
| SEADShrike | 2 × AIM-9L Sidewinder; 4 × AGM-45 Shrike | Empty | 2 × AGM-45 Shrike | 1,240 | 14,897 | 41,621 | 10,224 |
| EW | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 44,913 | 6,932 |
| EWLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 44,913 | 6,932 |
| EscortSEAD | 2 × AIM-9L Sidewinder; 2 × AGM-78 Standard ARM; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 1,932 | 14,897 | 42,313 | 9,532 |
| ReconLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,233 | 3,612 |
| AntiShipBay | 2 × AIM-9L Sidewinder | Empty | 3 × AGM-84A Harpoon | 1,750 | 14,897 | 42,131 | 9,714 |
| StrikeBay | 2 × AIM-9L Sidewinder | Empty | 3 × Mk 82 500-lb GP bomb | 853 | 14,897 | 41,234 | 10,611 |
| StrikeHeavyBay | 2 × AIM-9L Sidewinder | Empty | 2 × Mk 84 2000-lb GP bomb | 1,986 | 14,897 | 42,367 | 9,478 |
| StrikePrecisionBay | 2 × AIM-9L Sidewinder; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 876 | 14,897 | 41,257 | 10,588 |
| FleetInterceptBay | 2 × AIM-9L Sidewinder; 2 × AIM-7F Sparrow | Empty | 2 × AIM-54A Phoenix | 1,520 | 14,897 | 41,901 | 9,944 |
| AntiShipBayLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × AGM-84A Harpoon | 2,050 | 18,437 | 45,971 | 5,874 |
| StrikeBayLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × Mk 82 500-lb GP bomb | 1,153 | 18,437 | 45,074 | 6,771 |
| StrikeHeavyBayLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 2 × Mk 84 2000-lb GP bomb | 2,286 | 18,437 | 46,207 | 5,638 |
| StrikePrecisionBayLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,176 | 18,437 | 45,097 | 6,748 |
| FleetInterceptBayLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-7F Sparrow | Empty | 2 × AIM-54A Phoenix | 1,820 | 18,437 | 45,741 | 6,104 |

### FB-111N MudPig — 1985

ID: `ran_fb-111n_1985`. Role: Bomber. Empty: 25,200 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × AGM-84C Harpoon | Empty | Empty | 1,224 | 14,897 | 41,865 | 9,980 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | Empty | 806 | 14,897 | 41,447 | 10,398 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,398 | 18,437 | 45,579 | 6,266 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow; 2 × AIM-54C Phoenix | Empty | Empty | 1,560 | 14,897 | 42,201 | 9,644 |
| AntiShip | 2 × AIM-9M Sidewinder; 2 × AGM-84C Harpoon | Empty | Empty | 1,224 | 14,897 | 41,865 | 9,980 |
| AntiShipHeavy | 4 × AGM-84C Harpoon | Empty | 3 × AGM-84C Harpoon | 3,682 | 14,897 | 44,323 | 7,522 |
| AntiShipLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84C Harpoon | Empty | 3 × AGM-84C Harpoon | 3,102 | 18,437 | 47,283 | 4,562 |
| Strike | 2 × AIM-9M Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 6,701 | 14,897 | 47,342 | 4,503 |
| StrikeLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 4,077 | 18,437 | 48,258 | 3,587 |
| StrikeHeavy | 2 × AIM-9M Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 5,614 | 14,897 | 46,255 | 5,590 |
| StrikeHeavyLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 4,100 | 18,437 | 48,281 | 3,564 |
| StrikeMedium | 2 × AIM-9M Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | 2 × Mk 83 1000-lb GP bomb | 2,896 | 14,897 | 43,537 | 8,308 |
| StrikePrecision | 2 × AIM-9M Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 3,678 | 14,897 | 44,319 | 7,526 |
| StrikePrecisionLight | 2 × AIM-9M Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,707 | 14,897 | 42,348 | 9,497 |
| StrikePrecisionMedium | 2 × AIM-9M Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,361 | 14,897 | 43,002 | 8,843 |
| StrikePrecisionLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,110 | 18,437 | 46,291 | 5,554 |
| MaverickStrike | 2 × AIM-9M Sidewinder; 4 × AGM-65D Maverick | Empty | 2 × AGM-65D Maverick | 1,480 | 14,897 | 42,121 | 9,724 |
| SEAD | 2 × AIM-9M Sidewinder; 4 × AGM-88A HARM | Empty | Empty | 1,616 | 14,897 | 42,257 | 9,588 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 45,173 | 6,672 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 45,173 | 6,672 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88A HARM; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 1,414 | 14,897 | 42,055 | 9,790 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,493 | 3,352 |
| EOGlideStrike | 2 × AIM-9M Sidewinder; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,692 | 14,897 | 43,333 | 8,512 |
| StrikePavewayIII | 2 × AIM-9M Sidewinder; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 4,128 | 14,897 | 44,769 | 7,076 |
| AntiShipBay | 2 × AIM-9M Sidewinder | Empty | 3 × AGM-84C Harpoon | 1,750 | 14,897 | 42,391 | 9,454 |
| StrikeBay | 2 × AIM-9M Sidewinder | Empty | 3 × Mk 82 500-lb GP bomb | 853 | 14,897 | 41,494 | 10,351 |
| StrikeHeavyBay | 2 × AIM-9M Sidewinder | Empty | 2 × Mk 84 2000-lb GP bomb | 1,986 | 14,897 | 42,627 | 9,218 |
| StrikePrecisionBay | 2 × AIM-9M Sidewinder; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 876 | 14,897 | 41,517 | 10,328 |
| FleetInterceptBay | 2 × AIM-9M Sidewinder; 2 × AIM-7M Sparrow | Empty | 2 × AIM-54C Phoenix | 1,560 | 14,897 | 42,201 | 9,644 |
| AntiShipBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × AGM-84C Harpoon | 2,050 | 18,437 | 46,231 | 5,614 |
| StrikeBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × Mk 82 500-lb GP bomb | 1,153 | 18,437 | 45,334 | 6,511 |
| StrikeHeavyBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 2 × Mk 84 2000-lb GP bomb | 2,286 | 18,437 | 46,467 | 5,378 |
| StrikePrecisionBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,176 | 18,437 | 45,357 | 6,488 |
| FleetInterceptBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-7M Sparrow | Empty | 2 × AIM-54C Phoenix | 1,860 | 18,437 | 46,041 | 5,804 |

### FB-111N MudPig — 1995

ID: `ran_fb-111n_1995`. Role: Bomber. Empty: 26,460 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × AGM-84D Harpoon Block 1C | Empty | Empty | 1,224 | 14,897 | 43,125 | 8,720 |
| AirToAir | 4 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | Empty | 648 | 14,897 | 42,549 | 9,296 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,398 | 18,437 | 46,839 | 5,006 |
| FleetIntercept | 2 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM; 2 × AIM-54C Phoenix | Empty | Empty | 1,402 | 14,897 | 43,303 | 8,542 |
| AntiShip | 2 × AIM-9M Sidewinder; 2 × AGM-84D Harpoon Block 1C | Empty | Empty | 1,224 | 14,897 | 43,125 | 8,720 |
| AntiShipHeavy | 4 × AGM-84D Harpoon Block 1C | Empty | 3 × AGM-84D Harpoon Block 1C | 3,682 | 14,897 | 45,583 | 6,262 |
| AntiShipLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AGM-84D Harpoon Block 1C | Empty | 3 × AGM-84D Harpoon Block 1C | 3,102 | 18,437 | 48,543 | 3,302 |
| Strike | 2 × AIM-9M Sidewinder; 24 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 6,701 | 14,897 | 48,602 | 3,243 |
| StrikeLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 4,077 | 18,437 | 49,518 | 2,327 |
| StrikeHeavy | 2 × AIM-9M Sidewinder; 4 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 5,614 | 14,897 | 47,515 | 4,330 |
| StrikeHeavyLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 4,100 | 18,437 | 49,541 | 2,304 |
| StrikeMedium | 2 × AIM-9M Sidewinder; 4 × Mk 83 1000-lb GP bomb | Empty | 2 × Mk 83 1000-lb GP bomb | 2,896 | 14,897 | 44,797 | 7,048 |
| StrikePrecision | 2 × AIM-9M Sidewinder; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 3,678 | 14,897 | 45,579 | 6,266 |
| StrikePrecisionLight | 2 × AIM-9M Sidewinder; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,707 | 14,897 | 43,608 | 8,237 |
| StrikePrecisionMedium | 2 × AIM-9M Sidewinder; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,361 | 14,897 | 44,262 | 7,583 |
| StrikePrecisionLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,110 | 18,437 | 47,551 | 4,294 |
| MaverickStrike | 2 × AIM-9M Sidewinder; 4 × AGM-65G Maverick | Empty | 2 × AGM-65G Maverick | 1,984 | 14,897 | 43,885 | 7,960 |
| SEAD | 2 × AIM-9M Sidewinder; 4 × AGM-88C HARM | Empty | Empty | 1,616 | 14,897 | 43,517 | 8,328 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 46,433 | 5,412 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 46,433 | 5,412 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 1,414 | 14,897 | 43,315 | 8,530 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 49,753 | 2,092 |
| EOGlideStrike | 2 × AIM-9M Sidewinder; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,692 | 14,897 | 44,593 | 7,252 |
| StrikePavewayIII | 2 × AIM-9M Sidewinder; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 4,128 | 14,897 | 46,029 | 5,816 |
| PopeyeStrike | 2 × AIM-9M Sidewinder; 2 × AGM-142 Popeye / Have Nap; 1 × EO weapon control pod | Empty | Empty | 3,152 | 14,897 | 45,053 | 6,792 |
| SLAMStrike | 2 × AIM-9M Sidewinder; 2 × AGM-84E SLAM; 1 × EO weapon control pod | Empty | 2 × AGM-84E SLAM | 2,944 | 14,897 | 44,845 | 7,000 |
| AntiShipBay | 2 × AIM-9M Sidewinder | Empty | 3 × AGM-84D Harpoon Block 1C | 1,750 | 14,897 | 43,651 | 8,194 |
| StrikeBay | 2 × AIM-9M Sidewinder | Empty | 3 × Mk 82 500-lb GP bomb | 853 | 14,897 | 42,754 | 9,091 |
| StrikeHeavyBay | 2 × AIM-9M Sidewinder | Empty | 2 × Mk 84 2000-lb GP bomb | 1,986 | 14,897 | 43,887 | 7,958 |
| StrikePrecisionBay | 2 × AIM-9M Sidewinder; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 876 | 14,897 | 42,777 | 9,068 |
| FleetInterceptBay | 2 × AIM-9M Sidewinder; 2 × AIM-120B AMRAAM | Empty | 2 × AIM-54C Phoenix | 1,402 | 14,897 | 43,303 | 8,542 |
| AntiShipBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × AGM-84D Harpoon Block 1C | 2,050 | 18,437 | 47,491 | 4,354 |
| StrikeBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 3 × Mk 82 500-lb GP bomb | 1,153 | 18,437 | 46,594 | 5,251 |
| StrikeHeavyBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank | Empty | 2 × Mk 84 2000-lb GP bomb | 2,286 | 18,437 | 47,727 | 4,118 |
| StrikePrecisionBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,176 | 18,437 | 46,617 | 5,228 |
| FleetInterceptBayLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 2 × AIM-120B AMRAAM | Empty | 2 × AIM-54C Phoenix | 1,702 | 18,437 | 47,143 | 4,702 |

### FB-111N MudPig — 2003

ID: `ran_fb-111n_2003`. Role: Bomber. Empty: 26,975 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 2.6; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 2 × AGM-84L Harpoon Block II | Empty | Empty | 1,228 | 14,897 | 43,644 | 8,201 |
| AirToAir | 4 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | Empty | 656 | 14,897 | 43,072 | 8,773 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × AIM-54C Phoenix | Empty | Empty | 1,402 | 18,437 | 47,358 | 4,487 |
| FleetIntercept | 2 × ASRAAM; 2 × AIM-120C-5 AMRAAM; 2 × AIM-54C Phoenix | Empty | Empty | 1,406 | 14,897 | 43,822 | 8,023 |
| AntiShip | 2 × ASRAAM; 2 × AGM-84L Harpoon Block II | Empty | Empty | 1,228 | 14,897 | 43,644 | 8,201 |
| AntiShipHeavy | 4 × AGM-84L Harpoon Block II | Empty | 3 × AGM-84L Harpoon Block II | 3,682 | 14,897 | 46,098 | 5,747 |
| AntiShipLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × AGM-84L Harpoon Block II | Empty | 3 × AGM-84L Harpoon Block II | 3,106 | 18,437 | 49,062 | 2,783 |
| Strike | 2 × ASRAAM; 24 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 6,705 | 14,897 | 49,121 | 2,724 |
| StrikeLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 12 × Mk 82 on six-bomb rack | Empty | 3 × Mk 82 500-lb GP bomb | 4,081 | 18,437 | 50,037 | 1,808 |
| StrikeHeavy | 2 × ASRAAM; 4 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 5,618 | 14,897 | 48,034 | 3,811 |
| StrikeHeavyLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × Mk 84 2000-lb GP bomb | Empty | 2 × Mk 84 2000-lb GP bomb | 4,104 | 18,437 | 50,060 | 1,785 |
| StrikeMedium | 2 × ASRAAM; 4 × Mk 83 1000-lb GP bomb | Empty | 2 × Mk 83 1000-lb GP bomb | 2,900 | 14,897 | 45,316 | 6,529 |
| StrikePrecision | 2 × ASRAAM; 3 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 3,682 | 14,897 | 46,098 | 5,747 |
| StrikePrecisionLight | 2 × ASRAAM; 3 × GBU-12 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,711 | 14,897 | 44,127 | 7,718 |
| StrikePrecisionMedium | 2 × ASRAAM; 3 × GBU-16 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,365 | 14,897 | 44,781 | 7,064 |
| StrikePrecisionLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × GBU-10 Paveway II; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 2,114 | 18,437 | 48,070 | 3,775 |
| MaverickStrike | 2 × ASRAAM; 4 × AGM-65G Maverick | Empty | 2 × AGM-65G Maverick | 1,988 | 14,897 | 44,404 | 7,441 |
| SEAD | 2 × ASRAAM; 4 × AGM-88C HARM | Empty | Empty | 1,620 | 14,897 | 44,036 | 7,809 |
| EW | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 46,952 | 4,893 |
| EWLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 46,952 | 4,893 |
| EscortSEAD | 2 × ASRAAM; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 1,418 | 14,897 | 43,834 | 8,011 |
| ReconLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,272 | 1,573 |
| EOGlideStrike | 2 × ASRAAM; 2 × GBU-15 electro-optical glide bomb; 1 × EO weapon control pod | Empty | Empty | 2,696 | 14,897 | 45,112 | 6,733 |
| StrikePavewayIII | 2 × ASRAAM; 3 × GBU-24 Paveway III; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 4,132 | 14,897 | 46,548 | 5,297 |
| PopeyeStrike | 2 × ASRAAM; 2 × AGM-142 Popeye / Have Nap; 1 × EO weapon control pod | Empty | Empty | 3,156 | 14,897 | 45,572 | 6,273 |
| SLAMStrike | 2 × ASRAAM; 2 × AGM-84E SLAM; 1 × EO weapon control pod | Empty | 2 × AGM-84E SLAM | 2,948 | 14,897 | 45,364 | 6,481 |
| SLAMERStrike | 2 × ASRAAM; 2 × AGM-84K SLAM-ER; 1 × EO weapon control pod | Empty | Empty | 1,786 | 14,897 | 44,202 | 7,643 |
| JDAMHeavy | 2 × ASRAAM; 4 × GBU-31 JDAM Mk 84 | Empty | 2 × GBU-31 JDAM Mk 84 | 5,726 | 14,897 | 48,142 | 3,703 |
| JDAMMedium | 2 × ASRAAM; 4 × GBU-32 JDAM Mk 83 | Empty | 2 × GBU-32 JDAM Mk 83 | 2,942 | 14,897 | 45,358 | 6,487 |
| JSOWStrike | 2 × ASRAAM; 4 × AGM-154A JSOW | Empty | Empty | 2,108 | 14,897 | 44,524 | 7,321 |
| AntiShipBay | 2 × ASRAAM | Empty | 3 × AGM-84L Harpoon Block II | 1,754 | 14,897 | 44,170 | 7,675 |
| StrikeBay | 2 × ASRAAM | Empty | 3 × Mk 82 500-lb GP bomb | 857 | 14,897 | 43,273 | 8,572 |
| StrikeHeavyBay | 2 × ASRAAM | Empty | 2 × Mk 84 2000-lb GP bomb | 1,990 | 14,897 | 44,406 | 7,439 |
| StrikePrecisionBay | 2 × ASRAAM; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 880 | 14,897 | 43,296 | 8,549 |
| FleetInterceptBay | 2 × ASRAAM; 2 × AIM-120C-5 AMRAAM | Empty | 2 × AIM-54C Phoenix | 1,406 | 14,897 | 43,822 | 8,023 |
| JDAMBay | 2 × ASRAAM | Empty | 2 × GBU-32 JDAM Mk 83 | 1,098 | 14,897 | 43,514 | 8,331 |
| JDAMHeavyBay | 2 × ASRAAM | Empty | 2 × GBU-31 JDAM Mk 84 | 2,026 | 14,897 | 44,442 | 7,403 |
| AntiShipBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | Empty | 3 × AGM-84L Harpoon Block II | 2,054 | 18,437 | 48,010 | 3,835 |
| StrikeBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | Empty | 3 × Mk 82 500-lb GP bomb | 1,157 | 18,437 | 47,113 | 4,732 |
| StrikeHeavyBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | Empty | 2 × Mk 84 2000-lb GP bomb | 2,290 | 18,437 | 48,246 | 3,599 |
| StrikePrecisionBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × External laser designation pod | Empty | 2 × GBU-12 Paveway II | 1,180 | 18,437 | 47,136 | 4,709 |
| FleetInterceptBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 2 × AIM-120C-5 AMRAAM | Empty | 2 × AIM-54C Phoenix | 1,706 | 18,437 | 47,662 | 4,183 |
| JDAMBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | Empty | 2 × GBU-32 JDAM Mk 83 | 1,398 | 18,437 | 47,354 | 4,491 |
| JDAMHeavyBayLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank | Empty | 2 × GBU-31 JDAM Mk 84 | 2,326 | 18,437 | 48,282 | 3,563 |

### RF-111N SprintPig — 1980

ID: `ran_rf-111n`. Role: Recon,ESM. Empty: 25,350 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| AirToAir | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| Recon | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| ReconLongRange | 2 × AIM-9L Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,643 | 3,202 |
| ReconFast | 2 × AIM-9L Sidewinder | Empty | Empty | 172 | 14,897 | 40,963 | 10,882 |

### RF-111N SprintPig — 1985

ID: `ran_rf-111n_1985`. Role: Recon,ESM. Empty: 25,650 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| AirToAir | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| Recon | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 48,943 | 2,902 |
| ReconFast | 2 × AIM-9M Sidewinder | Empty | Empty | 172 | 14,897 | 41,263 | 10,582 |

### RF-111N SprintPig — 1995

ID: `ran_rf-111n_1995`. Role: Recon,ESM. Empty: 27,000 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| AirToAir | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| Recon | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| ReconLongRange | 2 × AIM-9M Sidewinder; 4 × 600 US-gallon fuel tank | Empty | Empty | 772 | 21,977 | 50,293 | 1,552 |
| ReconFast | 2 × AIM-9M Sidewinder | Empty | Empty | 172 | 14,897 | 42,613 | 9,232 |

### RF-111N SprintPig — 2003

ID: `ran_rf-111n_2003`. Role: Recon,ESM. Empty: 27,600 kg. Internal fuel: 14,897 kg. Gun ammunition: 544 kg / 2,000 rounds. Max Mach: 3.0; cruise Mach: 2.52.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| AirToAir | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| AirToAirLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| Recon | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| ReconLongRange | 2 × ASRAAM; 4 × 600 US-gallon fuel tank | Empty | Empty | 776 | 21,977 | 50,897 | 948 |
| ReconFast | 2 × ASRAAM | Empty | Empty | 176 | 14,897 | 43,217 | 8,628 |

### EF-111N ScreamPig — 1980

ID: `ran_ef-111n`. Role: EW,ESM. Empty: 28,250 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.84.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| AirToAir | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| AirToAirLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EW | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EWLongRange | 2 × AIM-9L Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 992 | 18,437 | 47,679 | 4,166 |
| EscortSEAD | 2 × AIM-9L Sidewinder; 2 × AGM-78 Standard ARM; 1 × Naval offensive ECM pod 1 (1980); 1 × Naval offensive ECM pod 2 (1980) | Empty | Empty | 1,932 | 14,897 | 45,079 | 6,766 |

### EF-111N ScreamPig — 1985

ID: `ran_ef-111n_1985`. Role: EW,ESM. Empty: 28,500 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.88.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| AirToAir | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 992 | 18,437 | 47,929 | 3,916 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88A HARM; 1 × Naval offensive ECM pod 1 (1985); 1 × Naval offensive ECM pod 2 (1985) | Empty | Empty | 1,414 | 14,897 | 44,811 | 7,034 |

### EF-111N ScreamPig — 1995

ID: `ran_ef-111n_1995`. Role: EW,ESM. Empty: 29,750 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.92.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| AirToAir | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| AirToAirLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EW | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EWLongRange | 2 × AIM-9M Sidewinder; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 992 | 18,437 | 49,179 | 2,666 |
| EscortSEAD | 2 × AIM-9M Sidewinder; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (1995); 1 × Naval offensive ECM pod 2 (1995) | Empty | Empty | 1,414 | 14,897 | 46,061 | 5,784 |

### EF-111N ScreamPig — 2003

ID: `ran_ef-111n_2003`. Role: EW,ESM. Empty: 30,250 kg. Internal fuel: 14,897 kg. Gun ammunition: none. Max Mach: 2.2; cruise Mach: 0.96.

| Preset | Wing stores | Auxiliary external | Internal bay | Dry stores kg | Total fuel kg | Takeoff kg | Margin kg |
|---|---|---|---|---|---|---|---|
| Default | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| AirToAir | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| AirToAirLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EW | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EWLongRange | 2 × ASRAAM; 2 × 600 US-gallon fuel tank; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 996 | 18,437 | 49,683 | 2,162 |
| EscortSEAD | 2 × ASRAAM; 2 × AGM-88C HARM; 1 × Naval offensive ECM pod 1 (2003); 1 × Naval offensive ECM pod 2 (2003) | Empty | Empty | 1,418 | 14,897 | 46,565 | 5,280 |

### Every local store definition

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
| ran_nw_mk82 | Mk 82 500-lb GP bomb | 227 | 0 | 1980 | Yes | Native guidance; rounded historical carried mass |
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

### Preserved design and simulation limits

MudPig AntiShip is two wing Harpoons/two IR missiles with empty bay; AntiShipHeavy is four wing and three bay Harpoons; AntiShipLongRange is two wing and three bay Harpoons, two IR missiles and two tanks. Bay stations, concealment and doors are exact original definitions. Extra strike/interceptor fits use those stations with strike/Phoenix targeting. [Bay loadouts and armed recovery test](INTERNAL_BAY_V8.md). The separately relocated M61 is fictional; no new gun fairing is drawn.

EF retains two physical pylon ECM pods and two offensive sensors. FB only carries removable offensive containers in its EW presets. Designation and EO control pods occupy counted external stations. Existing cockpit, model and landing animation geometry remains.

Native modern-weapon approximations: AMRAAM lacks platform midcourse correction; ASRAAM lacks helmet sight/LOAL; EO weapons lack manual man-in-the-loop retargeting; Block II Harpoon models radar-homing ship attack; JDAM/JSOW use CEP/ballistic/glide settings instead of full GPS/INS. Period choices assume funded Australian integration, including accelerated early procurement.

Static checks do not prove gun fire, release trajectories, AI Mach 3 behaviour, ECM display, date filtering or carrier landings. These still need Sea Power runtime testing. [References](../HISTORICAL_REFERENCES.md) · [Aircraft comparison](AIRCRAFT_COMPARISON.md) · [Investment](INVESTMENT_PROGRAMME.md)
