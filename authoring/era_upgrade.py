#!/usr/bin/env python3
"""Rebuild the four dated Naval Wing families from preserved V5.2.1 INIs.

Aircraft geometry, liveries, landing settings and the three-place MudPig bay
come from baseline/. Weapon definitions use the native Sea Power schema.
Naval engineering allowances and new-weapon simulation approximations are
recorded separately from historical reference values.
"""
from pathlib import Path
from collections import OrderedDict, Counter
from copy import deepcopy
import re, json, math, hashlib, shutil
from investment_programme import BLOCKS,mass_allowances,build_systems,apply as apply_investment,describe as describe_investment

ROOT=Path(__file__).resolve().parent.parent
MOD=ROOT/'RAN-F111N-Naval-Wing'
BASE=ROOT/'authoring/baseline'
NATIVE=ROOT/'authoring/native'
YEARS=(1980,1985,1995,2003)
LIMIT=51845
FUEL=14897
TANK_FUEL=1770
TANK_DRY=150  # engineering allowance; not a measured F-111 tank mass
GUN_ROUNDS=2000
GUN_ROUND_MASS=.272
NAVAL_ALLOWANCE=950
GUN_INSTALLATION=650  # complete separate gun, feed, mount and housing allowance

def read_ini(path):
    data=OrderedDict();section=None
    for raw in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line=raw.split('//',1)[0].strip()
        if not line or line.startswith(('#',';')):continue
        m=re.match(r'^\[([^]]+)\]',line)
        if m:section=m[1];data.setdefault(section,OrderedDict())
        elif section and '=' in line:
            key,value=line.split('=',1);data[section][key.strip()]=value.strip()
    return data

