#!/usr/bin/env python3
"""Static checks of dated stores, investment, mass, roles and native assets."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,sys
from era_upgrade import read_ini,MOD,ROOT,BASE,NATIVE,YEARS,ROLES,unit_id,inventory,CATALOG
from paint_textures import load_obj,matrix
import numpy as np
from investment_programme import BLOCKS,pod_id,sensor_id
from usn_liveries import protected_pixels
from PIL import Image

def main():
    failures=[];checks=0
    def check(ok,message):
        nonlocal checks
        checks+=1
        if not ok:failures.append(message)
    manifest=json.loads((ROOT/'loadout_manifest.json').read_text())
    catalog=json.loads((ROOT/'weapon_catalog.json').read_text())
    names=read_ini(MOD/'language_en/aircraft_names.ini')
    systems=read_ini(MOD/'systems/sensors.ini')
    native_sensors=read_ini(ROOT/'authoring/reference_sensors.ini')
    ammunition_names=read_ini(MOD/'language_en/ammunition_names.ini')
    ammo_table=ammunition_names.get('AmmunitionNames',{})
    check(set(ammunition_names)=={'AmmunitionNames'},'native flat ammunition language table')
    check(set(ammo_table)==set(catalog),'all custom ammunition IDs have display names')
    local_weapons=read_ini(MOD/'systems/weapons.ini')
    chaff_system=local_weapons.get('RAN_NW_AIR_CHAFF_DISP',{})
    check(chaff_system.get('ReloadTime')=='0','Naval Wing chaff reload is zero')
    check(len(manifest)==16 and set(manifest)==set(names),'exactly sixteen named aircraft')
    for p in MOD.rglob('*.ini'):
        sec='';seen=set()
        for line in p.read_text().splitlines():
            line=line.strip()
            if not line or line.startswith(('#',';')):continue
            if line.startswith('['):sec=line.split(']')[0][1:]
            elif '=' in line:
                ident=(sec,line.split('=',1)[0])
                check(ident not in seen,str(p.relative_to(MOD))+': duplicate '+str(ident));seen.add(ident)
    for key,c in catalog.items():
        label=ammo_table.get(key,'').split(',',3)
        check(len(label)==4 and label[0]==c['name'] and bool(label[2]) and bool(label[3]),key+': native display name/category/description')
        p=MOD/'ammunition'/(key+'.ini');check(p.is_file(),'store file '+key)
        ammo=read_ini(p)
        check(abs(float(ammo['General']['Mass'])-c['mass_kg'])<1e-5,'store mass '+key)
        md=ammo['Models'];path=MOD/md['ResourcesFolder']/md['ResourcesRoot']
        if md['ResourcesFolder'].startswith('assets/'):
            check(path.is_file(),key+': mesh missing')
            v,uv,n,groups=load_obj(path);check(md['ResourcesMesh'] in groups,key+': mesh group')
            check(np.isfinite(v).all() and np.isfinite(n).all(),key+': mesh finite')
            check(all((f[:,:,0]>=0).all() and (f[:,:,0]<len(v)).all() for f in groups.values()),key+': mesh indices')
            mat=read_ini(MOD/md['ResourcesFolder']/md['ResourcesMaterial'])
            for v in mat.get('Textures',{}).values():check((MOD/v).is_file(),key+': texture '+v)
        else:
            check(md['ResourcesFolder'].startswith('weapons/'),key+': undocumented stock asset path')
        if 'SensorSystems' in ammo:
            for i in range(1,int(ammo['SensorSystems']['NumberOfSensorSystems'])+1):
                sn=ammo['SensorSystem'+str(i)]['SystemName']
                check(sn in systems or sn in native_sensors,key+': missing sensor '+sn)
    for uid,spec in manifest.items():
        role=next(r for r in ROLES if uid.startswith('ran_'+r+'-111n'))
        year=spec['edition'];b=BLOCKS[year];d=read_ini(MOD/'aircraft'/(uid+'.ini'));baseline=read_ini(BASE/f'aircraft/ran_{role}-111n.ini')
        check(d['General']['CarrierCapable']=='True',uid+': carrier flag')
        for section in ('General','Models','Submodels','FlightControls','WingSweep','Animations'):
            check(d[section]==baseline[section],uid+': changed original model/landing contract '+section)
        check(d['AI']['Role']==ROLES[role][2],uid+': original role')
        check(int(d['Performance']['EmptyMass'])==spec['empty_mass_kg']==sum(spec['empty_mass_components_kg'].values()),uid+': empty mass budget')
        check(int(d['Performance']['MaxFuel'])==14897,uid+': real internal fuel')
        check(spec['investment_programme']['name']==b['name'],uid+': investment block')
        if role!='rf':
            check(float(d['Performance']['PerEngineMaxThrust'])==b['dry_n'] and float(d['Performance']['PerEngineMaxAfterburnerThrust'])==b['afterburner_n'],uid+': dated propulsion')
        for key,value in baseline['FlightModel'].items():
            factor=b['acceleration'] if key in ('VelocityGain','ThrustGain') else b['controls'] if key in ('PitchGain','HeadingGain','BankGain') else 1
            check(abs(float(d['FlightModel'][key])-float(value)*factor)<1e-6,uid+': native flight response '+key)
        check(spec['nominal_cruise_range_miles']==int(d['Performance']['SpeedAndRange_Cruise'].split(',')[1]),uid+': actual range manifest')
        check(spec['propulsion']['afterburner_thrust_n_per_engine']==int(d['Performance']['PerEngineMaxAfterburnerThrust']),uid+': actual engine manifest')
        squad=read_ini(MOD/'aircraft'/(uid+'_squadrons.ini'))
        for section,v in squad.items():
            if section=='General':continue
            check(v['ServiceDate']=='|'.join(str(x) for x in spec['service_years']),uid+': service gate')
            check((MOD/v['ResourcesLiveryFolder']/v['LiveryTexture']).is_file(),uid+': dated livery')
            if year>=1995:
                tex=f'ran_{role}-111n_{year}_usn_tps.png'
                check(v['LiveryTexture']==tex and v['FueltankTextures'].endswith('/'+tex),uid+': tactical aircraft/tank paint')

        presets=d['WeaponSystems']['AvailableLoadouts'].split(',')
        check(set(presets)==set(spec['loadouts']),uid+': manifest loadouts')
        check(len(presets)==len(set(presets)) and presets[0]=='Default',uid+': unique loadouts/default')
        sensors=[v for s,v in d.items() if re.fullmatch(r'SensorSystem\d+',s)]
        check(len(sensors)==int(d['SensorSystems']['NumberOfSensorSystems']),uid+': sensor count')
        for sn in sensors:check(sn['SystemName'] in native_sensors or sn['SystemName'] in systems,uid+': unknown sensor '+sn['SystemName'])
        ws=[s for s in d if re.fullmatch(r'WeaponSystem\d+',s)]
        check(len(ws)==int(d['WeaponSystems']['NumberOfWeaponSystems']),uid+': weapon count')
        chaff=[d[s] for s in ws if d[s].get('Type')=='Chaff']
        check(len(chaff)==1 and chaff[0].get('SystemName')=='RAN_NW_AIR_CHAFF_DISP',uid+': local zero-reload chaff dispenser')
        for w in ws:
            wd=d[w]
            if wd['Type']!='Hardpoint':continue
            for sn in wd.get('AssociatedSensors','').split(','):check(sn in d,uid+': invalid hardpoint sensor '+sn)
            n=int(wd['NumberOfStations'])
            for i in range(1,n+1):
                check('Station'+str(i) in wd,uid+': missing physical station')
                if 'Station'+str(i)+'Parent' in wd:check(wd['Station'+str(i)+'Parent'] in d['Submodels'].values(),uid+': pylon parent')
            for name in presets:
                for k,v in d.get(w+name,{}).items():
                    if not re.fullmatch(r'Station\d+',k):continue
                    check(int(k[7:])<=n and '*' not in v,uid+': bad station/rack')
                    store,*rack=v.split('|');check(store in catalog,uid+': unknown carried store '+store)
                    if rack:check(rack[0]+'Positions' in wd,uid+': missing rack offsets')
        for name,ld in spec['loadouts'].items():
            stores,by_system=inventory(d,name)
            check(by_system.get('3',{})==ld['auxiliary_external_stores'] if role=='f' else not ld['auxiliary_external_stores'],uid+': auxiliary store inventory '+name)
            ready=d['WeaponSystem1'+name]
            check(float(ready['ReadyUpTime'])==(b['ready_fb'] if role=='fb' else b['ready_other']) and float(ready['CoolDownTime'])==b['cooldown'],uid+': readiness '+name)

            check(stores==ld['stores'],uid+': actual stores '+name)
            for k in stores:check(catalog[k]['earliest_edition']<=year,uid+': future store in '+name+' '+k)
            sm=sum(catalog[k]['mass_kg']*n for k,n in stores.items())
            tf=14897+sum(catalog[k].get('fuel_kg',0)*n for k,n in stores.items())
            gm=544 if role!='ef' else 0
            check(abs(round(sm,1)-ld['stores_mass_kg'])<.01,uid+': store mass '+name)
            check(tf==ld['total_fuel_kg'],uid+': fuel arithmetic '+name)
            check(abs(spec['empty_mass_kg']+sm+tf+gm-ld['full_fuel_takeoff_mass_kg'])<.11,uid+': gross mass '+name)
            check(ld['full_fuel_takeoff_mass_kg']<=51845,uid+': reference gross limit '+name)
            if 'LongRange' in name:check(sum(n for k,n in stores.items() if 'tank_600' in k)>=2,uid+': long-range tanks')
        guns=[d[s] for s in ws if d[s].get('SystemName')=='M61']
        check(len(guns)==(0 if role=='ef' else 1),uid+': M61 role contract')
        if role!='ef':
            gun=guns[0];check(gun['AssociatedMagazine']=='WeaponMagazineM61',uid+': gun magazine')
            check(d['WeaponMagazineM61']['Ammunition1']=='usn_cal_20mm' and int(d['WeaponMagazineM61']['Ammunition1_Count'])==2000,uid+': gun ammunition')
            check(gun['IsMountRotatable']=='False',uid+': fixed forward gun')
        if role=='fb':
            check(d['WeaponSystem3']==baseline['WeaponSystem3'],uid+': preserved internal bay')
            for name,wing_count,bay_count in [('AntiShip',2,0),('AntiShipHeavy',4,3),('AntiShipLongRange',2,3)]:
                w=spec['loadouts'][name]['wing_stores'];bay=spec['loadouts'][name]['internal_bay_stores']
                check(sum(n for k,n in w.items() if 'harpoon' in k)==wing_count,uid+': wing Harpoons '+name)
                check(sum(bay.values())==bay_count and all('harpoon' in k for k in bay),uid+': internal Harpoons '+name)
                if name!='AntiShipHeavy':check(sum(n for k,n in w.items() if 'aim9' in k or 'asraam' in k)==2,uid+': defensive IR missiles '+name)
            own={k for v in spec['loadouts'].values() for k in v['stores'] if k.startswith('ran_nw_')}
            others={k for r in ('f','ef','rf') for v in manifest[unit_id(r,year)]['loadouts'].values() for k in v['stores'] if k.startswith('ran_nw_')}
            # Functional ECM containers have separate names but the same pod,
            # mass and jammer suite. Defensive missile/ARM types must be exact.
            check(others<=own,uid+': all family period weapon types carried')
            check('ReconLongRange' in presets and 'EW' in presets,uid+': family mission stores')
            for name in ('StrikePrecision','StrikePrecisionLongRange','StrikePrecisionLight','StrikePrecisionMedium'):
                check('ran_nw_laserpod' in spec['loadouts'][name]['stores'],uid+': external laser pod '+name)
                check(not spec['loadouts'][name]['internal_bay_stores'],uid+': bay not consumed by precision stores')
            w=d['WeaponSystem1'];pv,_,_,pg=load_obj(MOD/'assets/ran_f111n/models/alq-131/alq-131.obj')
            pod=pv[pg['AN_ALQ_131'][:,:,0]]
            v,_,_,gg=load_obj(MOD/d['Models']['ResourcesFolder']/d['Models']['ResourcesRoot'])
            for st,parent,wing in [(5,'hang2','right_wing'),(6,'hang1','left_wing')]:
                bottom=v[gg[parent][:,:,0],1].min()+float(d[parent]['Position'].split(',')[1])+float(d[wing]['Position'].split(',')[1])
                transform=matrix(w[f'Station{st}'],w[f'Station{st}Rotation'])@matrix(w['ECMPositions'],w['ECMRotations'])
                top=(pod@transform[:3,:3].T+transform[:3,3])[:,:,1].max()
                check(abs(top-bottom)<.0003,uid+': ECM attached to '+parent)
        if role=='rf':
            check(float(d['Performance']['MachLimit'])==3 and d['Performance']['SpeedAndRange_Cruise'].startswith('2.52,'),uid+': Mach 3 and triple cruise retained')
            check(float(d['Performance']['PerEngineMaxAfterburnerThrust'])==round(480000*b['acceleration']),uid+': fictional dated sprint propulsion')
            fighter=read_ini(MOD/'aircraft'/(unit_id('f',year)+'.ini'))
            for key in ('VelocityGain','ThrustGain'):check(abs(float(d['FlightModel'][key])-3*float(fighter['FlightModel'][key]))<1e-6,uid+': triple fighter response '+key)
            check('ReconFast' in presets and not any(n in presets for n in ('Strike','AntiShip','EW')),uid+': reconnaissance role')
            check(any(s['SystemName']==sensor_id('ELINT',year) for s in sensors),uid+': ELINT')
        if role=='ef':
            offensive=[s for s in sensors if systems.get(s['SystemName'],{}).get('Type')=='Offensive']
            check(len(offensive)==2 and {s['Mount'] for s in offensive}=={'hang1','hang2'},uid+': two pylon ECM sensors')
            for name,v in spec['loadouts'].items():check(v['stores'].get(pod_id('ef',1,year))==1 and v['stores'].get(pod_id('ef',2,year))==1,uid+': two physical pods '+name)
        if role=='f':check(not any(n in presets for n in ('Strike','AntiShip','EW')),uid+': fighter role')
    # Original meshes/maps remain intact alongside eight new maps.
    baseline_zip=ROOT/'authoring/V52_ASSET_SHA256.json'
    hashes=json.loads(baseline_zip.read_text())
    for name,digest in hashes.items():check(hashlib.sha256((MOD/name).read_bytes()).hexdigest()==digest,'unchanged aircraft asset '+name)
    texture_report=json.loads((ROOT/'USN_TEXTURE_VALIDATION.json').read_text())
    check(texture_report['status']=='PASS' and len(texture_report['maps'])==8,'eight audited tactical maps')
    protected=protected_pixels()
    for t in texture_report['maps']:
        p=MOD/t['texture'];a=np.asarray(Image.open(p).convert('RGBA'));old=np.asarray(Image.open(MOD/t['source']).convert('RGBA'))
        check(a.shape==(2048,3072,4),'native atlas size '+t['aircraft'])
        check(np.array_equal(a[:,:,3],old[:,:,3]),'native atlas alpha '+t['aircraft'])
        check(np.array_equal(a[protected],old[protected]),'cockpit/mechanical atlas '+t['aircraft'])
        check(hashlib.sha256(p.read_bytes()).hexdigest()==t['sha256'] and np.any(a!=old),'repaint content/hash '+t['aircraft'])
    for role in ROLES:
        values=[read_ini(MOD/'aircraft'/(unit_id(role,y)+'.ini')) for y in YEARS]
        series=[float(v['Performance']['PerEngineMaxAfterburnerThrust']) for v in values];check(all(a<b for a,b in zip(series,series[1:])),role+': increasing engine output')
        series=[float(v['FlightModel']['VelocityGain']) for v in values];check(all(a<b for a,b in zip(series,series[1:])),role+': increasing response')
        series=[float(v['Performance']['SpeedAndRange_Cruise'].split(',')[1]) for v in values];check(all(a<b for a,b in zip(series,series[1:])),role+': increasing range field')
        for kind,key in [('FleetRadar' if role=='f' else 'StrikeRadar','TargetChannels'),('DECM','JamChance'),('FLIR','MaxRangeMultiplier'),('OffensiveECM1','JamChannels')]:
            series=[float(systems[sensor_id(kind,y)][key]) for y in YEARS];check(all(a<b for a,b in zip(series,series[1:])),role+': increasing '+kind+'/'+key)
        a=MOD/'assets/textures/ran_f111n'/f'ran_{role}-111n_1995_usn_tps.png'
        b=MOD/'assets/textures/ran_f111n'/f'ran_{role}-111n_2003_usn_tps.png'
        check(hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(),role+': distinct late-edition materials')
    for line in (ROOT/'MOD_SHA256.txt').read_text().splitlines():
        digest,name=line.split('  ',1);check(hashlib.sha256((MOD/name).read_bytes()).hexdigest()==digest,'checksum '+name)
    result={'status':'FAIL' if failures else 'PASS','checks':checks,'failures':failures,'aircraft':len(manifest),'loadouts':sum(len(x['loadouts']) for x in manifest.values()),'runtime_tested':False,'scope':'Dated weapon selection, increasing native investment, eight tactical atlases, all-rounder union, M61 magazines, exact retained bay/model/landing geometry, mass arithmetic, takeoff reference budget, store and sensor resolution, pod attachment, original assets and checksums'}
    (ROOT/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    return bool(failures)

if __name__=='__main__':sys.exit(main())
