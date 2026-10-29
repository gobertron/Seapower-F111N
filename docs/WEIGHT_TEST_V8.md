> This separately versioned V8 diagnostic is compatible with Naval Wing 9.0. Its plugin identity and recording paths remain unchanged.

# Version 8 aircraft weight test

Version 8 already gives aircraft an empty mass and gives missiles, bombs, pods and tank shells separate native `Mass` values. Tank fuel is separate. This diagnostic records what the running game actually exposes, so configuration checks are not mistaken for a successful flight test.

**Status: prepared and tested with simulated state; not yet run in Sea Power.** This workspace has no game installation. The optional monitor is original code and uses the BepInEx preloader already installed with Anchor Chain. It does not patch physics or change weapon, fuel, thrust or aircraft settings.

## Install on Aram's CachyOS system

Close Sea Power, then run these commands from fish or bash:

```bash
curl -fL 'https://raw.githubusercontent.com/gobertron/Seapower-F111N/main/check-f111n-weight-v8.sh' -o ~/Downloads/check-f111n-weight-v8.sh
bash ~/Downloads/check-f111n-weight-v8.sh "/home/aram/.local/share/Steam/steamapps/common/Sea Power"
```

The script verifies its embedded plugin and installs only `BepInEx/plugins/RANF111NWeightMonitorV8`. The normal Naval Wing installer and Workshop payload are unchanged. This optional diagnostic is not part of the Workshop mod and does not need uploading to Steam.

## In-game test

1. Start a mission with **FB-111N MudPig 2003**, preset **AntiShipHeavy**. The fit has four wing and three bay Harpoons, each configured at 526 kg.
2. Use one aircraft with independent orders, a steady altitude and speed, and a surface target within Harpoon launch limits. Let it fly for about 30 seconds.
3. Fire at least one Harpoon, preferably wing and bay weapons over successive launches. Continue flying for at least one minute to record fuel burn. Avoid refuelling or changing loadout during this test.
4. Close Sea Power and collect the results:

```bash
bash ~/Downloads/check-f111n-weight-v8.sh --collect "/home/aram/.local/share/Steam/steamapps/common/Sea Power"
```

The script creates `RAN-F111N-weight-V8/weight-results-v8.zip` under the game folder. It includes the most recent nonempty CSV and its readable/JSON reports. Attach that ZIP for review. No game assemblies or unrelated logs are collected or uploaded.

## What is checked

The monitor reads live aircraft/controller mass and fuel fields, ammunition totals and live ammunition parameter masses when available. It also records field/type names when first seeing an aircraft/controller combination, to help diagnose an unsupported game layout. It samples once per real second, only matches the sixteen Naval Wing IDs, skips pooled objects with no live unit ID and limits recording to 64 aircraft and 40 MiB per game session.

The report compares two observations of the same aircraft:

`gross mass lost = released ammunition mass + fuel mass consumed`

For example, losing one 526-kg Harpoon while burning 10 kg of fuel should reduce reported gross mass by 536 kg. The report separately checks fuel-only intervals. It prefers live store parameters over the release catalogue, so an enabled mod's changed weapon weight can be detected.

Only matching **observed** gross/fuel mass fields count as consistent evidence. A constant mass, missing field, unknown ammunition mass, loadout swap or refuelling cannot produce a successful release result. If this game build uses another field layout, the result remains **NOT VERIFIED** and the raw values are retained for diagnosis. A matching field is evidence of a state update; it does not establish how every controller uses that field or certify acceleration, climb, drag, maximum speed, carrier launch or recovery.

Configuration budgets and measured state must remain separate. Do not add a preset's weapons to `EmptyMass`: doing that can double-count the payload and retain its weight after release. The native Mk 82 MER definition includes an estimated share of rack mass in each bomb's mass; this approximation also needs attention when interpreting rack-release results.

If no aircraft samples appear, check `BepInEx/LogOutput.log` for `RAN F-111N Weight Monitor Version 8` or `Version 8 read-only weight recording`. Merely finding the preloader files does not prove Proton loaded them. Keep the working Anchor Chain launch settings from your existing setup.

## Remove the monitor

Close the game and run:

```bash
bash ~/Downloads/check-f111n-weight-v8.sh --remove "/home/aram/.local/share/Steam/steamapps/common/Sea Power"
```

Recordings are kept. The aircraft mod and other plugins are preserved.

## Build and verification

Source is in `diagnostics/weight-v8`. With a .NET SDK and the game's existing dependencies:

```bash
dotnet build diagnostics/weight-v8/WeightMonitorV8.csproj -c Release -p:GameDir="/full/path/to/Sea Power"
python3 authoring/build_weight_monitor.py --dll diagnostics/weight-v8/bin/Release/netstandard2.1/RANF111NWeightMonitorV8.dll
python3 -m unittest authoring.test_weight_monitor -v
```

The shipped standalone wrapper contains only the compiled original monitor and catalogue. Unity, BepInEx, game DLLs and compiler dependencies are not bundled. `diagnostics/weight-v8/BUILD_V8.json` records source and payload hashes. `ProbeTests.cs` exercises state capture using fake objects; it is excluded from the plugin build.

API usage was checked against the primary [Anchor Chain loader and examples](https://github.com/SeaPower-Modders/AnchorChain/tree/28d225be917533fcc25e19cf8f25ac44010f8abd) and the primary [multiplayer mod's ammunition capture implementation](https://github.com/malfboi/SeaPowerMultiplayerMod/blob/8c429c540f2c873e5a2f40cb49528be8975a190f/src/Gameplay/CapturePatches.cs). Game types are discovered at runtime to avoid binding the monitor to a different `Seapower-Scripts.dll` build. Unsupported layouts fail as unverified rather than changing the game.
