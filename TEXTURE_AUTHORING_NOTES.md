# V8 native texture authoring

Eight 3072 × 2048 RGBA maps cover F/FB/RF/EF in 1995 and 2003. Squadron entries, external fuel tanks and selection profiles point to their matching edition maps.

The authored material uses USN-inspired darker upper surfaces, intermediate sides and light undersides, approximating FS35237/36320/36375. RGB is an uncalibrated screen approximation. Australian roundels, NAVY lettering, A8 serials, role-specific flying-pig badges and fin checks remain subdued. The 2003 material adds modest wear and touch-up variation.

`authoring/usn_liveries.py` defines the editable material and projects it through the actual OBJ surfaces into the existing UV atlas. Vector roundels, badges and text are projected in world coordinates. No UV island moves or resampling changes atlas dimensions. `paint_textures.py` supplies the original geometry mapper and vector badge/text authoring.

Each map preserves source alpha exactly and protects cockpit/mechanical atlas regions. Exhaust and warning details are preserved. The existing calibrated Unity side convention keeps serial/NAVY text readable on both sides. Original meshes, normal/specular maps, landing/bay animations and earlier maps remain unchanged.

`USN_TEXTURE_VALIDATION.json` records all eight sources, dimensions, changed pixels, alpha/protected-region checks and SHA-256 hashes. The comparison and both-side lettering images render actual shipped assets with a CPU rasterizer. They are visual checks, not Sea Power screenshots. Stock weapon meshes unavailable outside the game are omitted from the previews.
