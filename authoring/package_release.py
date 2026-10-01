#!/usr/bin/env python3
"""Package V7 assets, data, docs and source only after current checks pass."""
from pathlib import Path
import argparse,hashlib,json,zipfile
from era_upgrade import ROOT,MOD

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT.parent/'RAN-F111N-Naval-Wing-V7.zip')
    output=parser.parse_args().output.resolve()
    for filename in ('VALIDATION.json','CARRIER_VALIDATION.json','USN_TEXTURE_VALIDATION.json'):
        if json.loads((ROOT/filename).read_text()).get('status')!='PASS':raise SystemExit('Cannot package: '+filename+' is not PASS')
    hashes={name:digest for digest,name in (line.split('  ',1) for line in (ROOT/'MOD_SHA256.txt').read_text().splitlines())}
    current={str(p.relative_to(MOD)) for p in MOD.rglob('*') if p.is_file()}
    if current!=set(hashes):raise SystemExit('Cannot package: mod file set changed since hashing')
    for name,digest in hashes.items():
        if hashlib.sha256((MOD/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Cannot package: checksum changed '+name)
    required=('README.md','COMPLETE_BREAKDOWN_V7.md','docs/AIRCRAFT_COMPARISON.md','docs/INVESTMENT_PROGRAMME.md','ALL_LOADOUTS_V7.csv','investment_manifest.json','RELEASE_NOTES_V7.md','WORKSHOP_DESCRIPTION.txt')
    if any(not (ROOT/name).is_file() for name in required):raise SystemExit('Cannot package: release documentation incomplete')
    output.parent.mkdir(parents=True,exist_ok=True);count=0
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file():continue
            relative=path.relative_to(ROOT)
            if any(p in ('.git','__pycache__','.venv','dist','sources') for p in relative.parts):continue
            if path==output or path.suffix in ('.pyc','.zip'):continue
            archive.write(path,'RAN-F111N-Naval-Wing-V7/'+str(relative));count+=1
    with zipfile.ZipFile(output) as archive:
        bad=archive.testzip()
        if bad:raise SystemExit('ZIP integrity failure: '+bad)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.sha256').write_text(digest+'  '+output.name+'\n')
    print(json.dumps({'file':str(output),'bytes':output.stat().st_size,'MiB':round(output.stat().st_size/1024**2,2),'entries':count,'sha256':digest,'zip_integrity':'PASS'}))
if __name__=='__main__':main()
