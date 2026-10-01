#!/usr/bin/env python3
"""Static content validation, independent of the Sea Power runtime."""
from pathlib import Path
from collections import Counter
import re,json,sys
import numpy as np
from PIL import Image
from build_mod import read_ini,ROOT,OUT,MOD,U,F,VARIANTS

# Also validate the shipped package without requiring the original Workshop ZIPs.
package = Path(__file__).resolve().parent.parent
if (package/'RAN-F111N-Naval-Wing').is_dir():
    OUT = package
    MOD = package/'RAN-F111N-Naval-Wing'

def main():
    failures=[];checks=0;objects={}
    def check(ok,message):
        nonlocal checks
        checks+=1
        if not ok:failures.append(message)
    for p in MOD.rglob('*.ini'):
        seen=set();sec=''
        for line in p.read_text().splitlines():
            line=line.strip()
            if not line or line.startswith(('#',';')):continue
            if line.startswith('['):sec=line.split(']')[0][1:]
            elif '=' in line:
                key=line.split('=',1)[0]; ident=(sec,key)
                check(ident not in seen,f'{p.name}: duplicate {sec}/{key}');seen.add(ident)
        check('=Ture' not in p.read_text() and '=Ture' not in p.read_text(),f'{p}: malformed Boolean')
    for obj in MOD.rglob('*.obj'):
        objects[obj]=set(re.findall(r'^o (\S+)',obj.read_text(),re.M))
    manifest=json.loads((OUT/'loadout_manifest.json').read_text())
    units={}
    for short,cfg in VARIANTS.items():
        unit='ran_'+short+'-111n';d=read_ini(MOD/f'aircraft/{unit}.ini');units[unit]=d
        active=set(d['Submodels'].values())
        root=MOD/d['Models']['ResourcesFolder']/d['Models']['ResourcesRoot']
        check(root.is_file(),f'{unit}: missing OBJ')
        check(d['Models']['ResourcesMesh'] in objects[root],f'{unit}: missing fuselage mesh')
        for name in active:
            check(name in d,f'{unit}: missing submodel {name}')
            s=d.get(name,{})
            if s.get('RootMesh','').endswith('.obj'):
                op=MOD/s['ResourcesMeshFolder']/s['RootMesh']; check(s.get('Mesh') in objects.get(op,set()),f'{unit}: custom mesh {name}')
            elif 'ResourcesMeshFolder' not in s:
                check(s.get('Mesh') in objects[root],f'{unit}: OBJ group {name}/{s.get("Mesh")}')
            if 'Parent' in s:check(s['Parent'] in active,f'{unit}: parent {s["Parent"]} not active')
            if s.get('Material','').endswith('.ini'):
                folder=s.get('ResourcesMaterialFolder',d['Models']['ResourcesFolder'])
                check((MOD/folder/s['Material']).is_file(),f'{unit}: material {name}')
        for k,v in d['FlightControls'].items():
            if k.endswith('_Model'):check(v in active,f'{unit}: missing flight-control node {v}')
        for k in ['LeftWingModel','RightWingModel']:
            check(d['WingSweep'][k] in active,f'{unit}: {k}')
        n=int(d['WingSweep']['NumberOfAngles'])
        check(all(f'SweepAngle{i}' in d['WingSweep'] and f'SweepSpeed{i}' in d['WingSweep'] for i in range(1,n+1)),f'{unit}: wing-sweep count')
        af=d['Animations']['AnimationFile_1'];ani=read_ini(MOD/'animations'/(af+'.ini'))
        check(af.startswith('animations_ran_'),f'{unit}: global animation collision')
        for i in range(1,int(ani['Animations']['NumberOfAnimations'])+1):
            act=ani['Animations'].get(f'Animation{i}');check(act in ani,f'{unit}: missing animation {act}')
            a=ani.get(act,{})
            for j in range(1,int(a.get('NumberOfSequencesToPlay',0))+1):
                seq=a.get(f'Sequence{j}');node=a.get(f'Sequence{j}_Model')
                check(seq in ani,f'{unit}: missing sequence {seq}');check(node in active,f'{unit}: animation target {node}')
                seqd=ani.get(seq,{})
                count=int(seqd.get('NumberOfSteps',0))
                check(count>0 and all(f'Step{k}' in seqd for k in range(1,count+1)),f'{unit}: sequence step count {seq}')
                for k in range(1,count+1):
                    components=seqd[f'Step{k}'].split('|')
                    check(len(components)==4 and len(components[1].split(','))==3 and len(components[2].split(','))==3,f'{unit}: malformed step {seq}')
        presets=d['WeaponSystems']['AvailableLoadouts'].split(',');check(presets[0]=='Default',f'{unit}: default preset')
        if short != 'fb':
            check('AntiShip' not in ','.join(presets),f'{unit}: unexpected anti-ship presets')
        else:
            check({'AntiShip','AntiShipHeavy','AntiShipLongRange'} <= set(presets),f'{unit}: missing maritime presets')
        check(int(d['SensorSystems']['NumberOfSensorSystems'])==len([s for s in d if re.fullmatch('SensorSystem[0-9]+',s)]),f'{unit}: sensor count')
        check(int(d['WeaponSystems']['NumberOfWeaponSystems'])==len([s for s in d if re.fullmatch('WeaponSystem[0-9]+',s)]),f'{unit}: weapon-system count')
        inventory={name:Counter() for name in presets}
        by_system={name:{} for name in presets}
        for i in range(1,int(d['WeaponSystems']['NumberOfWeaponSystems'])+1):
            ws=d[f'WeaponSystem{i}']
            if ws['Type']!='Hardpoint':continue
            n=int(ws['NumberOfStations'])
            check(all(f'Station{k}' in ws for k in range(1,n+1)),f'{unit}: station count {i}')
            check(ws['AssociatedSensors'] in d,f'{unit}: hardpoint sensor {i}')
            for k,v in ws.items():
                if re.fullmatch('Station[0-9]+Parent',k):
                    check(v in active,f'{unit}: hardpoint parent {v}')
            for key in ['OpenSystemAnimation','CloseSystemAnimation']:
                if key in ws:
                    check(ws[key] in ani,f'{unit}: unknown weapon animation {ws[key]}')
            for name in presets:
                ld=d.get(f'WeaponSystem{i}{name}',{})
                counts=Counter()
                for key,value in ld.items():
                    if not re.fullmatch('Station[0-9]+',key):continue
                    check(int(key[7:])<=n,f'{unit}: loadout station out of range')
                    amm=value.split('|')[0].split('*')[0]
                    check('*' not in value,f'{unit}: non-native store multiplier; use rack positions')
                    if amm.startswith('ran_'):check((MOD/'ammunition'/(amm+'.ini')).is_file(),f'{unit}: ammo {amm}')
                    if '|' in value:
                        rack=value.split('|')[1];check(rack+'Positions' in ws,f'{unit}: missing store offset {rack}')
                        quantity=len(ws.get(rack+'Positions','').split('|'))
                    else:quantity=1
                    counts[amm]+=quantity
                inventory[name].update(counts)
                by_system[name][i]=counts
        check(set(manifest[unit]['loadouts'])==set(presets),f'{unit}: manifest preset list')
        for name,spec in manifest[unit]['loadouts'].items():
            st=spec['stores'];ntanks=sum(v for k,v in st.items() if k.startswith('ran_tank_'))
            check(dict(inventory.get(name,{}))==st,f'{unit}: manifest inventory mismatch for {name}')
            check(spec['total_fuel_kg']==int(d['Performance']['MaxFuel'])+ntanks*1800,f'{unit}: fuel summary for {name}')
            if 'LongRange' in name:check(ntanks>=2,f'{unit}: long-range tanks')
            if short=='rf':check(st.get('usn_aim-9l')==2 and ntanks==4 and len(st)==2,f'{unit}: recon stores')
            if short=='ef':check(st.get('usn_aim-9l')==2 and ntanks==2 and sum(v for k,v in st.items() if k.startswith('ran_alq'))==2,f'{unit}: EW stores')
            if short=='fb' and name!='AntiShipHeavy':
                check(st.get('usn_aim-9l')==2,f'{unit}: defensive AAM for {name}')
        if short=='fb':
            expected={
                'AntiShip':({ 'usn_aim-9l':2,'usn_agm-84c':2},{}),
                'AntiShipHeavy':({'usn_agm-84c':4},{'usn_agm-84c':3}),
                'AntiShipLongRange':({'usn_aim-9l':2,'usn_agm-84c':2,'ran_tank_600_fb111n':2},{'usn_agm-84c':3}),
            }
            for name,(wing,bay) in expected.items():
                check(dict(by_system.get(name,{}).get(1,{}))==wing,f'{unit}: exact wing stores for {name}')
                check(dict(by_system.get(name,{}).get(3,{}))==bay,f'{unit}: exact internal stores for {name}')
                check(manifest[unit]['loadouts'][name].get('wing_stores')==wing,f'{unit}: wing summary for {name}')
                check(manifest[unit]['loadouts'][name].get('internal_bay_stores')==bay,f'{unit}: bay summary for {name}')
                check(d['WeaponSystem1'+name].get('LevelAttack')=='Missiles',f'{unit}: missile attack mode for {name}')
            bay=d['WeaponSystem3']
            check(bay['SystemName']=='BombBay' and bay['HideWeaponsInsideSystem']=='True',f'{unit}: concealed internal bay')
            check(d['Animations']['AnimationFile_1']=='animations_ran_fb111n',f'{unit}: isolated MudPig animation')
            for name in ('AntiShipHeavy','AntiShipLongRange'):
                hidden=set(d['WeaponSystem1'+name]['SubModelsToHide'].split(','))
                check({'pave','pave_body'}<=hidden,f'{unit}: Pave Tack occupies the missile bay for {name}')
            for action in ('Bay_Open','Bay_Close'):
                nodes={ani[action][f'Sequence{i}_Model'] for i in range(1,int(ani[action]['NumberOfSequencesToPlay'])+1)}
                check(nodes=={'bay_l','bay_r'},f'{unit}: missile-bay door targets for {action}')
        check(d['General'].get('CarrierCapable')=='True',f'{unit}: carrier capability')
        if short=='ef':
            systems=read_ini(MOD/'systems/sensors.ini')
            offensive=[v for k,v in d.items() if re.fullmatch(r'SensorSystem\d+',k)
                and systems.get(v.get('SystemName'),{}).get('Type')=='Offensive']
            check(len(offensive)==2,f'{unit}: exactly two aircraft offensive ECM systems')
            check({v['Mount'] for v in offensive}=={'hang1','hang2'},f'{unit}: distinct pylon-mounted ECM sensors')
            check(not any(v.get('Type')=='LaserDesignator' for v in d.values()),f'{unit}: inappropriate laser designator')
            for i in [1,2]:
                pod=read_ini(MOD/f'ammunition/ran_alq-131n_{i}.ini')
                check('SensorSystems' not in pod,f'{unit}: duplicate container ECM')
            from paint_textures import load_obj
            verts,uv,norms,groups=load_obj(MOD/'assets/ran_f111n/models/alq-131/alq-131.obj')
            podtop=verts[groups['AN_ALQ_131'][:,:,0],1].max()
            for station,parent,wing in [(5,'hang2','right_wing'),(6,'hang1','left_wing')]:
                source,_,_,pg=load_obj(MOD/'assets/ran_f111n/models/ef-111/ef-111.obj')
                bottom=source[pg[parent][:,:,0],1].min()+float(d[parent]['Position'].split(',')[1])+float(d[wing]['Position'].split(',')[1])
                top=float(d['WeaponSystem1'][f'Station{station}'].split(',')[1])+podtop
                check(abs(top-bottom)<0.0003,f'{unit}: ECM pod-to-pylon gap at {parent}')
        if short=='rf':
            check(float(d['Performance']['MachLimit'])==3 and float(d['Performance']['MaxFuel'])>10000,f'{unit}: recon performance')
            check(float(d['Performance']['SpeedAndRange_Cruise'].split(',')[0])==2.52,f'{unit}: threefold cruise speed')
            check(float(d['Performance']['MaxSpeedAtSeaLevel'])>=1984,f'{unit}: low-altitude speed cap blocks Mach 3')
            check(all(float(d['Performance'][k].split(',')[0])==3 for k in ['SpeedAndRange_Max','SpeedAndRange_Afterburner']),f'{unit}: Mach 3 throttle settings')
        src=U/'assets/textures/ef-111/42nd_ECS.png' if short=='ef' else F/'assets/textures/f-111c'/('rf-111c.png' if short=='rf' else 'f-111c.png')
        orig=np.asarray(Image.open(src)) if src.is_file() else None
        for suffix in ['', '_1990']:
            p=MOD/f'assets/textures/ran_f111n/{unit}{suffix}.png'
            check(p.is_file(),f'{unit}: missing texture')
            if p.is_file():
                tex=np.asarray(Image.open(p));check(tex.shape==(orig.shape if orig is not None else (2048,3072,4)),f'{unit}: texture shape')
                if orig is not None:
                    check(np.array_equal(tex[:,:,3],orig[:,:,3]),f'{unit}: alpha channel changed')
                    check(np.array_equal(tex[1024:,2048:],orig[1024:,2048:]),f'{unit}: cockpit pixels changed')
    for p in MOD.rglob('*_mat.ini'):
        for v in read_ini(p).get('Textures',{}).values():check((MOD/v).is_file(),f'{p.name}: missing texture {v}')
    for p in (MOD/'vessels').glob('*.ini'):
        d=read_ini(p);deck=d['FlightDeck']
        nr=int(deck['NumberOfRecoveryPoints']);nl=int(deck['NumberOfLaunchPoints'])
        recoveries=[d.get(f'RecoveryPoint{i}',{}) for i in range(1,nr+1)]
        launches=[d.get(f'LaunchPoint{i}',{}) for i in range(1,nl+1)]
        check(all(recoveries) and all(launches),f'{p.name}: active deck point count')
        fixed=[(i,point) for i,point in enumerate(recoveries,1) if 'Plane' in point.get('AllowedType','').split(',')]
        check(bool(fixed),f'{p.name}: no fixed-wing recovery')
        check(any('Plane' in point.get('AllowedType','').split(',') for point in launches),f'{p.name}: no fixed-wing launch')
        for i,point in fixed:
            check(point.get('Arrested')=='True',f'{p.name}: fixed-wing arresting support')
            check('CircuitWaypoints' in point,f'{p.name}: fixed-wing approach route')
            for elevator in point['AssociatedElevators'].split(','):
                check('Elevator'+elevator in d,f'{p.name}: missing recovery elevator')
            check(any(v.get('From')==f'RecoveryPoint{i}' for k,v in d.items() if re.fullmatch('TaxiPath[0-9]+',k)),f'{p.name}: no recovery taxi route')
    native_manifest=set(re.findall(r'"(usn_[^"]+)"',(OUT/'loadout_manifest.json').read_text()))
    result={'status':'PASS' if not failures else 'FAIL','checks':checks,'failures':failures,
        'game_target':'0.8.x; V5 baseline targets 0.8.2',
        'runtime_tested':False,'scope':'Static file, mesh, animation, attachment, exact store and fuel validation; two independently mounted offensive ECM systems; configured Mach 2.52 cruise and Mach 3 maximum; fixed-wing carrier recovery, launch and elevator/taxi routes. Original texture/alpha comparison runs when source textures are available. Sea Power runtime testing is still required.',
        'native_ammunition_references':sorted(native_manifest)}
    (OUT/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return bool(failures)

if __name__=='__main__':sys.exit(main())
