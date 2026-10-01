#!/usr/bin/env python3
"""Build the self-contained RAN F-111N V5.2.1 package from the supplied sources."""
from pathlib import Path
from collections import OrderedDict
import re, shutil, json, os

ROOT = Path(__file__).resolve().parent
SRC = Path(os.environ.get('RAN_F111N_SOURCE_ROOT', str(ROOT / 'sources')))
F = SRC / '3689650533/3689650533'
U = SRC / '3587484531/3587484531'
OUT = ROOT / 'deliverables/RAN-F111N-Naval-Wing-V5.2.1'
MOD = OUT / 'RAN-F111N-Naval-Wing'

def read_ini(path):
    result = OrderedDict(); section = None
    for raw in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line = raw.split('//', 1)[0].strip()
        if not line or line.startswith(('#', ';')): continue
        match = re.match(r'^\[([^]]+)\]', line)
        if match:
            section = match[1]
            result.setdefault(section, OrderedDict())
        elif '=' in line and section:
            key, value = line.split('=', 1)
            result[section][key.strip()] = value.strip()
    return result

def write_ini(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n\n'.join('['+s+']\n'+'\n'.join(k+'='+str(v) for k,v in d.items())
                              for s,d in data.items() if d) + '\n', encoding='utf-8')

def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

def animation_file(is_ew):
    old = read_ini(U / 'animations/animations_usaf_f-111.ini')
    new = OrderedDict()
    actions = ['Canopy_Extend','Canopy_Retract','Gear_Extend','Gear_Retract',
               'Hook_Deploy','Hook_Retrieve','Flaps_Takeoff','Flaps_Takeoff_Retract',
               'Flaps_Landing','Flaps_Landing_Retract']
    if not is_ew: actions += ['Bay_Open','Bay_Close']
    new['Animations'] = {'NumberOfAnimations':len(actions),
                         **{f'Animation{i}':x for i,x in enumerate(actions,1)}}
    for action in actions:
        if action in old:
            new[action] = old[action].copy()
            for k,v in old[action].items():
                if not re.fullmatch(r'Sequence\d+', k): continue
                seq = old[v]
                steps = int(seq['NumberOfSteps']); nd = {'NumberOfSteps':steps}
                for n in range(1,steps+1):
                    pos = ','.join(seq.get(f'Position{a}{n}', a.lower()) or a.lower() for a in 'XYZ')
                    rot = ','.join(seq.get(f'Rotation{a}{n}', a.lower()) or '0' for a in 'XYZ')
                    nd[f'Step{n}'] = f"{seq.get(f'Time{n}', '0')}|{pos}|{rot}|{seq.get(f'Smoothness{n}', 'EaseInOut')}"
                new[v] = nd
    for action, angle1, angle2 in [('Hook_Deploy','0','-45'),('Hook_Retrieve','-45','0')]:
        new[action] = {'NumberOfSequencesToPlay':1,'Sequence1':action+'_Sequence','Sequence1_Model':'hook'}
        new[action+'_Sequence']={'NumberOfSteps':2,'Step1':f'0|x,y,z|{angle1},y,z|EaseInOut',
                                'Step2':f'5|x,y,z|{angle2},y,z|EaseInOut'}
    for action, start, end in [('Flaps_Takeoff',0,15),('Flaps_Takeoff_Retract',15,0),
                              ('Flaps_Landing',0,30),('Flaps_Landing_Retract',30,0)]:
        new[action] = {'NumberOfSequencesToPlay':2}
        for i, side in enumerate(['l','r'],1):
            name = action+'_'+side
            new[action][f'Sequence{i}']=name; new[action][f'Sequence{i}_Model']='flap_'+side
            new[name] = {'NumberOfSteps':2,'Step1':f'0|x,y,z|{start},y,z|EaseInOut',
                         'Step2':f'5|x,y,z|{end},y,z|EaseInOut'}
    return new

VARIANTS = {
 'f': dict(name='F-111N',nickname='WaterPig',role='Fighter',squadrons=[805,808],fuel=10000,mach=2.5,
           cruise=1450,mass=21200,thrust=112000,chaff=64,model='f-111f'),
 'fb':dict(name='FB-111N',nickname='MudPig',role='Bomber',squadrons=[817,850],fuel=10000,mach=2.6,
           cruise=1550,mass=23000,thrust=125000,chaff=96,model='f-111f'),
 'rf':dict(name='RF-111N',nickname='SprintPig',role='Recon,ESM',squadrons=[816,817],fuel=14000,mach=3.0,
           cruise=2300,mass=21500,thrust=145000,chaff=128,model='f-111f'),
 'ef':dict(name='EF-111N',nickname='ScreamPig',role='EW,ESM',squadrons=[723,817],fuel=10000,mach=2.2,
           cruise=1700,mass=22400,thrust=112000,chaff=160,model='ef-111'),
}

