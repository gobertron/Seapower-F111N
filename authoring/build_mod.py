#!/usr/bin/env python3
"""Rebuild V8 data in the extracted package; existing visual assets are reused."""
from era_upgrade import read_ini,write_ini,ROOT,MOD,main,ROLES
OUT=ROOT
# Compatibility exports for the retained visual authoring utilities. Texture
# painting requires the original source ZIPs; rendering uses shipped assets.
U=ROOT/'authoring/sources/3587484531/3587484531'
F=ROOT/'authoring/sources/3689650533/3689650533'
VARIANTS={role:{'name':v[0],'nickname':v[1],'model':'ef-111' if role=='ef' else 'f-111f'} for role,v in ROLES.items()}
if __name__=='__main__':main()
