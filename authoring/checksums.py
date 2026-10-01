#!/usr/bin/env python3
"""Refresh mod hashes after data/assets/carrier overrides change."""
import hashlib
from era_upgrade import ROOT,MOD

def main():
    files=sorted(p for p in MOD.rglob('*') if p.is_file())
    (ROOT/'MOD_SHA256.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(MOD)) for p in files)+'\n')
    print(f'Checksummed {len(files)} mod files.')
if __name__=='__main__':main()
