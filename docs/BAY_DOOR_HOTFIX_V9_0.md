# V9.0 bay-door hotfix

The shared F-111F model includes `bay_l` and `bay_r` door meshes. Their original free-form entries in `[Submodels]` differed from the numbered `General_N` registrations used by other aircraft. This candidate fix registers the two doors and the parent of the Pave Tack mesh as `General_12` through `General_14` on all twelve F-111N, FB-111N and RF-111N aircraft. The EF-111N uses a different model and is unchanged.

The MudPig already has a three-station bay with hidden internal stores, plus door-open and door-close animation references. This fix preserves those definitions and their existing loadouts. The other two families do not have a playable internal weapons bay.

For an existing V9.0 installation, close Sea Power and run:

```bash
python3 fix-f111n-v9-bay-doors.py "/path/to/Sea Power"
```

The offline script checks the installed mod identity and all twelve aircraft, saves a complete backup, and refuses unexpected or conflicting registrations. Repeating it is safe. The old V9.0 replacement installer remains pinned to the pre-hotfix release; reapply the hotfix after using it.

## In-game verification required

This is an evidence-backed candidate, not a confirmed runtime fix. Test all four eras: view WaterPig, MudPig and SprintPig from below in ordinary flight; check for closed panels and clipping. On MudPig, try an internal `StrikeBay` or `AntiShipBay` preset and observe the doors opening for release, the store leaving, and the doors closing afterwards. Repeat with an empty-bay preset and a carrier takeoff/recovery. Check the separate ScreamPig model visually as well. Record the aircraft, preset, camera view, and any clipping or failure. These checks were not performed in this environment.
