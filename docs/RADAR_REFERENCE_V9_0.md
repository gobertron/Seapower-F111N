# V9.0 radar coverage and Unit Reference

29 October 2026. Applies to all sixteen aircraft in the 1980, 1985, 1995 and 2003 editions.

## Forward coverage

Azimuth angles are measured left/right from the aircraft nose. The total sector spans both sides, rather than describing each side separately.

| Edition | WaterPig search and all Phoenix controllers | Total sector | MudPig, SprintPig and ScreamPig search | Total sector |
|---|---|---:|---|---:|
| 1980 | -65 to +65 degrees | 130 degrees | -45 to +45 degrees | 90 degrees |
| 1985 | -70 to +70 degrees | 140 degrees | -55 to +55 degrees | 110 degrees |
| 1995 | -80 to +80 degrees | 160 degrees | -65 to +65 degrees | 130 degrees |
| 2003 | -85 to +85 degrees | 170 degrees | -75 to +75 degrees | 150 degrees |

These fictional programme upgrades represent funded changes to antenna steering, processing and track handling. They are not claims about historical F-111 or AWG-9 scan limits. All systems remain forward-looking. Fleet and Phoenix vertical limits stay -60 to +60 degrees, and strike vertical limits stay -70 to +60 degrees.

WaterPig searches for air targets. The other families use the existing air/surface radar with land-target detection. The 1980/1985 radars retain local-only data, and the 1995/2003 sets share radar data. The 15-metre Fleet/Phoenix minimum target altitude and existing strike-radar zero-metre limit remain as before. Search and fire-control range, horizon, target cross-section, weather, jamming and game-version behaviour still limit actual detection.

Phoenix controllers widen with the same-year fleet radar. This includes MudPig's wing and internal-bay guidance links. A wider control sector does not give MudPig a wider search sector than the strike-radar values above. Hardpoint firing arcs still require the aircraft to align for launch.

## Expanded reference cards

Each aircraft has its own role and edition story, written for the Unit Reference description. The cards explain the alternate Australian carrier programme, why each specialist was developed, its equipment generation, radar coverage, weapons or mission stores and operating considerations. Displayed capability figures are drawn from the shipped configuration.

The supplied screenshot ended at the first semicolon in the old MudPig description. This strongly suggests inline-comment parsing, rather than proving a fixed UI text limit. New descriptions contain no semicolons, comment markers, rich-text tags or unverified newline escapes. Each stays on one physical INI line for the native UI to wrap. Squadron selections inherit the aircraft description.

## In-game check

1. Install the updated V9.0, enable it with priority over older copies and restart Sea Power.
2. Open Unit Reference and select each dated family. Check that the development story and capability text continue beyond the old truncation point. Scroll the description area if needed.
3. In a simple daylight mission without jamming, point the aircraft north and enable its search radar. Place comparable air targets at the same altitude and range, inside and outside the listed sector. Use ships separately for the three air/surface radar families.
4. Compare matching aircraft at 1980 and later dates. For example, a target 60 degrees off the nose is outside the 1980 strike sector and inside the 1995/2003 strike sectors. A target 75 degrees off the nose is outside the 1980 fleet sector and inside the 1995/2003 fleet sectors. Use positions comfortably away from the exact boundary.
5. Check Sparrow/Phoenix targeting with suitable loadouts, allowing the aircraft to turn into its unchanged hardpoint firing arc before launch. Check MudPig's external and bay Phoenix fits separately.

Static validation checks actual radar values and references, the preserved vertical limits, the manifests, all sixteen descriptions and the unchanged loadout/model contracts. Sea Power is unavailable in the authoring environment, so live radar tracking and long-description layout remain runtime checks.
