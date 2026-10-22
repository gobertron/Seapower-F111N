#!/usr/bin/env bash
set -euo pipefail
exec python3 - "$@" <<'V8_WEIGHT_PY'
#!/usr/bin/env python3
"""Version 8: install/remove a read-only monitor and interpret its observations.

The generated standalone shell wrapper embeds the compiled original plugin and
the release's store catalogue. No game, Unity or BepInEx assembly is distributed.
"""
import argparse
import base64
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

PLUGIN_BASE64 = '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BgDoAZwABgDtAZwABgD/AZwABgAhApwABgAyApwABgBCApwABgCTApwABgAqA8cABgBBA1oATwCOAwAAVwCcAwAABgDTA8cABgDaA+YDBgACBJwABgAWBOYDXwCcAwAABgA/BJwABgBRBGwECgCfBKsECgCzBKsEBgDKBIAABgDXBIAABgDxBIAABgD/BJwABgATBYAABgAeBYAABgAnBYAABgAyBYAABgA8BYAABgBDBYAACgBeBasECgB5BYkFBgChBZwADgDABcUFBgDqBVoABgDzBZwADgAyAcUFDgAdBsUFDgA8BsUFDgBVBsUFBgCEBpwABgCKBpwABgCQBpwABgBIB2wEAAAAAAEAAAAAAAEAAQABARAAHAAKABkAAQABAIEBEAAkAAoAGQAEAAIAAQEQADAACgCpAAYADAAGADcAAQAGADwAAQAGAEEABABRgEcABwARADAEZwEBAGwACwABAIoADwABAKMAEwABAK4AFgAhALUAGQABAOIAIABRgOoAFgAxAPcAIwBQIAAAAACGGDkBfgIBAHAgAAAAAJYAvgaFAgQALCEAAAAAlgDCBpUCBgAgIgAAAACWAMkGoAIIAJQiAAAAAJYA1AZSAQkARCMAAAAAkQDgBlIBCgCoIwAAAACRAOcGUgELADwkAAAAAJEA7ga3AgwAsCQAAAAAkQD5Br0CDQAQJwAAAACWAP4G8wITAFApAAAAAJEAAwcnAxUAeSkAAAAAhhg5AScAFwCMKQAAAACBAA4HJwAXAGAqAAAAAJEAFAc6AxcAhCoAAAAAgQAYBycAGABkLgAAAACBAB8HJwAYAIMuAAAAAJEYKQdpAxgAAAABACIBAAACACcBAAADACwBAAABAD8BAAACACcBAAABACwBAgACANkBAAABAFoCAAABAK8CAAABACcBAAABACcBAAABAN8CAAABAAIDAAACAAgDAAADAA0DAAAEABMDAAAFABoDEBAGAB8DAAABAFoCEBACAB8DAAABAIwEAAACAI4EAAABACwBMQA5AScAMQBIATAAGQBaATUAOQBjAT0AOQBxAUUAGQCHAUoAQQBjAVIAQQCTAVoAQQC0AWAAUQBjAWYAQQBxAW4AGQDMATAAGQBjAXUAGQD0AX0AKQAMAoEAeQApAoYAiQBJAo0AiQBPAo0AeQBjApIAaQBsApkAaQB0Ap8AaQCAAqQAaQCKAqkAaQCkArAAaQCAArQAaQCyAroAaQC5AsEAaQCyAscAaQDFAs0AaQDWAtEAGQDkAs0AaQDxAgEAaQD3AqkADAAmA94AFAA5AScAGQA3A+wAoQBMA80AFABVA94AOQBhAzAAFAAmA/QAGQBvA/wAQQB9AzAAFACnAwQBHACwAxcBJAC+AyoBFADKAy8BaQCyAjYBLAAmA0MBJAD5A30AyQAOBCcALAA5AScADAA5AScAwQCwA0kB0QC+A04BaQAiBFIB0QD5A30ALACwA1cBNAC+AyoBNAD5A30APAA5AXYBLABMBHwB6QA5AScAaQCQBIsB8QA5AZEB+QC5BO4BAQHPBMcACQHhBPIBGQEIBfkBGQFjAv8BIQE5AQYCEQA5ARQCSQFOBRsCSQFYBScAUQFuBSACWQGZBSYCYQGrBc0AWQG3BSYCaQBsAisCaQHRBTECGQC5AnUAeQH9BTUCeQEPBjsCcQFIAUICiQEnBkkCgQG5AlICkQFGBlwCmQFgBn0AgQF2BrAAoQFjAmICiQBjAmICRAAmA94AqQFjAmICsQFjAv8BiQBjAv8BEQCXBm4CQQGmBnQCWQGzBiYCSQEOBCcAaQCyAngCRAA5AScAUQE5AScAuQE5AScACAAQACsACgAwAOUBAgBJANYAAgBRANYALgAzA20DgwADApgBoQDzAYYBYAHzAYYBiwKcAqUCqwKzAtAC/gIvAz8D2ADkAA8BIgE8AWABbwFoAgSAAAAAAAAAAAAAAAAAAAAAADAHAAACAAEAAAAAAAAAAACMA2YHAAAAAAUABAAXAAIAAAAAAAAAqwQAAAAAAAAAAAAAAAAAAAAAAAByBwAAAAAAAAA8TW9kdWxlPgBSQU5GMTExTi5XZWlnaHRWOABSZWFkaW5nAFdlaWdodFByb2JlAFBsdWdpbgBLaW5kAE5hbWUAVmFsdWUARmxhZ3MAQmluZGluZ0ZsYWdzAFN5c3RlbS5SZWZsZWN0aW9uAHdyaXRlcgBTdHJlYW1Xcml0ZXIAU3lzdGVtLklPAGFpcmNyYWZ0VHlwZQBUeXBlAFN5c3RlbQBuZXh0U2FtcGxlAHNhbXBsZQBzY2hlbWFzAEhhc2hTZXRgMQBTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYwBzdG9wcGVkAE1heGltdW1CeXRlcwBJbnZhcmlhbnQAQ3VsdHVyZUluZm8AU3lzdGVtLkdsb2JhbGl6YXRpb24Aa2luZABuYW1lAHZhbHVlAE9iamVjdAAuY3RvcgBpbnN0YW5jZQBHZXRUeXBlAEZpZWxkSW5mbwBHZXRGaWVsZABvcF9JbmVxdWFsaXR5AEdldFZhbHVlAFByb3BlcnR5SW5mbwBHZXRQcm9wZXJ0eQBHZXRJbmRleFBhcmFtZXRlcnMAUGFyYW1ldGVySW5mbwBHZXRHZXRNZXRob2QATWV0aG9kSW5mbwBnZXRfQmFzZVR5cGUAbnVtYmVyAEJvb2xlYW4AQ2hhcgBTdHJpbmcAZ2V0X0lzRW51bQBJQ29udmVydGlibGUAZ2V0X0ludmFyaWFudEN1bHR1cmUAQ29udmVydABUb0RvdWJsZQBJRm9ybWF0UHJvdmlkZXIARG91YmxlAElzTmFOAElzSW5maW5pdHkAYWlyY3JhZnQAVG9TdHJpbmcAUmVwbGFjZQBMYXN0SW5kZXhPZgBTdWJzdHJpbmcARW5kc1dpdGgAU3RyaW5nQ29tcGFyaXNvbgBnZXRfTGVuZ3RoAGlkAENvbmNhdABvcF9FcXVhbGl0eQBUb0xvd2VySW52YXJpYW50AENvbnRhaW5zAHR5cGUAZ2V0X0Z1bGxOYW1lAEVtcHR5AFN0YXJ0c1dpdGgAb3duZXIAcGF0aABkZXB0aABvdXRwdXQAc2VlbgBzY2hlbWEAQWRkAERpY3Rpb25hcnlgMgBHZXRGaWVsZHMATWVtYmVySW5mbwBnZXRfTmFtZQBDb250YWluc0tleQBnZXRfRmllbGRUeXBlAEdldFByb3BlcnRpZXMAZ2V0X1Byb3BlcnR5VHlwZQBLZXlDb2xsZWN0aW9uAEVudW1lcmF0b3IAZ2V0X0tleXMAR2V0RW51bWVyYXRvcgBnZXRfQ3VycmVudABnZXRfSXRlbQBMaXN0YDEASUVudW1lcmFibGUAU3lzdGVtLkNvbGxlY3Rpb25zAE1vdmVOZXh0AElEaXNwb3NhYmxlAERpc3Bvc2UASUVudW1lcmF0b3IASXNOdWxsT3JFbXB0eQA8PmZfX2FtJGNhY2hlMABDb21wYXJpc29uYDEAU29ydABDb21waWxlckdlbmVyYXRlZEF0dHJpYnV0ZQBTeXN0ZW0uUnVudGltZS5Db21waWxlclNlcnZpY2VzAGEAYgBDb21wYXJlT3JkaW5hbABCZXBJblBsdWdpbgBCZXBJbkV4AFBhdGhzAGdldF9HYW1lUm9vdFBhdGgAUGF0aABDb21iaW5lAERpcmVjdG9yeQBDcmVhdGVEaXJlY3RvcnkARGlyZWN0b3J5SW5mbwBEYXRlVGltZQBnZXRfVXRjTm93AEZpbGVTdHJlYW0ARmlsZU1vZGUARmlsZUFjY2VzcwBGaWxlU2hhcmUAU3RyZWFtAFRleHRXcml0ZXIAV3JpdGVMaW5lAEZsdXNoAEJhc2VVbml0eVBsdWdpbgBnZXRfTG9nZ2VyAE1hbnVhbExvZ1NvdXJjZQBCZXBJbkV4LkxvZ2dpbmcATG9nSW5mbwBFeGNlcHRpb24AZ2V0X01lc3NhZ2UATG9nRXJyb3IAVGltZQBVbml0eUVuZ2luZQBnZXRfcmVhbHRpbWVTaW5jZVN0YXJ0dXAAQXNzZW1ibHkAQXBwRG9tYWluAGdldF9DdXJyZW50RG9tYWluAEdldEFzc2VtYmxpZXMAUmVzb3VyY2VzAEZpbmRPYmplY3RzT2ZUeXBlQWxsAENvbXBvbmVudABnZXRfZ2FtZU9iamVjdABHYW1lT2JqZWN0AGdldF9hY3RpdmVJbkhpZXJhcmNoeQBHZXRJbnN0YW5jZUlEAEludDMyAEludDY0AFNpbmdsZQBnZXRfQmFzZVN0cmVhbQBnZXRfUG9zaXRpb24ATG9nV2FybmluZwBHZXQATnVtYmVyAERlZmluaXRpb24ASXNOYXZhbFdpbmcATWV0cmljAEJyYW5jaABCcmFuY2hUeXBlAFNjYW4AUmVhZAA8UmVhZD5tX18wAEF3YWtlAENzdgBVcGRhdGUAT25EZXN0cm95AC5jY3RvcgBSQU5GMTExTldlaWdodE1vbml0b3JWOABSdW50aW1lQ29tcGF0aWJpbGl0eUF0dHJpYnV0ZQBuZXRzdGFuZGFyZABVbml0eUVuZ2luZS5Db3JlTW9kdWxlAFJBTkYxMTFOV2VpZ2h0TW9uaXRvclY4LmRsbAAAAAAAC1YAYQBsAHUAZQAACV8AbwBiAHAAAB1fAG8AYgBqAGUAYwB0AEkAbgBpAE4AYQBtAGUAAAkuAGkAbgBpAAADZgAABWYAYgAABXIAZgAABWUAZgAACXIAYQBuAF8AAAstADEAMQAxAG4AAAtfADEAOQA4ADUAAAtfADEAOQA5ADUAAAtfADIAMAAwADMAAAltAGEAcwBzAAANdwBlAGkAZwBoAHQAAAlmAHUAZQBsAAATcgBhAG4AZwBlAGkAbgBrAG0AAB9hAGMAdAB1AGEAbAByAGEAbgBnAGUAaQBuAGsAbQAAB18AYQBwAAAHXwBmAHAAACFtAG8AdABpAG8AbgBjAG8AbgB0AHIAbwBsAGwAZQByAAAXZgBsAGkAZwBoAHQAbQBvAGQAZQBsAAAbZgBsAGkAZwBoAHQAcABoAHkAcwBpAGMAcwAAFXAAYQByAGEAbQBlAHQAZQByAHMAABdwAGUAcgBmAG8AcgBtAGEAbgBjAGUAABNTAGUAYQBQAG8AdwBlAHIALgAAFVAAYQByAGEAbQBlAHQAZQByAHMAAA9QAGgAeQBzAGkAYwBzAAAVQwBvAG4AdAByAG8AbABsAGUAcgAAF0YAbABpAGcAaAB0AE0AbwBkAGUAbAAADXMAYwBoAGUAbQBhAAADLgAAAzoAAA1tAGUAdAByAGkAYwAAEWEAaQByAGMAcgBhAGYAdAAANUEAbQBtAHUAbgBpAHQAaQBvAG4AQQBtAG8AdQBuAHQARABpAGMAdABpAG8AbgBhAHIAeQAADXMAdABhAHQAdQBzAAAnaQBuAHYAZQBuAHQAbwByAHkAXwBhAHYAYQBpAGwAYQBiAGwAZQAAB0sAZQB5AAAVYQBtAG0AdQBuAGkAdABpAG8AbgAASUEAbQBtAHUAbgBpAHQAaQBvAG4ATgBhAG0AZQBUAG8AQQBtAG0AdQBuAGkAdABpAG8AbgBEAGkAYwB0AGkAbwBuAGEAcgB5AAApYQBtAG0AdQBuAGkAdABpAG8AbgBfAHAAYQByAGEAbQBlAHQAZQByAAAnUgBBAE4ALQBGADEAMQAxAE4ALQB3AGUAaQBnAGgAdAAtAFYAOAAAFXcAZQBpAGcAaAB0AC0AdgA4AC0AAC95AHkAeQB5AE0ATQBkAGQALQBIAEgAbQBtAHMAcwAtAGYAZgBmAGYAZgBmAGYAAAkuAGMAcwB2AABtcwBhAG0AcABsAGUALAByAGUAYQBsAHQAaQBtAGUAXwBzACwAdQBuAGkAdABfAGsAZQB5ACwAYQBpAHIAYwByAGEAZgB0AF8AaQBkACwA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAMAAAAcDcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  # populated by authoring/build_weight_monitor.py
PLUGIN_SHA256 = '03589138f925f1c955bc74142d3334b3823600f259e74d8e3f34c66fd83d2f46'
CATALOG = {'ran_nw_aim9l': {'name': 'AIM-9L Sidewinder', 'mass_kg': 86, 'earliest_edition': 1980, 'native_donor': 'usn_aim-9l', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_aim9m': {'name': 'AIM-9M Sidewinder', 'mass_kg': 86, 'earliest_edition': 1985, 'native_donor': 'usn_aim-9m', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_aim7f': {'name': 'AIM-7F Sparrow', 'mass_kg': 231, 'earliest_edition': 1980, 'native_donor': 'usn_aim-7f', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_aim7m': {'name': 'AIM-7M Sparrow', 'mass_kg': 231, 'earliest_edition': 1985, 'native_donor': 'usn_aim-7m', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_aim54a': {'name': 'AIM-54A Phoenix', 'mass_kg': 443, 'earliest_edition': 1980, 'native_donor': 'usn_aim-54a', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_aim54c': {'name': 'AIM-54C Phoenix', 'mass_kg': 463, 'earliest_edition': 1985, 'native_donor': 'usn_aim-54a', 'model': 'Native geometry', 'simulation': 'Native AIM-54A geometry and flight profile with C mass and estimated improved ECCM'}, 'ran_nw_aim120b': {'name': 'AIM-120B AMRAAM', 'mass_kg': 152, 'earliest_edition': 1995, 'native_donor': 'usn_aim-54a', 'model': 'Original simplified dimensional AMRAAM mesh', 'simulation': 'Active radar homing; no simulated launch-platform midcourse datalink; engagement range is a game estimate, not a published missile limit'}, 'ran_nw_aim120c5': {'name': 'AIM-120C-5 AMRAAM', 'mass_kg': 152, 'earliest_edition': 2003, 'native_donor': 'usn_aim-54a', 'model': 'Original simplified dimensional AMRAAM mesh', 'simulation': 'Active radar homing; no simulated launch-platform midcourse datalink; engagement range is a game estimate, not a published missile limit; C-5 ECCM is an estimated improvement over B'}, 'ran_nw_asraam': {'name': 'ASRAAM', 'mass_kg': 88, 'earliest_edition': 2003, 'native_donor': 'usn_aim-9m', 'model': 'Original simplified dimensional ASRAAM mesh', 'simulation': 'Native IR homing approximation; no helmet sight or lock-on-after-launch simulation'}, 'ran_nw_harpoona': {'name': 'AGM-84A Harpoon', 'mass_kg': 526, 'earliest_edition': 1980, 'native_donor': 'usn_agm-84a', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_harpoonc': {'name': 'AGM-84C Harpoon', 'mass_kg': 526, 'earliest_edition': 1985, 'native_donor': 'usn_agm-84c', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_harpoond': {'name': 'AGM-84D Harpoon Block 1C', 'mass_kg': 526, 'earliest_edition': 1995, 'native_donor': 'usn_agm-84d', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_harpoonl': {'name': 'AGM-84L Harpoon Block II', 'mass_kg': 526, 'earliest_edition': 2003, 'native_donor': 'usn_agm-84d', 'model': 'Native geometry', 'simulation': 'Block II acquisition/integration assumed. Native radar-homing ship attack only; GPS route planning and coastal land-attack mode are not simulated'}, 'ran_nw_maverickb': {'name': 'AGM-65B Maverick', 'mass_kg': 208, 'earliest_edition': 1980, 'native_donor': 'usn_agm-65b', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_maverickd': {'name': 'AGM-65D Maverick', 'mass_kg': 218, 'earliest_edition': 1985, 'native_donor': 'usn_agm-65b', 'model': 'Native geometry', 'simulation': 'Native Maverick geometry with IIR homing and selected variant mass'}, 'ran_nw_maverickg': {'name': 'AGM-65G Maverick', 'mass_kg': 302, 'earliest_edition': 1995, 'native_donor': 'usn_agm-65b', 'model': 'Native geometry', 'simulation': 'Native Maverick geometry with IIR homing and selected variant mass'}, 'ran_nw_standardarm': {'name': 'AGM-78 Standard ARM', 'mass_kg': 620, 'earliest_edition': 1980, 'native_donor': 'usn_agm-78', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_shrike': {'name': 'AGM-45 Shrike', 'mass_kg': 178, 'earliest_edition': 1980, 'native_donor': 'usn_agm-45', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_harma': {'name': 'AGM-88A HARM', 'mass_kg': 361, 'earliest_edition': 1985, 'native_donor': 'usn_agm-88a', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_harmc': {'name': 'AGM-88C HARM', 'mass_kg': 361, 'earliest_edition': 1995, 'native_donor': 'usn_agm-88a', 'model': 'Native geometry', 'simulation': 'Native HARM-A geometry/flight model with estimated C seeker resilience'}, 'ran_nw_mk82': {'name': 'Mk 82 500-lb GP bomb', 'mass_kg': 227, 'earliest_edition': 1980, 'native_donor': 'usn_mk-82', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_mk83': {'name': 'Mk 83 1000-lb GP bomb', 'mass_kg': 454, 'earliest_edition': 1980, 'native_donor': 'usn_mk-83', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_mk84': {'name': 'Mk 84 2000-lb GP bomb', 'mass_kg': 907, 'earliest_edition': 1980, 'native_donor': 'usn_mk-84', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_gbu10': {'name': 'GBU-10 Paveway II', 'mass_kg': 934, 'earliest_edition': 1980, 'native_donor': 'usn_gbu-10', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_gbu12': {'name': 'GBU-12 Paveway II', 'mass_kg': 277, 'earliest_edition': 1980, 'native_donor': 'usn_gbu-12', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_gbu16': {'name': 'GBU-16 Paveway II', 'mass_kg': 495, 'earliest_edition': 1980, 'native_donor': 'usn_gbu-16', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_gbu15': {'name': 'GBU-15 electro-optical glide bomb', 'mass_kg': 1130, 'earliest_edition': 1985, 'native_donor': 'usaf_gbu-15', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_gbu24': {'name': 'GBU-24 Paveway III', 'mass_kg': 1084, 'earliest_edition': 1985, 'native_donor': 'usn_gbu-24', 'model': 'Native geometry', 'simulation': 'Native guidance; rounded historical carried mass'}, 'ran_nw_popeye': {'name': 'AGM-142 Popeye / Have Nap', 'mass_kg': 1360, 'earliest_edition': 1995, 'native_donor': 'usn_agm-65b', 'model': 'Original simplified dimensional AGM-142 Popeye / Have Nap mesh', 'simulation': 'Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated'}, 'ran_nw_slam': {'name': 'AGM-84E SLAM', 'mass_kg': 628, 'earliest_edition': 1995, 'native_donor': 'usn_agm-65b', 'model': 'Original simplified dimensional AGM-84E SLAM mesh', 'simulation': 'Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated'}, 'ran_nw_slamer': {'name': 'AGM-84K SLAM-ER', 'mass_kg': 675, 'earliest_edition': 2003, 'native_donor': 'usn_agm-65b', 'model': 'Original simplified dimensional AGM-84K SLAM-ER mesh', 'simulation': 'Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated'}, 'ran_nw_gbu31': {'name': 'GBU-31 JDAM Mk 84', 'mass_kg': 925, 'earliest_edition': 2003, 'native_donor': 'usn_mk-84', 'model': 'Original simplified dimensional GBU-31 JDAM Mk 84 mesh', 'simulation': 'Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation'}, 'ran_nw_gbu32': {'name': 'GBU-32 JDAM Mk 83', 'mass_kg': 461, 'earliest_edition': 2003, 'native_donor': 'usn_mk-83', 'model': 'Original simplified dimensional GBU-32 JDAM Mk 83 mesh', 'simulation': 'Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation'}, 'ran_nw_jsowa': {'name': 'AGM-154A JSOW', 'mass_kg': 483, 'earliest_edition': 2003, 'native_donor': 'usn_mk-84', 'model': 'Original simplified dimensional AGM-154A JSOW mesh', 'simulation': 'Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation'}, 'ran_tank_600_f111n': {'name': '600 US-gallon fuel tank', 'mass_kg': 150, 'fuel_kg': 1770, 'earliest_edition': 1980, 'simulation': 'Fuel from flight-manual capacity table; dry shell mass is an engineering allowance'}, 'ran_tank_600_fb111n': {'name': '600 US-gallon fuel tank', 'mass_kg': 150, 'fuel_kg': 1770, 'earliest_edition': 1980, 'simulation': 'Fuel from flight-manual capacity table; dry shell mass is an engineering allowance'}, 'ran_tank_600_rf111n': {'name': '600 US-gallon fuel tank', 'mass_kg': 150, 'fuel_kg': 1770, 'earliest_edition': 1980, 'simulation': 'Fuel from flight-manual capacity table; dry shell mass is an engineering allowance'}, 'ran_tank_600_ef111n': {'name': '600 US-gallon fuel tank', 'mass_kg': 150, 'fuel_kg': 1770, 'earliest_edition': 1980, 'simulation': 'Fuel from flight-manual capacity table; dry shell mass is an engineering allowance'}, 'ran_alq-131n_1': {'name': 'Naval offensive ECM pod 1', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation'}, 'ran_nw_ecmpod_1': {'name': 'MudPig removable offensive ECM pod 1', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation'}, 'ran_alq-131n_2': {'name': 'Naval offensive ECM pod 2', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation'}, 'ran_nw_ecmpod_2': {'name': 'MudPig removable offensive ECM pod 2', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation'}, 'ran_nw_datalink': {'name': 'EO weapon control pod', 'mass_kg': 260, 'earliest_edition': 1985, 'simulation': 'Estimated pod mass with existing pod geometry and native sensor; full historical pod shape is not reproduced'}, 'ran_nw_laserpod': {'name': 'External laser designation pod', 'mass_kg': 150, 'earliest_edition': 1980, 'simulation': 'Estimated pod mass with existing pod geometry and native sensor; full historical pod shape is not reproduced'}, 'ran_nw_mk82_mer': {'name': 'Mk 82 on six-bomb rack', 'mass_kg': 243.66666666666666, 'earliest_edition': 1980, 'simulation': '227 kg nominal bomb plus one-sixth of an estimated 100 kg detachable MER; no separate unsupported hardpoint mass key'}, 'ran_alq-131n_1_1980': {'name': 'Naval offensive ECM pod 1 (1980)', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_1_1980': {'name': 'Naval offensive ECM pod 1 (1980)', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_2_1980': {'name': 'Naval offensive ECM pod 2 (1980)', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_2_1980': {'name': 'Naval offensive ECM pod 2 (1980)', 'mass_kg': 260, 'earliest_edition': 1980, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_1_1985': {'name': 'Naval offensive ECM pod 1 (1985)', 'mass_kg': 260, 'earliest_edition': 1985, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_1_1985': {'name': 'Naval offensive ECM pod 1 (1985)', 'mass_kg': 260, 'earliest_edition': 1985, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_2_1985': {'name': 'Naval offensive ECM pod 2 (1985)', 'mass_kg': 260, 'earliest_edition': 1985, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_2_1985': {'name': 'Naval offensive ECM pod 2 (1985)', 'mass_kg': 260, 'earliest_edition': 1985, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_1_1995': {'name': 'Naval offensive ECM pod 1 (1995)', 'mass_kg': 260, 'earliest_edition': 1995, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_1_1995': {'name': 'Naval offensive ECM pod 1 (1995)', 'mass_kg': 260, 'earliest_edition': 1995, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_2_1995': {'name': 'Naval offensive ECM pod 2 (1995)', 'mass_kg': 260, 'earliest_edition': 1995, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_2_1995': {'name': 'Naval offensive ECM pod 2 (1995)', 'mass_kg': 260, 'earliest_edition': 1995, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_1_2003': {'name': 'Naval offensive ECM pod 1 (2003)', 'mass_kg': 260, 'earliest_edition': 2003, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_1_2003': {'name': 'Naval offensive ECM pod 1 (2003)', 'mass_kg': 260, 'earliest_edition': 2003, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_alq-131n_2_2003': {'name': 'Naval offensive ECM pod 2 (2003)', 'mass_kg': 260, 'earliest_edition': 2003, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}, 'ran_nw_ecmpod_2_2003': {'name': 'Naval offensive ECM pod 2 (2003)', 'mass_kg': 260, 'earliest_edition': 2003, 'simulation': 'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}}
GUID = "com.gobertron.f111n.weight.v8"
FOLDER = "RANF111NWeightMonitorV8"
DLL = "RANF111NWeightMonitorV8.dll"
MASS_NAMES = {"mass", "totalmass", "currentmass", "grossmass", "aircraftmass", "weight", "totalweight", "currentweight"}
FUEL_NAMES = {"fuelmass", "currentfuelmass", "remainingfuelmass", "fuelweight", "currentfuelweight"}


def normal(name):
    return re.sub(r"[^a-z]", "", name.rsplit(".", 1)[-1].lower())


def game_running():
    for process in Path("/proc").glob("[0-9]*/comm"):
        try:
            if process.read_text().strip().lower() in {"sea power.exe", "seapower.exe", "sea power", "seapower"}:
                return True
        except (OSError, UnicodeError):
            pass
    return False


def check_game(game):
    if not (game / "Sea Power_Data/StreamingAssets").is_dir():
        raise RuntimeError("This is not a Sea Power folder: " + str(game))


def install(game, remove=False):
    check_game(game)
    if game_running():
        raise RuntimeError("Close Sea Power before installing or removing the monitor.")
    parent = game / "BepInEx/plugins"
    destination = parent / FOLDER
    for path in (game / "BepInEx", parent, destination):
        if path.is_symlink():
            raise RuntimeError("Refusing a symlink in the monitor installation path: " + str(path))
    marker = destination / "monitor-v8.json"
    if destination.exists():
        try:
            data = json.loads(marker.read_text())
        except (OSError, ValueError):
            raise RuntimeError("The monitor destination has unrecognised files; nothing was replaced.")
        if data.get("plugin_guid") != GUID:
            raise RuntimeError("The monitor destination belongs to another plugin; nothing was replaced.")
    if remove:
        if destination.exists():
            shutil.rmtree(destination)
        print("[100%] Version 8 weight monitor removed. Recordings have been kept.")
        return
    if not (game / "BepInEx/core/BepInEx.dll").is_file():
        raise RuntimeError("The existing Anchor Chain/BepInEx preloader was not found. Install it before this optional monitor.")
    print("[20%] Sea Power and the existing BepInEx installation found.")
    payload = base64.b64decode(PLUGIN_BASE64, validate=True)
    if not payload or hashlib.sha256(payload).hexdigest() != PLUGIN_SHA256:
        raise RuntimeError("Embedded Version 8 monitor checksum failed.")
    print("[50%] Version 8 monitor checksum verified.")
    parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="weight-v8-stage-", dir=parent))
    old = stage / "previous"
    try:
        (stage / DLL).write_bytes(payload)
        (stage / "monitor-v8.json").write_text(json.dumps({"version": "Version 8", "plugin_guid": GUID, "sha256": PLUGIN_SHA256}, indent=2) + "\n")
        if destination.exists():
            destination.rename(old)
        try:
            destination.mkdir()
            for name in (DLL, "monitor-v8.json"):
                (stage / name).rename(destination / name)
        except BaseException:
            if destination.exists():
                shutil.rmtree(destination)
            if old.exists():
                old.rename(destination)
            raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    print("[100%] Version 8 weight monitor installed: " + str(destination))
    print("Start Sea Power and use a Naval Wing aircraft. The monitor only records state.")
    print("Use MudPig AntiShipHeavy, let it fly for 30 seconds, fire Harpoons, then fly for another minute.")
    print("Close the game, then run this script again with --collect to make the report.")


def load_recording(path):
    snapshots = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["sample", "realtime_s", "unit_key", "aircraft_id", "kind", "name", "value"]:
            raise ValueError("Unrecognised Version 8 recording format")
        for row in reader:
            # A recording may still be open in game. Ignore an unfinished last row.
            try:
                value = float(row["value"])
                sample, realtime = int(row["sample"]), float(row["realtime_s"])
                if not math.isfinite(value) or not math.isfinite(realtime):
                    continue
                key = row["unit_key"], row["aircraft_id"], sample
                snapshot = snapshots.setdefault(key, {"sample": sample, "time": realtime, "unit": key[0], "aircraft": key[1], "metric": {}, "ammunition": {}, "ammunition_parameter": {}, "status": {}})
                if row["kind"] in {"metric", "ammunition", "ammunition_parameter", "status"} and row["name"]:
                    snapshot[row["kind"]][row["name"]] = value
            except (ValueError, TypeError, KeyError):
                continue
    units = {}
    for (_, _, _), snapshot in snapshots.items():
        units.setdefault((snapshot["unit"], snapshot["aircraft"]), []).append(snapshot)
    for values in units.values():
        values.sort(key=lambda s: s["sample"])
    return units


def mass_for(ammunition, first, second, catalog):
    """Prefer the live ammunition parameter; reject disagreeing mass candidates."""
    live = []
    for point in (first, second):
        for path, value in point["ammunition_parameter"].items():
            if path.startswith(ammunition + ".") and normal(path) == "mass" and value > 0:
                live.append(value)
    if live:
        return live[0] if max(live) - min(live) <= .01 else None
    data = catalog.get(ammunition)
    return data["mass_kg"] if data else None


def compare(first, second, catalog):
    if first.get("status", {}).get("inventory_available") != 1 or second.get("status", {}).get("inventory_available") != 1:
        return {"kind": "inventory", "status": "insufficient_data", "reason": "Live inventory was not available in both samples."}
    ammo_delta = {name: first["ammunition"].get(name, 0) - second["ammunition"].get(name, 0)
                  for name in first["ammunition"].keys() | second["ammunition"].keys()}
    changes = {name: count for name, count in ammo_delta.items() if count}
    # Rearming, loadout swaps and pooled respawns are not weapon-release tests.
    if any(count < 0 for count in changes.values()):
        return None
    expected = 0.0
    for name, count in changes.items():
        mass = mass_for(name, first, second, catalog)
        if mass is None:
            return {"kind": "release", "status": "insufficient_data", "reason": "Missing live/catalogued mass for " + name, "released": changes}
        expected += count * mass
    metrics = first["metric"].keys() & second["metric"].keys()
    candidates = [name for name in metrics if normal(name) in MASS_NAMES and first["metric"][name] >= 5000
                  and not any(part in name.lower() for part in ("parameters", "._obp", "._ap", "._fp"))]
    fuels = [name for name in metrics if normal(name) in FUEL_NAMES]
    kind = "release" if changes else "fuel"
    if not changes and not any(first["metric"][f] - second["metric"][f] >= 10 for f in fuels):
        return None
    observations = []
    for name in sorted(candidates):
        actual = first["metric"][name] - second["metric"][name]
        for fuel in sorted(fuels):
            fuel_loss = first["metric"][fuel] - second["metric"][fuel]
            if fuel_loss < -.1:  # refuelling is a separate test
                continue
            predicted = expected + fuel_loss
            # Constant values can never count as evidence of an update.
            matches = predicted > 2 and actual > 0 and abs(actual - predicted) <= 2
            observations.append({"mass_field": name, "fuel_field": fuel, "observed_loss_kg": round(actual, 3),
                                 "weapon_loss_kg": round(expected, 3), "fuel_loss_kg": round(fuel_loss, 3),
                                 "difference_kg": round(actual - predicted, 3), "consistent": matches})
    if not observations:
        return {"kind": kind, "status": "insufficient_data", "released": changes,
                "reason": "No usable live gross-mass/fuel-mass pair was exposed; raw fields are retained."}
    return {"kind": kind, "status": "observed_consistent" if any(o["consistent"] for o in observations) else "mismatch",
            "released": changes, "observations": observations}


def analyse(units, catalog):
    result = {"version": "Version 8", "runtime_tested_here": False, "units": [], "scope": "Observed game fields and inventory; this is not flight-performance or carrier certification."}
    for (key, aircraft), points in sorted(units.items()):
        events = []
        fuel_anchor = points[0]
        for previous, second in zip(points, points[1:]):
            changed = previous["ammunition"] != second["ammunition"]
            event = compare(previous if changed else fuel_anchor, second, catalog)
            if event is not None:
                event["sample"] = second["sample"]
                events.append(event)
            # Accumulate small per-second burns until a useful fuel-only delta
            # exists; reset at releases, rearming or a completed observation.
            if changed or event is not None:
                fuel_anchor = second
        result["units"].append({"unit_key": key, "aircraft": aircraft, "samples": len(points),
                                "metric_fields": sorted({name for p in points for name in p["metric"]}), "events": events})
    result["release_observed"] = any(e["kind"] == "release" and e["status"] == "observed_consistent" for u in result["units"] for e in u["events"])
    result["fuel_burn_observed"] = any(e["kind"] == "fuel" and e["status"] == "observed_consistent" for u in result["units"] for e in u["events"])
    return result


def report(game, collect=False):
    check_game(game)
    folder = game / "RAN-F111N-weight-V8"
    recordings = sorted(folder.glob("weight-v8-*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    for path in recordings:
        units = load_recording(path)
        if units:
            break
    else:
        raise RuntimeError("No aircraft samples yet. Start a mission with V8 aircraft, then use --collect after the test. Check BepInEx/LogOutput.log for 'Weight Monitor' if no recording appears.")
    result = analyse(units, CATALOG)
    result["recording"] = path.name
    lines = ["RAN F-111N — Version 8 weight report", "Recording: " + path.name,
             "Weapon release: " + ("observed mass change consistent with released weapons and fuel burn" if result["release_observed"] else "NOT VERIFIED"),
             "Fuel burn: " + ("observed mass change consistent with fuel consumption" if result["fuel_burn_observed"] else "NOT VERIFIED")]
    for unit in result["units"]:
        lines.append(f"\n{unit['aircraft']} ({unit['samples']} samples)")
        for kind in ("release", "fuel", "inventory"):
            events = [e for e in unit["events"] if e["kind"] == kind]
            for status in ("observed_consistent", "mismatch", "insufficient_data"):
                selected = [e for e in events if e["status"] == status]
                if selected:
                    lines.append(f"  {kind}: {len(selected)} {status}")
                    example = selected[0]
                    lines.append("  " + json.dumps(example, sort_keys=True))
    lines += ["", "Raw mass/fuel fields remain in the CSV. Unknown field layouts are reported as unverified.",
              "The monitor never changes aircraft, weapons, fuel, thrust, AI orders or game assemblies."]
    text = "\n".join(lines) + "\n"
    (folder / "weight-report-v8.txt").write_text(text)
    (folder / "weight-report-v8.json").write_text(json.dumps(result, indent=2) + "\n")
    print(text)
    if collect:
        bundle = folder / "weight-results-v8.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
            for source in (path, folder / "weight-report-v8.txt", folder / "weight-report-v8.json"):
                archive.write(source, source.name)
        print("Results ready to share: " + str(bundle))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Version 8 read-only in-game weight monitor")
    parser.add_argument("game", nargs="?", default=str(Path.home() / ".local/share/Steam/steamapps/common/Sea Power"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--remove", action="store_true")
    mode.add_argument("--report", action="store_true")
    mode.add_argument("--collect", action="store_true")
    args = parser.parse_args(argv)
    game = Path(args.game).expanduser().resolve()
    if args.report or args.collect:
        report(game, args.collect)
    else:
        install(game, args.remove)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print("Version 8 weight check stopped: " + str(error), file=sys.stderr)
        sys.exit(1)

V8_WEIGHT_PY