def write_ini(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('\n\n'.join('['+s+']\n'+'\n'.join(k+'='+str(v) for k,v in d.items()) for s,d in data.items() if d)+'\n')

def unit_id(role,year):
    # Keep the original four IDs usable in saved missions as the 1980 edition.
    return 'ran_'+role+'-111n'+('' if year==1980 else '_'+str(year))

ROLES={
 'f':('F-111N','WaterPig','Fighter',[805,808]),
 'fb':('FB-111N','MudPig','Bomber',[817,850]),
 'rf':('RF-111N','SprintPig','Recon,ESM',[816,817]),
 'ef':('EF-111N','ScreamPig','EW,ESM',[723,817])}

# key, display name, native donor, carried mass kg, earliest permitted edition.
# Conservative edition floors deliberately omit late introductions from earlier
# editions even when test or initial production examples existed.
SPECS=[
 ('aim9l','AIM-9L Sidewinder','usn_aim-9l',86,1980),
 ('aim9m','AIM-9M Sidewinder','usn_aim-9m',86,1985),
 ('aim7f','AIM-7F Sparrow','usn_aim-7f',231,1980),
 ('aim7m','AIM-7M Sparrow','usn_aim-7m',231,1985),
 ('aim54a','AIM-54A Phoenix','usn_aim-54a',443,1980),
 ('aim54c','AIM-54C Phoenix','usn_aim-54a',463,1985),
 ('aim120b','AIM-120B AMRAAM','usn_aim-54a',152,1995),
 ('aim120c5','AIM-120C-5 AMRAAM','usn_aim-54a',152,2003),
 ('asraam','ASRAAM','usn_aim-9m',88,2003),
 ('harpoona','AGM-84A Harpoon','usn_agm-84a',526,1980),
 ('harpoonc','AGM-84C Harpoon','usn_agm-84c',526,1985),
 ('harpoond','AGM-84D Harpoon Block 1C','usn_agm-84d',526,1995),
 ('harpoonl','AGM-84L Harpoon Block II','usn_agm-84d',526,2003),
 ('maverickb','AGM-65B Maverick','usn_agm-65b',208,1980),
 ('maverickd','AGM-65D Maverick','usn_agm-65b',218,1985),
 ('maverickg','AGM-65G Maverick','usn_agm-65b',302,1995),
 ('standardarm','AGM-78 Standard ARM','usn_agm-78',620,1980),
 ('shrike','AGM-45 Shrike','usn_agm-45',178,1980),
 ('harma','AGM-88A HARM','usn_agm-88a',361,1985),
 ('harmc','AGM-88C HARM','usn_agm-88a',361,1995),
 ('mk82','Mk 82 500-lb GP bomb','usn_mk-82',227,1980),
 ('mk83','Mk 83 1000-lb GP bomb','usn_mk-83',454,1980),
 ('mk84','Mk 84 2000-lb GP bomb','usn_mk-84',907,1980),
 ('gbu10','GBU-10 Paveway II','usn_gbu-10',934,1980),
 ('gbu12','GBU-12 Paveway II','usn_gbu-12',277,1980),
 ('gbu16','GBU-16 Paveway II','usn_gbu-16',495,1980),
 ('gbu15','GBU-15 electro-optical glide bomb','usaf_gbu-15',1130,1985),
 ('gbu24','GBU-24 Paveway III','usn_gbu-24',1084,1985),
 ('popeye','AGM-142 Popeye / Have Nap','usn_agm-65b',1360,1995),
 ('slam','AGM-84E SLAM','usn_agm-65b',628,1995),
 ('slamer','AGM-84K SLAM-ER','usn_agm-65b',675,2003),
 ('gbu31','GBU-31 JDAM Mk 84','usn_mk-84',925,2003),
 ('gbu32','GBU-32 JDAM Mk 83','usn_mk-83',461,2003),
 ('jsowa','AGM-154A JSOW','usn_mk-84',483,2003)]
CATALOG={}

def aid(key):return 'ran_nw_'+key

def missile_mesh(key,length,diameter,span,style='missile'):
    """Simple dimensional OBJ; original code geometry, no borrowed modern mesh.

    Weapons point along +Z. The supplied F-111 geometry uses 0.01 units/metre.
    Fins are double-sided triangles; body normals are generated explicitly.
    """
    folder=MOD/'assets/ran_f111n/models/era_weapons';folder.mkdir(parents=True,exist_ok=True)
    vs=[];fs=[]
    def face(pts):
        idx=[]
        for p in pts:vs.append(tuple(float(x)*.01 for x in p));idx.append(len(vs))
        for i in range(1,len(idx)-1):fs.append((idx[0],idx[i],idx[i+1]))
    r=diameter/2;z0=-length/2;z1=length/2
    rings=[(z0,r*.65),(z0+length*.07,r),(z1-length*.22,r),(z1,r*.03)]
    sides=24
    for (za,ra),(zb,rb) in zip(rings,rings[1:]):
        for i in range(sides):
            a=2*math.pi*i/sides;b=2*math.pi*(i+1)/sides
            face([(ra*math.cos(a),ra*math.sin(a),za),(ra*math.cos(b),ra*math.sin(b),za),(rb*math.cos(b),rb*math.sin(b),zb),(rb*math.cos(a),rb*math.sin(a),zb)])
    for angle in [math.pi/4+i*math.pi/2 for i in range(4)]:
        ax,ay=math.cos(angle),math.sin(angle)
        pts=[(r*ax,r*ay,z0+length*.05),(span/2*ax,span/2*ay,z0+length*.04),(span/2*ax,span/2*ay,z0+length*.20),(r*ax,r*ay,z0+length*.32)]
        face(pts);face(pts[::-1])
        if style!='asraam':
            pts=[(r*ax,r*ay,z0+length*.52),(span*.38*ax,span*.38*ay,z0+length*.40),(r*ax,r*ay,z0+length*.33)]
            face(pts);face(pts[::-1])
    lines=['o '+key]+['v '+' '.join(f'{x:.8f}' for x in v) for v in vs]
    # Constant UVs sample the existing light weapon paint; normals keep the
    # faceted dimensional models independent of undocumented importer features.
    lines+=['vt 0.5 0.5']
    normals=[]
    for f in fs:
        a,b,c=[vs[i-1] for i in f]
        u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        norm=math.sqrt(sum(x*x for x in n)) or 1;normals.append([x/norm for x in n])
    lines+=['vn '+' '.join(f'{x:.6f}' for x in n) for n in normals]
    lines+=['f '+' '.join(f'{i}/1/{j}' for i in f) for j,f in enumerate(fs,1)]
    (folder/(key+'.obj')).write_text('\n'.join(lines)+'\n')
    return dict(ResourcesFolder='assets/ran_f111n/models/era_weapons/',ResourcesRoot=key+'.obj',ResourcesMesh=key,ResourcesMaterial='era_weapon_mat.ini')

def build_weapons():
    names=read_ini(BASE/'language_en/ammunition_names.ini')
    donor_mats=MOD/'assets/ran_f111n/models/era_weapons'
    donor_mats.mkdir(parents=True,exist_ok=True)
    write_ini(donor_mats/'era_weapon_mat.ini',{'Shader':{'Path':'Marmoset/Bumped Specular IBL'},'Textures':{
      '_MainTex':'assets/ran_f111n/models/alq-131/textures/alq-131_tex.png',
      '_SpecTex':'assets/ran_f111n/models/alq-131/textures/alq-131_spec.png',
      '_BumpMap':'assets/ran_f111n/models/alq-131/textures/alq-131_nm.png'}})
    for key,label,donor,mass,floor in SPECS:
        d=read_ini(NATIVE/'ammunition'/(donor+'.ini'));g=d.setdefault('Guidance',{})
        d['General']['Mass']=str(mass)
        d['General']['AirLaunched']='True'
        d['General']['AmmoPoints']=str(int(mass*(4 if d['General']['Type']=='Missile' else 2)))
        model_note='Native geometry'
        sim_note='Native guidance; rounded historical carried mass'
        if key in ('aim120b','aim120c5'):
            d['Models']=missile_mesh(key,3.66,.178,.526 if key=='aim120b' else .447)
            g.update(GuidanceType='3',MidCourseCorrection='0',MaxLaunchRange='40' if key=='aim120b' else '55',MinLaunchRange='1',MaxVelocity='2500',MaxTurnRate='35',SeekerActiveRange='12',SeekerPassiveRange='12',TerminalApproachDist='12',AntiCountermeasuresBonus='.4',AntiJammerBonus='.3')
            for k in ('SemiActivePhaseMaxDuration','SemiActivePhaseDist','RequiresIllumination'):g.pop(k,None)
            d['WarheadData'].update(Power='4',ImpactSize='Small')
            d['col_main']['Scale']='0.003,0.003,0.0366'
            model_note='Original simplified dimensional AMRAAM mesh'
            sim_note='Active radar homing; no simulated launch-platform midcourse datalink; engagement range is a game estimate, not a published missile limit'
        if key=='aim120c5':
            g.update(AntiCountermeasuresBonus='.55',AntiJammerBonus='.45')
            sim_note+='; C-5 ECCM is an estimated improvement over B'
        if key=='aim54c':
            g.update(AntiCountermeasuresBonus='.35',AntiJammerBonus='.3')
            sim_note='Native AIM-54A geometry and flight profile with C mass and estimated improved ECCM'
        if key=='asraam':
            d['Models']=missile_mesh(key,2.9,.166,.45,'asraam')
            g.update(MaxLaunchRange='15',SeekerPassiveRange='15',MaxTurnRate='50',AntiCountermeasuresBonus='.45',MaxVelocity='2100')
            d['col_main']['Scale']='0.003,0.003,0.029'
            model_note='Original simplified dimensional ASRAAM mesh'
            sim_note='Native IR homing approximation; no helmet sight or lock-on-after-launch simulation'
        if key.startswith('harpoon'):
            g['MaxLaunchRange']='50' if key=='harpoona' else '65' if key=='harpoonc' else '67'
            if key=='harpoonl':
                g.update(AntiCountermeasuresBonus='.35',AntiJammerBonus='.25')
                sim_note='Block II acquisition/integration assumed. Native radar-homing ship attack only; GPS route planning and coastal land-attack mode are not simulated'
        if key in ('maverickd','maverickg'):
            g['GuidanceType']='1'
            if key=='maverickg':d['WarheadData']['Power']='25'
            sim_note='Native Maverick geometry with IIR homing and selected variant mass'
        if key=='harmc':
            g.update(AntiCountermeasuresBonus='.35',TargetMemory='True')
            sim_note='Native HARM-A geometry/flight model with estimated C seeker resilience'
        if key in ('popeye','slam','slamer'):
            length,diameter,span,rng=(4.82,.533,1.98,43) if key=='popeye' else (4.38,.343,.914,60) if key=='slam' else (4.4,.343,2.2,150)
            d['Models']=missile_mesh(key,length,diameter,span)
            g.update(GuidanceType='1' if key=='popeye' else '6',MidCourseCorrection='0',MaxLaunchRange=str(rng),MinLaunchRange='3',SeekerPassiveRange=str(rng),MaxVelocity='540',MaxTurnRate='12',TargetMemory='True',SelfDestructAfterTargetGone='False')
            d['WarheadData'].update(Power='65' if key=='popeye' else '45',ImpactSize='Large',Penetration='Heavy')
            d['col_main']['Scale']=f'{diameter*.01},{diameter*.01},{length*.01}'
            model_note='Original simplified dimensional '+label+' mesh'
            sim_note='Native EO/IIR homing approximation. Control pod is carried and weighted; manual man-in-the-loop control and in-flight retargeting are not simulated'
        if key in ('gbu31','gbu32','jsowa'):
            length,diam,span=(3.879,.457,.635) if key=='gbu31' else (3.035,.356,.498) if key=='gbu32' else (4.06,.33,2.69)
            d['Models']=missile_mesh(key,length,diam,span,'bomb')
            g.update(GuidanceType='0',CircularErrorRadius='13',TargetMemory='True',MinLaunchRange='.5',MaxLaunchRange='13' if key!='jsowa' else '40',GravityFactor='1' if key!='jsowa' else '.5',MinLaunchAltitude='500',MaxLaunchAltitude='45000',SelfDestructAfterTargetGone='False')
            d['col_main']['Scale']=f'{diam*.01},{diam*.01},{length*.01}'
            if key=='jsowa':d['WarheadData'].update(WarheadType='4',Power='45')
            model_note='Original simplified dimensional '+label+' mesh'
            sim_note='Native unguided/CEP approximation for fixed-coordinate INS/GPS attack; no GPS guidance type exists in the supplied schema. JSOW uses reduced gravity as a glide approximation'
        write_ini(MOD/'ammunition'/(aid(key)+'.ini'),d)
        names[aid(key)]={'Default':label+','+label,'DefaultDescription':label+' for the fictional Naval Wing programme.'}
        CATALOG[aid(key)]={'name':label,'mass_kg':mass,'earliest_edition':floor,'native_donor':donor,'model':model_note,'simulation':sim_note}
    # 600 US gallons at SG .78: 1,770 kg fuel, separate estimated dry shell.
    for role in ROLES:
        tank='ran_tank_600_'+role+'111n';d=read_ini(MOD/'ammunition'/(tank+'.ini'))
        d['General'].update(Fuel=str(TANK_FUEL),Mass=str(TANK_DRY))
        write_ini(MOD/'ammunition'/(tank+'.ini'),d)
        CATALOG[tank]={'name':'600 US-gallon fuel tank','mass_kg':TANK_DRY,'fuel_kg':TANK_FUEL,'earliest_edition':1980,'simulation':'Fuel from flight-manual capacity table; dry shell mass is an engineering allowance'}
    # Pods remain ALQ-131 geometry, used to represent the user's naval ECM suite.
    for n in (1,2):
        name='ran_alq-131n_'+str(n);d=read_ini(MOD/'ammunition'/(name+'.ini'))
        d['General']['Mass']='260';write_ini(MOD/'ammunition'/(name+'.ini'),d)
        CATALOG[name]={'name':'Naval offensive ECM pod '+str(n),'mass_kg':260,'earliest_edition':1980,'simulation':'Existing fictional naval ECM in ALQ-131 geometry; not an exact historical ALQ-99 installation'}
        # MudPig carries its offensive sensors in the removable containers, so
        # non-EW presets do not have permanently active offensive jammers.
        fb=deepcopy(d);fb['SensorSystems']={'NumberOfSensorSystems':'1'}
        fb['SensorSystem1']={'Type':'ECM','SystemName':'RAN_ALQ99N_'+str(n),'Mount':'Dummy','ModuleType':'Sensor'}
        fn='ran_nw_ecmpod_'+str(n);write_ini(MOD/'ammunition'/(fn+'.ini'),fb)
        CATALOG[fn]={**CATALOG[name],'name':'MudPig removable offensive ECM pod '+str(n)}
        names[fn]={'Default':'Naval offensive ECM pod,Naval ECM','DefaultDescription':'Removable offensive ECM container.'}
    # Control pods are visible stores and their masses are counted.
    for name,mass,label in [('ran_nw_datalink',260,'EO weapon control pod'),('ran_nw_laserpod',150,'External laser designation pod')]:
        d=read_ini(MOD/'ammunition/ran_alq-131n_1.ini');d['General']['Mass']=str(mass)
        d['SensorSystems']={'NumberOfSensorSystems':'1'}
        d['SensorSystem1']={'Type':'Radar' if 'datalink' in name else 'LaserDesignator','SystemName':'GuidancePodNoAlignment' if 'datalink' in name else 'AN/AVQ-26','Mount':'Dummy','ModuleType':'Sensor'}
        write_ini(MOD/'ammunition'/(name+'.ini'),d)
        CATALOG[name]={'name':label,'mass_kg':mass,'earliest_edition':1985 if 'datalink' in name else 1980,'simulation':'Estimated pod mass with existing pod geometry and native sensor; full historical pod shape is not reproduced'}
        names[name]={'Default':label+','+label,'DefaultDescription':label+' for the fictional Naval Wing.'}
    # Six-bomb rack ammunition carries its proportional 100 kg rack allowance.
    rack=read_ini(MOD/'ammunition/ran_nw_mk82.ini')
    rack['General']['Mass']=str(227+100/6)
    write_ini(MOD/'ammunition/ran_nw_mk82_mer.ini',rack)
    CATALOG['ran_nw_mk82_mer']={'name':'Mk 82 on six-bomb rack','mass_kg':227+100/6,'earliest_edition':1980,'simulation':'227 kg nominal bomb plus one-sixth of an estimated 100 kg detachable MER; no separate unsupported hardpoint mass key'}
    names['ran_nw_mk82_mer']={'Default':'Mk 82 GP bomb,Mk 82','DefaultDescription':'Mk 82; mass includes its share of a six-bomb rack.'}
    write_ini(MOD/'language_en/ammunition_names.ini',names)

PERIOD={
 1980:dict(ir='aim9l',bvr='aim7f',phoenix='aim54a',ship='harpoona',arm='standardarm',mav='maverickb'),
 1985:dict(ir='aim9m',bvr='aim7m',phoenix='aim54c',ship='harpoonc',arm='harma',mav='maverickd'),
 1995:dict(ir='aim9m',bvr='aim120b',phoenix='aim54c',ship='harpoond',arm='harmc',mav='maverickg'),
 2003:dict(ir='asraam',bvr='aim120c5',phoenix='aim54c',ship='harpoonl',arm='harmc',mav='maverickg')}

def remove_loadouts(d):
    for section in list(d):
        if re.fullmatch(r'WeaponSystem\d+\D.*',section):del d[section]

def inventory(d,loadout):
    whole=Counter();systems={}
    for i in range(1,int(d['WeaponSystems']['NumberOfWeaponSystems'])+1):
        w=d['WeaponSystem'+str(i)]
        if w['Type']!='Hardpoint':continue
        c=Counter()
        for k,v in d.get('WeaponSystem'+str(i)+loadout,{}).items():
            if not re.fullmatch(r'Station\d+',k):continue
            a,*rack=v.split('|');n=len(w[rack[0]+'Positions'].split('|')) if rack else 1
            c[a]+=n
        systems[str(i)]=dict(c);whole.update(c)
    return dict(whole),systems

def add_gun(d):
    n=int(d['WeaponSystems']['NumberOfWeaponSystems'])+1
    d['WeaponSystems']['NumberOfWeaponSystems']=str(n)
    d['WeaponSystem'+str(n)]={
        'Type':'CIWS','SystemName':'M61','Mount':'Dummy',
        'MountPosition':'0.012,-0.007,0.078','IsMountRotatable':'False',
        'ContainerBase':'Dummy','Gun':'Dummy','AreContainersRotatable':'False',
        'FiringArcs':'-1,1','ElevationArc':'-1,1',
        'AssociatedMagazine':'WeaponMagazineM61','IsOffensive':'True','ModuleType':'Weapon'}
    d['WeaponMagazineM61']={'NumberOfAmmunitionTypes':'1','Ammunition1_Count':str(GUN_ROUNDS),'Ammunition1':'usn_cal_20mm','ModuleType':'WeaponMagazine'}

def mass_budget(role,year):
    # Source baseline is basic F-111C, not fictional published N-family weights.
    # Recon and fleet radar allowance includes removal/replacement of strike
    # equipment. EF includes the Raven's approximately four-ton integrated suite.
    components={'historical_F111C_basic_reference':23300,'naval_conversion_estimate':NAVAL_ALLOWANCE,
      'role_equipment_estimate':{'f':350,'fb':0,'rf':450,'ef':4000}[role],
      'separate_M61_installation_estimate':GUN_INSTALLATION if role!='ef' else 0,
      'edition_avionics_growth_estimate':{1980:0,1985:100,1995:250,2003:400}[year]}
    components.update(mass_allowances(role,year))
    return components,sum(components.values())

def build_aircraft():
    names=OrderedDict();lds=read_ini(BASE/'language_en/loadout_names.ini');ldnames=lds.setdefault('LoadoutNames',{})
    manifest={}
    for role,(model,nickname,ai,squadrons) in ROLES.items():
      for yi,year in enumerate(YEARS):
        uid=unit_id(role,year);d=read_ini(BASE/f'aircraft/ran_{role}-111n.ini');remove_loadouts(d)
        period=PERIOD[year];ir=aid(period['ir']);bvr=aid(period['bvr']);phoenix=aid(period['phoenix']);ship=aid(period['ship']);arm=aid(period['arm']);mav=aid(period['mav'])
        tank='ran_tank_600_'+role+'111n';wing=d['WeaponSystem1'];components,mass=mass_budget(role,year)
        d['AI']['Role']=ai;d['Performance'].update(EmptyMass=str(mass),MaxFuel=str(FUEL))
        # Keep RF's requested fictional propulsion/speed. Other engines start with the
        # TF30 reference before the dated programme applies hypothetical retrofits.
        if role!='rf':d['Performance'].update(PerEngineMaxThrust='43600',PerEngineMaxAfterburnerThrust='82300')
        d['SensorSystem5']['SystemName']='AircraftDECM_Med' if year<1995 else 'AircraftDECM_Late'
        for section in list(d):
            if re.fullmatch(r'SensorSystem\d+',section) and d[section].get('Type')=='LaserDesignator':
                # A removable external pod allows laser bombing without taking
                # any space from the unchanged internal three-missile bay.
                del d[section]
        # Renumber sensors and fix existing references after the removed laser.
        sns=[(s,v) for s,v in d.items() if re.fullmatch(r'SensorSystem\d+',s)]
        ren={s:'SensorSystem'+str(i) for i,(s,v) in enumerate(sns,1)}
        for s,v in sns:del d[s]
        for s,v in sns:d[ren[s]]=v
        for w in d.values():
            if 'AssociatedSensors' in w:w['AssociatedSensors']=','.join(ren.get(s,s) for s in w['AssociatedSensors'].split(','))
        d['SensorSystems']['NumberOfSensorSystems']=str(len(sns))
        if role in ('rf','fb'):
            n=int(d['SensorSystems']['NumberOfSensorSystems'])+1
            d['SensorSystem'+str(n)]={'Type':'ESM','SystemName':'AircraftELINT','Mount':'Dummy','ModuleType':'Sensor'}
            d['SensorSystems']['NumberOfSensorSystems']=str(n)
        hidden='tank1,tank2,MER_Outer_Right,MER_Outer_Left,MER_Inner_Left,MER_Inner_Right'
        if role!='ef':hidden+=',pave,pave_body'
        presets=[]
        def load(name,stores=None,secondary=None,label=None,mode='Missiles',mer=False):
            presets.append(name);w={'SubModelsToHide':hidden,'ReadyUpTime':'30' if role=='fb' else '20','CoolDownTime':'60','LevelAttack':mode}
            if mer:w['SubModelsToHide']=','.join(x for x in hidden.split(',') if not x.startswith('MER_'))
            for n,value in (stores or {}).items():w['Station'+str(n)]=value
            d['WeaponSystem1'+name]=w
            if role in ('f','fb'):
                sw={'LevelAttack':mode}
                for n,value in (secondary or {}).items():sw['Station'+str(n)]=value
                d['WeaponSystem3'+name]=sw
            if label:ldnames[name]=label
        a=lambda x:x+'|AAM'
        h=lambda x:x+'|Harpoon'
        t=lambda x:x+'|Tank'
        b=lambda x:x+'|Bomb'
        m=lambda x:x+'|MER6'
        if role=='f':
            load('Default',{1:a(ir),2:a(ir),3:a(bvr),4:a(bvr),5:a(ir),6:a(ir)})
            load('AirToAir',{1:a(ir),2:a(ir),3:a(bvr),4:a(bvr),5:a(ir),6:a(ir)})
            load('AirToAirLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank)},{1:a(phoenix),2:a(phoenix)})
            load('FleetIntercept',{1:a(ir),2:a(ir),3:a(bvr),4:a(bvr)},{1:a(phoenix),2:a(phoenix)},'Fleet interceptor')
        elif role=='rf':
            for n in ('Default','AirToAir','AirToAirLongRange','Recon','ReconLongRange'):
                load(n,{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:t(tank),6:t(tank)})
            load('ReconFast',{1:a(ir),2:a(ir)},label='Reconnaissance sprint (no tanks)')
        elif role=='ef':
            for n in ('Default','AirToAir','AirToAirLongRange','EW','EWLongRange'):
                load(n,{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:'ran_alq-131n_1',6:'ran_alq-131n_2'})
            load('EscortSEAD',{1:a(ir),2:a(ir),3:b(arm),4:b(arm),5:'ran_alq-131n_1',6:'ran_alq-131n_2'},label='Electronic attack and SEAD escort')
        else:
            # Existing bay geometry and its three concealed stations stay exact.
            wing.update(HarpoonPositions='0,0.0011,0.002',HarpoonRotations='-2,0,0')
            load('Default',{1:a(ir),2:a(ir),3:h(ship),4:h(ship)})
            load('AirToAir',{1:a(ir),2:a(ir),3:a(bvr),4:a(bvr),5:a(ir),6:a(ir)})
            load('AirToAirLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:a(phoenix),6:a(phoenix)})
            load('FleetIntercept',{1:a(ir),2:a(ir),3:a(bvr),4:a(bvr),5:a(phoenix),6:a(phoenix)},label='Fleet interceptor')
            load('AntiShip',{1:a(ir),2:a(ir),3:h(ship),4:h(ship)})
            load('AntiShipHeavy',{3:h(ship),4:h(ship),5:h(ship),6:h(ship)},{1:ship,2:ship,3:ship})
            load('AntiShipLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:h(ship),6:h(ship)},{1:ship,2:ship,3:ship})
            load('Strike',{1:a(ir),2:a(ir),3:m(aid('mk82_mer')),4:m(aid('mk82_mer')),5:m(aid('mk82_mer')),6:m(aid('mk82_mer'))},mode='DumbBombs,Missiles',mer=True)
            load('StrikeLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:m(aid('mk82_mer')),6:m(aid('mk82_mer'))},mode='DumbBombs,Missiles',mer=True)
            load('StrikeHeavy',{1:a(ir),2:a(ir),3:b(aid('mk84')),4:b(aid('mk84')),5:b(aid('mk84')),6:b(aid('mk84'))},mode='DumbBombs,Missiles')
            load('StrikeHeavyLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:b(aid('mk84')),6:b(aid('mk84'))},mode='DumbBombs,Missiles')
            load('StrikeMedium',{1:a(ir),2:a(ir),3:b(aid('mk83')),4:b(aid('mk83')),5:b(aid('mk83')),6:b(aid('mk83'))},label='Medium bombing',mode='DumbBombs,Missiles')
            for n,key in [('StrikePrecision','gbu10'),('StrikePrecisionLight','gbu12'),('StrikePrecisionMedium','gbu16')]:
                load(n,{1:a(ir),2:a(ir),3:b(aid(key)),4:b(aid(key)),5:b(aid(key)),6:'ran_nw_laserpod'},label={'StrikePrecisionLight':'Light precision bombing','StrikePrecisionMedium':'Medium precision bombing'}.get(n),mode='GuidedBombs,Missiles')
            load('StrikePrecisionLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:b(aid('gbu10')),6:'ran_nw_laserpod'},mode='GuidedBombs,Missiles')
            load('MaverickStrike',{1:a(ir),2:a(ir),3:b(mav),4:b(mav),5:b(mav),6:b(mav)},label='Maverick strike')
            load('SEAD',{1:a(ir),2:a(ir),3:b(arm),4:b(arm),5:b(arm),6:b(arm)},label='Suppression of enemy air defence')
            if year==1980:load('SEADShrike',{1:a(ir),2:a(ir),3:b(aid('shrike')),4:b(aid('shrike')),5:b(aid('shrike')),6:b(aid('shrike'))},label='Shrike SEAD')
            for n in ('EW','EWLongRange'):
                load(n,{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:'ran_nw_ecmpod_1|ECM',6:'ran_nw_ecmpod_2|ECM'})
            load('EscortSEAD',{1:a(ir),2:a(ir),3:b(arm),4:b(arm),5:'ran_nw_ecmpod_1|ECM',6:'ran_nw_ecmpod_2|ECM'},label='Electronic attack and SEAD escort')
            # Keep RF's four-tank reconnaissance fit available on the all-rounder.
            load('ReconLongRange',{1:a(ir),2:a(ir),3:t(tank),4:t(tank),5:t(tank),6:t(tank)})
            if year>=1985:
                load('EOGlideStrike',{1:a(ir),2:a(ir),3:b(aid('gbu15')),4:b(aid('gbu15')),5:'ran_nw_datalink'},label='Electro-optical glide bombing',mode='GuidedBombs,Missiles')
                load('StrikePavewayIII',{1:a(ir),2:a(ir),3:b(aid('gbu24')),4:b(aid('gbu24')),5:b(aid('gbu24')),6:'ran_nw_laserpod'},label='Paveway III precision bombing',mode='GuidedBombs,Missiles')
            if year>=1995:
                load('PopeyeStrike',{1:a(ir),2:a(ir),3:b(aid('popeye')),4:b(aid('popeye')),5:'ran_nw_datalink'},label='Popeye stand-off strike')
                load('SLAMStrike',{1:a(ir),2:a(ir),3:b(aid('slam')),4:b(aid('slam')),5:'ran_nw_datalink'},label='SLAM stand-off strike')
            if year>=2003:
                load('SLAMERStrike',{1:a(ir),2:a(ir),3:b(aid('slamer')),4:b(aid('slamer')),5:'ran_nw_datalink'},label='SLAM-ER stand-off strike')
                for n,key in [('JDAMHeavy','gbu31'),('JDAMMedium','gbu32'),('JSOWStrike','jsowa')]:
                    load(n,{1:a(ir),2:a(ir),3:b(aid(key)),4:b(aid(key)),5:b(aid(key)),6:b(aid(key))},label={'JDAMHeavy':'JDAM heavy bombing','JDAMMedium':'JDAM medium bombing','JSOWStrike':'JSOW stand-off glide bombing'}[n],mode='DumbBombs,Missiles')
            # A second air-targeting mode supplies Phoenix guidance without
            # changing the bay's physical station definitions.
            count=int(d['SensorSystems']['NumberOfSensorSystems'])+1
            d['SensorSystem'+str(count)]={'Type':'Radar','SystemName':'AN/AWG-9_Phoenix','Mount':'Dummy','ModuleType':'Sensor'}
            d['SensorSystems']['NumberOfSensorSystems']=str(count)
            d['WeaponSystem1']['AssociatedSensors']='SensorSystem3,SensorSystem'+str(count)
            # Align ECM pod tops to this model's outer hardpoint bottoms.
            # Values are calculated from the source meshes by the validator.
            wing['ECMPositions']='0,-0.0020,0';wing['ECMRotations']='-2,0,0'
        if role in ('f','fb','rf'):add_gun(d)
        d['WeaponSystems']['AvailableLoadouts']=','.join(presets)
        apply_investment(d,role,year)
        write_ini(MOD/'aircraft'/(uid+'.ini'),d)
        squad=read_ini(BASE/f'aircraft/ran_{role}-111n_squadrons.ini')
        end=YEARS[yi+1]-1 if yi+1<len(YEARS) else 2050
        for s,v in squad.items():
            if s!='General':
                v['ServiceDate']=f'{year}|{end}'
                if year>=1995:v['LiveryTexture']=f'ran_{role}-111n_{year}_usn_tps.png'
                v['FueltankTextures']=tank+',assets/textures/ran_f111n/'+v['LiveryTexture']
        write_ini(MOD/'aircraft'/(uid+'_squadrons.ini'),squad)
        names[uid]={'Type':{'f':'Fighter','fb':'Bomber','rf':'Recon','ef':'EW'}[role],
          'Default':f'{model} {nickname} ({year}),{model} {year}',
          'DefaultDescription':f'{year} edition of the fictional RAN-RAAF Naval Wing. '+{
            'f':'Fleet defence fighter with period Sidewinder or ASRAAM, Sparrow or AMRAAM, Phoenix and M61 Vulcan.',
            'fb':'All-round maritime and land strike aircraft; carries the fighter, reconnaissance and EW families\' period weapons, M61 Vulcan, and the unchanged three-missile internal bay.',
            'rf':'Fast reconnaissance and ELINT; defensive period IR missiles, M61 Vulcan, four tanks or clean sprint. Fictional Mach 3 performance retained.',
            'ef':'Electronic attack and SEAD escort with two physical ECM pods and two offensive ECM sensors; period defensive missiles and anti-radiation weapons.'}[role]+f' {BLOCKS[year]["name"]}. Empty mass {mass:,} kg; internal fuel {FUEL:,} kg. Naval weights are documented engineering estimates.',
          'Squadron1':f'{model} {year} - {squadrons[0]} Squadron heritage,{squadrons[0]} Sqn',
          'Squadron2':f'{model} {year} - {squadrons[1]} Squadron heritage,{squadrons[1]} Sqn',
          'Callsigns':'Squadron1,Pig,Boar,Tusk|Squadron2,Razor,Grunt,Hog'}
        details={}
        for name in presets:
            stores,by_system=inventory(d,name)
            store_mass=sum(CATALOG[k]['mass_kg']*n for k,n in stores.items())
            tank_fuel=sum(CATALOG[k].get('fuel_kg',0)*n for k,n in stores.items())
            ammo_mass=GUN_ROUNDS*GUN_ROUND_MASS if role!='ef' else 0
            gross=mass+FUEL+tank_fuel+store_mass+ammo_mass
            details[name]={'stores':stores,'wing_stores':by_system.get('1',{}),'auxiliary_external_stores':by_system.get('3',{}) if role=='f' else {},'internal_bay_stores':by_system.get('3',{}) if role=='fb' else {},
                'stores_mass_kg':round(store_mass,1),'total_fuel_kg':FUEL+tank_fuel,'gun_ammunition_mass_kg':ammo_mass,
                'full_fuel_takeoff_mass_kg':round(gross,1),'reference_max_takeoff_kg':LIMIT,'margin_kg':round(LIMIT-gross,1)}
        manifest[uid]={'name':model,'nickname':nickname,'edition':year,'service_years':[year,end],'role':ai,
           'empty_mass_kg':mass,'empty_mass_components_kg':components,'internal_fuel_kg':FUEL,
           'gun':{'system':'M61','rounds':GUN_ROUNDS,'position':'Separate fixed fuselage installation; does not consume bomb-bay stations','installation_mass_status':'Engineering allowance'} if role!='ef' else None,
           'mach_limit':float(d['Performance']['MachLimit']),'cruise_mach':float(d['Performance']['SpeedAndRange_Cruise'].split(',')[0]),
           'nominal_cruise_range_miles':int(d['Performance']['SpeedAndRange_Cruise'].split(',')[1]),
           'flight_response':{k:float(d['FlightModel'][k]) for k in ('VelocityGain','ThrustGain','PitchGain','HeadingGain','BankGain')},
           'propulsion':{'engine_count':int(d['Performance']['EngineCount']),'dry_thrust_n_per_engine':int(d['Performance']['PerEngineMaxThrust']),'afterburner_thrust_n_per_engine':int(d['Performance']['PerEngineMaxAfterburnerThrust'])},
           'carrier_capable':True,'investment_programme':describe_investment(role,year),'loadouts':details}
    write_ini(MOD/'language_en/aircraft_names.ini',names)
    write_ini(MOD/'language_en/loadout_names.ini',lds)
    (ROOT/'loadout_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'weapon_catalog.json').write_text(json.dumps(CATALOG,indent=2)+'\n')
    return manifest

def finish(manifest):
    info=read_ini(MOD/'_info.ini');info['Language_en'].update(Name='RAN F-111N Naval Wing V7 - 1980 / 1985 / 1995 / 2003',Description='Sixteen dated Australian naval aircraft with increasing engine, flight-control, targeting and EW investment. Period weapons, explicit mass budgets, M61 guns, preserved internal bay and carrier support. Dedicated USN-inspired 1995/2003 tactical grey liveries retain Australian markings.')
    write_ini(MOD/'_info.ini',info)
    # All carrier allowlists must include every new unit ID, not only the four
    # compatibility IDs inherited from V5.2.1.
    ids=list(manifest)
    helper=ROOT/'carrier_compatibility.py';s=helper.read_text()
    s=re.sub(r'^IDS=.*$', 'IDS='+repr(tuple(ids)),s,flags=re.M);helper.write_text(s)
    for p in (MOD/'vessels').glob('*.ini'):
        d=read_ini(p);deck=d.get('FlightDeck',{})
        if 'AircraftSupported' in deck:
            allowed=deck['AircraftSupported'].split(',')
            deck['AircraftSupported']=','.join(allowed+[u for u in ids if u not in allowed])
            write_ini(p,d)
    for f in ('install-ran-f111n.py','install-ran-f111n.sh'):
        p=ROOT/f;p.write_text(p.read_text().replace('V5.2.1','V7').replace('Naval Wing V6','Naval Wing V7'))
    # Profile artwork is reused without altering the four models/liveries.
    for uid in ids:
        original=uid.rsplit('_',1)[0] if uid[-4:].isdigit() else uid
        if uid!=original and int(uid[-4:])<1995:shutil.copy2(MOD/'ui/profiles'/(original+'.png'),MOD/'ui/profiles'/(uid+'.png'))
    (ROOT/'MOD_SHA256.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(MOD)) for p in sorted(MOD.rglob('*')) if p.is_file())+'\n')

def main():
    build_weapons();build_systems(MOD,ROOT,CATALOG,read_ini,write_ini);manifest=build_aircraft()
    from runtime_fixes import apply
    apply(ROOT,MOD)
    finish(manifest)
    print(json.dumps({'aircraft':len(manifest),'weapons_and_stores':len(CATALOG),'loadouts':sum(len(d['loadouts']) for d in manifest.values()),'largest_full_fuel_mass_kg':max(x['full_fuel_takeoff_mass_kg'] for d in manifest.values() for x in d['loadouts'].values())}))

if __name__=='__main__':main()