def weapon_section(stations, sensor='SensorSystem3'):
    data={'Type':'Hardpoint','SystemName':'Hardpoint','AssociatedSensors':sensor,
          'FiringArcs':'-15,15','NumberOfStations':len(stations),'ModuleType':'Weapon'}
    for n,(pos,parent) in enumerate(stations,1):
        data[f'Station{n}']=pos
        data[f'Station{n}Parent']=parent
        data[f'Station{n}Rotation']='2,0,0'
    data.update(TankPositions='0,-0.003,0', TankRotations='0,0,0',
                AAMPositions='0,0,0', AAMRotations='-2,0,0',
                BombPositions='0,-0.003,0.005',
                MER6Positions='0,-0.0048,-0.0159|0,-0.0048,0.0174|0.0035,-0.0008,-0.0159|0.0035,-0.0008,0.0174|-0.0035,-0.0008,-0.0159|-0.0035,-0.0008,0.0174',
                MER6Rotations='0,0,0|0,0,0|0,0,45|0,0,45|0,0,-45|0,0,-45')
    return data

STATIONS = [('-0.074254,0.002245,0.013277','hang1'),('0.074254,0.002245,0.013277','hang2'),
            ('0.043455,-0.004675,0.015994','hang4'),('-0.043455,-0.004675,0.015994','hang3'),
            ('0.068848,-0.004102,0.008404','hang2'),('-0.068848,-0.004102,0.008404','hang1')]

