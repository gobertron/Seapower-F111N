# Historical references

V6 references checked 30 September 2026; V8 engine references checked 1 October 2026. All N-family procurement, integration and naval engineering are alternate-history assumptions. The historical reference baseline and estimated additions are separated in `loadout_manifest.json`.

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

## V8 propulsion references and estimates

[GE historical military engine status report](https://www.geaerospace.com/news/press-releases/defense-engines/ge-aircraft-engines-military-engine-status-report) gives the F110-GE-400 120 kN afterburning class in operational service from April 1988 and the F110-GE-129 129 kN class from April 1992. These support the chosen 1995/2003 supplier classes; they do not establish an actual F-111 retrofit. [GE F110 datasheet](https://www.geaerospace.com/sites/default/files/2022-02/F110-Datasheet.pdf) is additional family context; later engine upgrades are not silently assigned to early editions.

V8 adds systems/control allowances 0/150/650/850 kg; propulsion-retrofit allowances 0/0/600/750 kg; RF thermal allowances 0/50/150/250 kg, alongside the existing edition-avionics allowance. These are explicit engineering estimates. Installed dry thrust, TF30 uprating, F-111 naval adaptation, control/sensor/readiness ratings, nominal range growth and RF Mach 3 propulsion are fictional. The TPS-inspired RGB palette is an uncalibrated screen approximation, not a certified paint standard or historical USN F-111 scheme.
