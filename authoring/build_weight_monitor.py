#!/usr/bin/env python3
"""Build the optional Version 8 read-only monitor; game assemblies are not shipped.

Pass --dll after compiling Plugin.cs and WeightProbe.cs against BepInEx.dll,
UnityEngine.dll and UnityEngine.CoreModule.dll from the existing game/preloader.
The result is a self-contained bash/Python installer with a verified payload.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dll", type=Path, required=True)
    args = parser.parse_args()
    payload = args.dll.read_bytes()
    if not payload.startswith(b"MZ"):
        raise ValueError("Expected a compiled managed plugin DLL")
    source = ROOT / "diagnostics/weight-v8"
    code = (source / "weight_check.py").read_text()
    checksum = hashlib.sha256(payload).hexdigest()
    code = code.replace('PLUGIN_BASE64 = ""', "PLUGIN_BASE64 = " + repr(base64.b64encode(payload).decode("ascii")))
    code = code.replace('PLUGIN_SHA256 = ""', "PLUGIN_SHA256 = " + repr(checksum))
    catalog = json.loads((ROOT / "weapon_catalog.json").read_text())
    code = code.replace("CATALOG = {}", "CATALOG = " + repr(catalog), 1)
    wrapper = '#!/usr/bin/env bash\nset -euo pipefail\nexec python3 - "$@" <<\'V8_WEIGHT_PY\'\n' + code + '\nV8_WEIGHT_PY\n'
    script = ROOT / "check-f111n-weight-v8.sh"
    script.write_text(wrapper)
    script.chmod(0o755)
    provenance = {"version": "Version 8", "plugin_sha256": checksum, "plugin_bytes": len(payload),
                  "source_sha256": {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in ("Plugin.cs", "WeightProbe.cs", "weight_check.py")},
                  "runtime_tested_in_seapower": False, "external_dependencies_shipped": False,
                  "build": "Mono C# compiler 6.8.0.105; NETStandard.Library.Ref 2.1.0 reference assemblies; BepInEx/Unity assemblies supplied by AnchorChain 28d225be917533fcc25e19cf8f25ac44010f8abd"}
    (source / "BUILD_V8.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"script": str(script), "plugin_sha256": checksum, "plugin_bytes": len(payload)}))


if __name__ == "__main__":
    main()