def build():
    MOD.mkdir(parents=True,exist_ok=True)
    for model in ['f-111f','ef-111']:
        src=U / f'assets/models/vechicle/aircraft/{model}'
        dest=MOD / f'assets/ran_f111n/models/{model}'
        copy_file(src / f'{model}.obj',dest / f'{model}.obj')
        for file in ['hull_nm.png','hull_spec.png']:
            copy_file(src / 'textures' / file, dest / 'textures' / file)
    # Preserve original OBJ topology. A separate tailhook mesh gets a correct hinge.
    obj = (MOD/'assets/ran_f111n/models/f-111f/f-111f.obj').read_text()
    vs=[]; uvs=[]; ns=[]; faces=[]; active=False
    for ln in obj.splitlines():
        t=ln.split()
        if not t: continue
        if t[0]=='v': vs.append([float(x) for x in t[1:4]])
        elif t[0]=='vt': uvs.append(t[1:])
        elif t[0]=='vn': ns.append(t[1:])
        elif t[0]=='o': active=t[1]=='hook'
        elif t[0]=='f' and active: faces.append(t[1:])
    pivot=[0,-0.001626,-0.078958]
    lines=['o ran_tailhook']
    indices=sorted({int(t.split('/')[0]) for f in faces for t in f})
    vi={v:i+1 for i,v in enumerate(indices)}
    for i in indices: lines.append('v '+' '.join(f'{vs[i-1][a]-pivot[a]:.8f}' for a in range(3)))
    texids=sorted({int(t.split('/')[1]) for f in faces for t in f if len(t.split('/'))>1 and t.split('/')[1]})
    normalids=sorted({int(t.split('/')[2]) for f in faces for t in f if len(t.split('/'))>2 and t.split('/')[2]})
    ti={v:i+1 for i,v in enumerate(texids)}; ni={v:i+1 for i,v in enumerate(normalids)}
    lines+=['vt '+' '.join(uvs[i-1]) for i in texids]
    lines+=['vn '+' '.join(ns[i-1]) for i in normalids]
    for face in faces:
        out=[]
        for x in face:
            a=x.split('/'); out.append(f'{vi[int(a[0])]}/{ti[int(a[1])]}/{ni[int(a[2])]}')
        lines.append('f '+' '.join(out))
    (MOD/'assets/ran_f111n/models/f-111f/tailhook.obj').write_text('\n'.join(lines)+'\n')
    podsrc=U/'assets/models/weapon/ammunition/alq-131'
    poddst=MOD/'assets/ran_f111n/models/alq-131'
    copy_file(podsrc/'alq-131.obj',poddst/'alq-131.obj')
    for p in (podsrc/'textures').glob('*.png'): copy_file(p,poddst/'textures'/p.name)
    podmat=read_ini(podsrc/'alq-131_mat.ini')
    for k,v in podmat['Textures'].items(): podmat['Textures'][k]=v.replace('assets/models/weapon/ammunition/alq-131/','assets/ran_f111n/models/alq-131/')
    write_ini(poddst/'ran_alq-131_mat.ini',podmat)
    for n in range(1,5):
        pod=read_ini(U/'ammunition/usaf_alq-131.ini')
        pod['General']['AmmoPoints']='520'
        pod['SensorSystem1']['SystemName']=f'RAN_ALQ99N_{n}'
        pod['Models'].update(ResourcesFolder='assets/ran_f111n/models/alq-131/',ResourcesMaterial='ran_alq-131_mat.ini')
        write_ini(MOD/f'ammunition/ran_alq-131n_{n}.ini',pod)
    old_sensors=read_ini(SRC/'RAN-F111N-Naval-Wing-V4.3-SteamWorkshop(1)/RAN-F111N-Naval-Wing-V4.3-SteamWorkshop/systems/sensors.ini')
    write_ini(MOD/'systems/sensors.ini',old_sensors)
    write_ini(MOD/'animations/animations_ran_f111n.ini',animation_file(False))
    write_ini(MOD/'animations/animations_ran_ef111n.ini',animation_file(True))
    language=OrderedDict(); loadout_names=OrderedDict(); ammo_names=OrderedDict(AmmunitionNames={})
    for n in range(1,5): ammo_names['AmmunitionNames'][f'ran_alq-131n_{n}']=f'RAN ALQ-131N ECM pod {n},,ECM pod {n}'
    manifest={}
    for short,cfg in VARIANTS.items():
        unit='ran_'+short+'-111n'; ew=short=='ef'; bomber=short=='fb'
        src=(U/'aircraft/usaf_ef-111.ini') if ew else (F/'aircraft/raaf_f-111c1985.ini')
        d=read_ini(src)
        d=OrderedDict((s,k) for s,k in d.items() if k and not s.startswith('WeaponSystem') and s not in ['WeaponSystems','SensorSystems'] and not s.startswith('SensorSystem'))
        # Source geometry and source transforms stay together; no stock mesh/animation mixing.
        d['General'].update(CarrierCapable='True',LaunchPointOffset='0.055',OnDeckPositionOffset='0,0,-0.070',
                            LandingPivot='0,-0.035,-0.105',Length='24.6',Pilot='wp_pilot_k1m_a',
                            PilotPositions='0.006,-0.002,0.081|-0.006,-0.002,0.081')
        d['General'].pop('PilotRotation',None)
        d['AI']['Role']=cfg['role']
        for n,side in [(1,'l'),(2,'r')]:
            d['FlightControls'].update({f'Spoileron{n}_Model':'aileron_'+side,
                f'Spoileron{n}_BaseAngle':'0',f'Spoileron{n}_RotationAxis':'X'})
        d['Animations']['AnimationFile_1']='animations_ran_ef111n' if ew else 'animations_ran_f111n'
        d['Engine']['EngineIntakeArea']='0.615'
        d['Performance'].update(WingSpan='19' if ew else '21.4',MaxG='6.5' if ew or bomber else '7.5',
            MaxClimbRate='400',EmptyMass=str(cfg['mass']),MaxFuel=str(cfg['fuel']),
            PerEngineMaxThrust='80000',PerEngineMaxAfterburnerThrust=str(cfg['thrust']),
            Ceiling='68000' if short=='rf' else '60000',CruiseAltitude='37000',
            MachLimit=str(cfg['mach']),MaxSpeedAtSeaLevel='820' if short=='rf' else '780',
            SpeedAndRange_Cruise=f"0.84,{cfg['cruise']}",SpeedAndRange_Afterburner=f"{cfg['mach']},0.2")
        d['WingSweep'].update(NumberOfAngles='3',SweepSpeed3=str(cfg['mach']))
        model=cfg['model']; folder=f'assets/ran_f111n/models/{model}/'; mat=unit+'_mat.ini'
        for s,values in d.items():
            for key in ['ResourcesMaterial','Material','DamageModelMaterial1']:
                if values.get(key) in ['f-111f_mat.ini','ef-111_mat.ini']: values[key]=mat
            if values.get('ResourcesFolder','').startswith('assets/models/vechicle/aircraft/'):
                values['ResourcesFolder']=folder
        for key in list(d['Models']):
            if key.startswith('AssetBundle'): del d['Models'][key]
        d['Models']['ResourcesFolder']=folder
        # Inactive built-in tanks and serial overlays never sit on top of new loadout stores.
        for key,val in list(d['Submodels'].items()):
            if val in ['number','tank1','tank2']: del d['Submodels'][key]
        # The EW model has no bay doors or Pave Tack mesh.
        d['hook'].update(ResourcesMeshFolder='assets/ran_f111n/models/f-111f/',RootMesh='tailhook.obj',
                         Mesh='ran_tailhook',Position='0,-0.001626,-0.078958')
        # Material files use original normal/specular maps plus new RAN diffuse atlases.
        write_ini(MOD/folder/mat,{'Shader':{'Path':'Marmoset/Bumped Specular IBL'},'Textures':{
            '_MainTex':f'assets/textures/ran_f111n/{unit}.png',
            '_SpecTex':folder+'textures/hull_spec.png','_BumpMap':folder+'textures/hull_nm.png'}})
        tank=read_ini(U/'ammunition/usaf_tank_600_f-111.ini')
        for key in list(tank['Models']):
            if key.startswith('AssetBundle'): del tank['Models'][key]
        tankid='ran_tank_600_'+short+'111n'
        tank['Models'].update(ResourcesFolder='assets/ran_f111n/models/f-111f/',ResourcesRoot='f-111f.obj',
                              ResourcesMesh='tank',ResourcesMaterial='ran_tank_'+short+'_mat.ini')
        write_ini(MOD/'assets/ran_f111n/models/f-111f'/('ran_tank_'+short+'_mat.ini'),
                  {'Shader':{'Path':'Marmoset/Bumped Specular IBL'},'Textures':{
                    '_MainTex':f'assets/textures/ran_f111n/{unit}.png',
                    '_SpecTex':'assets/ran_f111n/models/f-111f/textures/hull_spec.png',
                    '_BumpMap':'assets/ran_f111n/models/f-111f/textures/hull_nm.png'}})
        write_ini(MOD/f'ammunition/{tankid}.ini',tank)
        ammo_names['AmmunitionNames'][tankid]='RAN F-111N 600 US gal tank (1800 kg fuel),,600 gal tank'
        sensors=[{'Type':'Visual','SystemName':'Eyes','Mount':'Dummy','ViewArcs':'-150,150|-25,91'},
                 {'Type':'Visual','SystemName':'F-111_IR','Mount':'Dummy'},
                 {'Type':'Radar','SystemName':'AN/AWG-9' if short=='f' else 'AN/APQ-161','Mount':'Dummy'},
                 {'Type':'ESM','SystemName':'AircraftRWR','Mount':'Dummy'},
                 {'Type':'ECM','SystemName':'AircraftDECM_Late','Mount':'Dummy'},
                 {'Type':'Radar','SystemName':'AN/AWG-9_Phoenix','Mount':'Dummy'} if short=='f'
                  else {'Type':'LaserDesignator','SystemName':'AN/AVQ-26','Mount':'Dummy'}]
        # Use a stock infrared sensor name, avoiding the source mod's unbundled F-111_IR override.
        sensors[1]={'Type':'Infrared','SystemName':'2nd_Gen_FLIR','Mount':'Dummy','ViewArcs':'-130,130|-160,15'}
        d['SensorSystems']={'NumberOfSensorSystems':len(sensors)}
        for i,s in enumerate(sensors,1): d[f'SensorSystem{i}']={**s,'ModuleType':'Sensor'}
        stations=STATIONS.copy()
        if ew:
            stations[4]=('0.064448,-0.011602,0.008404','hang2')
            stations[5]=('-0.064448,-0.011602,0.008404','hang1')
            stations += [('0.073248,-0.011602,0.008404','hang2'),('-0.073248,-0.011602,0.008404','hang1')]
        d['WeaponSystem1']=weapon_section(stations,'SensorSystem3')
        d['WeaponSystem2']={'Type':'Chaff','SystemName':'WP_AIR_CHAFF_DISP','Mount':'Dummy',
            'AssociatedMagazine':'WeaponMagazineChaff','NumberOfEffects':'4','DelayBetweenLaunches':'0.1',
            'WorksStandalone':'True','ModuleType':'Weapon'}
        if short=='f':
            # Phoenix uses the dedicated guidance mode, as on the current F-14A.
            d['WeaponSystem3']=weapon_section(STATIONS[4:6],'SensorSystem6')
        aa={1:'usn_aim-9l|AAM',2:'usn_aim-9l|AAM'}
        tanks={3:tankid+'|Tank',4:tankid+'|Tank'}
        presets=OrderedDict()
        if short=='f':
            default={**aa,3:'usn_aim-7m|AAM',4:'usn_aim-7m|AAM',5:'usn_aim-9l|AAM',6:'usn_aim-9l|AAM'}
            presets['Default']=(default,{})
            presets['AirToAir']=(default,{})
            presets['AirToAirLongRange']=({**aa,**tanks},{1:'usn_aim-54a|AAM',2:'usn_aim-54a|AAM'})
        elif bomber:
            presets['Default']=(aa,{})
            presets['AirToAir']=(aa,{})
            presets['AirToAirLongRange']=({**aa,**tanks},{})
            presets['Strike']=({**aa,**{i:'usn_mk-82|MER6' for i in range(3,7)}},{})
            presets['StrikeLongRange']=({**aa,**tanks,5:'usn_mk-82|MER6',6:'usn_mk-82|MER6'},{})
            presets['StrikeHeavy']=({**aa,**{i:'usn_mk-84|Bomb' for i in range(3,7)}},{})
            presets['StrikeHeavyLongRange']=({**aa,**tanks,5:'usn_mk-84|Bomb',6:'usn_mk-84|Bomb'},{})
            presets['StrikePrecision']=({**aa,**{i:'usn_gbu-10|Bomb' for i in range(3,7)}},{})
            presets['StrikePrecisionLongRange']=({**aa,**tanks,5:'usn_gbu-10|Bomb',6:'usn_gbu-10|Bomb'},{})
        elif short=='rf':
            recon={**aa,**{i:tankid+'|Tank' for i in range(3,7)}}
            for name in ['Default','AirToAir','AirToAirLongRange','Recon','ReconLongRange']: presets[name]=(recon,{})
        else:
            suite={**aa,**tanks,5:'ran_alq-131n_1',6:'ran_alq-131n_2',7:'ran_alq-131n_3',8:'ran_alq-131n_4'}
            for name in ['Default','AirToAir','AirToAirLongRange','EW','EWLongRange']: presets[name]=(suite,{})
        d['WeaponSystems']={'NumberOfWeaponSystems':3 if short=='f' else 2,'AvailableLoadouts':','.join(presets)}
        stats={}
        for name,(stores,phoenix) in presets.items():
            hide=['tank1','tank2']
            racks=['MER_Outer_Right','MER_Outer_Left','MER_Inner_Left','MER_Inner_Right']
            if not ew:
                if name=='Strike': pass
                elif name=='StrikeLongRange': hide+=['MER_Inner_Left','MER_Inner_Right']
                else: hide+=racks
            ld={'SubModelsToHide':','.join(hide),'ReadyUpTime':30 if bomber else 20,'CoolDownTime':60}
            ld.update({f'Station{k}':v for k,v in stores.items()})
            ld['LevelAttack']='GuidedBombs,Missiles' if 'Precision' in name else ('DumbBombs,Missiles' if name.startswith('Strike') else 'Missiles')
            d['WeaponSystem1'+name]=ld
            if short=='f':
                d['WeaponSystem3'+name]={'LevelAttack':'Missiles',**{f'Station{k}':v for k,v in phoenix.items()}}
            counts={}
            for v in list(stores.values())+list(phoenix.values()):
                ident=v.split('|')[0]; amt=1
                if '|' in v:
                    rack=v.split('|')[1]
                    amt=len(d['WeaponSystem1'].get(rack+'Positions','0,0,0').split('|'))
                counts[ident]=counts.get(ident,0)+amt
            stats[name]=dict(stores=counts,total_fuel_kg=cfg['fuel']+counts.get(tankid,0)*1800)
        d['WeaponMagazineChaff']['Ammunition1_Count']=str(cfg['chaff'])
        write_ini(MOD/f'aircraft/{unit}.ini',d)
        sq=OrderedDict(General={'NumberOfSquadrons':2})
        for name in ['Default','Squadron1','Squadron2']:
            sq[name]={'ResourcesLiveryFolder':'assets/textures/ran_f111n/','LiveryTexture':unit+'.png',
                      'FueltankTextures':tankid+',assets/textures/ran_f111n/'+unit+'.png',
                      'Nation':'Australia','ServiceDate':'1985|2050'}
        write_ini(MOD/f'aircraft/{unit}_squadrons.ini',sq)
        text={'f':'Heavy naval fighter with an F-14-derived radar and missile integration. Default is four Sidewinders and two Sparrows; long-range CAP trades two wing missiles for two 600-gallon tanks and uses two Phoenix missiles.',
              'fb':'Reinforced fast bomber. Bombing is its primary role; two Sidewinders provide self-defence. Default is defensive air-to-air only. Dedicated conventional and precision bombing presets include real external tanks on every long-range option.',
              'rf':'High-speed fleet reconnaissance aircraft with increased internal fuel. Carries only two Sidewinders and four 600-gallon tanks. Mach 3 is a fictional high-altitude clean-airframe design limit; store drag and fuel consumption affect achievable performance.',
              'ef':'Fleet electronic-attack aircraft based on the source EF-111A model. Every operational preset carries exactly two Sidewinders, two 600-gallon tanks and four separately defined offensive ECM pods.'}[short]
        language[unit]={'Type':'Bomber' if bomber else ('Fighter' if short=='f' else 'Recon' if short=='rf' else 'EW'),
            'Default':cfg['name']+' '+cfg['nickname']+','+cfg['name'],
            'DefaultDescription':'Fictional RAN-RAAF naval aviation programme. '+text+' RAN operates the ships and carrier support; the RAAF supplies the specialist airpower and training. Squadron references are heritage tributes.',
            'Squadron1':f"{cfg['name']} {cfg['nickname']} - {cfg['squadrons'][0]} Squadron heritage,{cfg['squadrons'][0]} Sqn",
            'Squadron2':f"{cfg['name']} {cfg['nickname']} - {cfg['squadrons'][1]} Squadron heritage,{cfg['squadrons'][1]} Sqn",
            'Callsigns':'Squadron1,Pig,Boar,Tusk|Squadron2,Razor,Grunt,Hog'}
        loadout_names[unit]={name:(f'Default - {"Defensive AAM only" if bomber else "Fleet defence" if short=="f" else "Recon + 4 tanks" if short=="rf" else "Electronic attack"}' if name=='Default' else {
            'AirToAir':'Air-to-air','AirToAirLongRange':'Air-to-air long range - external tanks',
            'Strike':'Bombing - 24 Mk 82 + 2 AAM','StrikeLongRange':'Bombing long range - 12 Mk 82 + 2 AAM + 2 tanks',
            'StrikeHeavy':'Heavy bombing - 4 Mk 84 + 2 AAM','StrikeHeavyLongRange':'Heavy bombing long range - 2 Mk 84 + 2 AAM + 2 tanks',
            'StrikePrecision':'Precision bombing - 4 GBU-10 + 2 AAM','StrikePrecisionLongRange':'Precision bombing long range - 2 GBU-10 + 2 AAM + 2 tanks',
            'Recon':'Reconnaissance - 2 AAM + 4 tanks','ReconLongRange':'Recon long range - 2 AAM + 4 tanks',
            'EW':'Electronic attack - 2 AAM + 2 tanks + 2 ECM','EWLongRange':'Electronic attack long range - 2 AAM + 2 tanks + 2 ECM'}[name]) for name in presets}
        manifest[unit]={**cfg,'loadouts':stats,'texture':unit+'.png','source_definition':str(src.relative_to(ROOT))}
    write_ini(MOD/'language_en/aircraft_names.ini',language)
    # The game reads a global LoadoutNames section, not per-aircraft sections.
    # Keep built-in labels intact and define only the additional preset names.
    write_ini(MOD/'language_en/loadout_names.ini',{'LoadoutNames':{
        'StrikeHeavyLongRange':'Heavy bombing long range',
        'StrikePrecisionLongRange':'Precision bombing long range',
        'ReconLongRange':'Reconnaissance long range',
        'EWLongRange':'Electronic warfare long range'}})
    write_ini(MOD/'language_en/ammunition_names.ini',ammo_names)
    write_ini(MOD/'_info.ini',{'Language_en':{'Name':'RAN F-111N Naval Wing V5','Description':'WaterPig fighter, MudPig bomber, SprintPig reconnaissance, ScreamPig electronic attack. Source-matched models, isolated animations, real fuel tanks and RAN liveries.'},'Compatibility':{'ApproximateVersion':'0.8.0'}})
    (OUT/'loadout_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    from mudpig_maritime import apply_package
    apply_package(OUT)
    from revisions_v52 import apply_package as apply_v52
    apply_v52(OUT)
    print('Built',MOD)

if __name__=='__main__': build()
