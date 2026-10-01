from pathlib import Path
from tempfile import TemporaryDirectory
import sys,json,shutil,hashlib,subprocess
package=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(package))
from carrier_compatibility import compatible,parse,generate,IDS
checks=0
def check(ok,message):
    global checks
    checks+=1
    assert ok,message
reference=package/'authoring/reference_carriers'
for source in sorted(reference.glob('*.ini')):
    text=source.read_text();result=compatible(text,source.stem)
    if not result:continue
    output,report=result;before=parse(text);after=parse(output)
    check(after.get('AirGroup')==before.get('AirGroup'),source.name+': air group changed')
    for section in before:
        if section not in ['FlightDeck'] and not section.startswith(('RecoveryPoint','LaunchPoint','Elevator','TaxiPath')):
            check(after.get(section)==before[section],source.name+': unrelated section '+section)
    for section in ['General','Models','SensorSystems','WeaponSystems']:
        check(after.get(section)==before.get(section),source.name+': systems changed')
    check(compatible(output,source.stem)[0]==output,source.name+': not idempotent')
    check('Arrested=True' in output,source.name+': no arrested recovery')
    for section,data in before.items():
        if section.startswith('RecoveryPoint') and 'Plane' not in data.get('AllowedType',''):
            for key in ['Position','Rotation','AllowedType','CircuitWaypoints','HelicopterCircuitWaypoints']:
                check(after[section].get(key)==data.get(key),source.name+': changed prior '+section+'/'+key)

with TemporaryDirectory(prefix='ran-carrier-qa-') as temp:
    root=Path(temp);game=root/'steamapps/common/Sea Power'
    native=game/'Sea Power_Data/StreamingAssets/original/vessels';native.mkdir(parents=True)
    native_text=(reference/'usn_cvn_nimitz.ini').read_text().replace('[FlightDeck]', '[FlightDeck]\nAircraftSupported=usn_f-14a')
    (native/'usn_cvn_nimitz.ini').write_text(native_text)
    workshop=root/'steamapps/workshop/content/1286220/3574957049/vessels';workshop.mkdir(parents=True)
    # Representative RAN filename/placement using native deck geometries.
    # These are fixtures, not the user's actual RAN carrier definitions.
    fixtures={'ran_cv_centaur_catobar.ini':'usn_cvn_nimitz.ini', 'hms_ark_royal.ini':'usn_cvn_nimitz.ini',
        'ran_cv_invincible.ini':'wp_takr_kiev.ini','ran_cv_majestic1968.ini':'usn_cv_forrestal_75.ini'}
    for name,source in fixtures.items():(workshop/name).write_bytes((reference/source).read_bytes())
    source_hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in [*native.glob('*.ini'),*workshop.glob('*.ini')]}
    user=game/'Sea Power_Data/StreamingAssets/user'
    old=user/'RAN-F111N-Naval-Wing';(old/'aircraft').mkdir(parents=True)
    (old/'_info.ini').write_text('[Language_en]\nName=RAN F-111N Naval Wing V5.1\n')
    (old/'aircraft/ran_f-111n.ini').write_text('old fixture\n')
    result=subprocess.run([sys.executable,str(package/'install-ran-f111n.py'),str(game)],text=True,capture_output=True)
    check(result.returncode==0,result.stderr+result.stdout)
    check((old/'aircraft/ran_rf-111n.ini').is_file(),'new aircraft missing')
    check(all((old/'vessels'/name).is_file() for name in fixtures),'RAN carrier overrides missing')
    check(len(IDS)==16,'all dated IDs known to carrier installer')
    installed=parse((old/'vessels/usn_cvn_nimitz.ini').read_text())
    check(set(IDS)<=set(installed['FlightDeck']['AircraftSupported'].split(',')),'all dated IDs supported by restricted carrier')
    for name in fixtures:
        d=parse((old/'vessels'/name).read_text())
        check(any('Plane' in d.get('RecoveryPoint'+str(i),{}).get('AllowedType','').split(',') for i in range(1,int(d['FlightDeck']['NumberOfRecoveryPoints'])+1)),name+': no Plane recovery')
    backups=list((game/'RAN-F111N-backups').rglob('aircraft/ran_f-111n.ini'))
    check(len(backups)==1 and backups[0].read_text()=='old fixture\n','old version backup missing')
    check(all(hashlib.sha256(p.read_bytes()).hexdigest()==digest for p,digest in source_hashes.items()),'source carrier files changed')
    print(result.stdout.strip())
    report=json.loads((old/'CARRIER_COMPATIBILITY.json').read_text())
    check(not report['errors'],'carrier report errors')

out={'status':'PASS','checks':checks,'runtime_tested':False,
    'scope':'Native carrier conversion, active Plane recovery/launch, existing systems and air-group preservation, VTOL/heli approach preservation, idempotence, RAN-named deck fixtures, installer staging and prior-version backup, source files unchanged. RAN fixtures are representative native layouts, not actual installed RAN source files.'}
(package/'CARRIER_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
