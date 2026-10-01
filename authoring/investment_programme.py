"""Fictional Australian investment blocks expressed through native game fields.
F110 afterburning classes are supplier references; adaptations and other ratings
are hypothetical. RF propulsion is intentionally fictional for Mach 3.
"""
from copy import deepcopy
import re

FIELDS=('name','engine','dry_n','afterburner_n','acceleration','controls','range_factor','cruise','climb_factor','systems_mass','engine_mass','rf_thermal_mass','radar_gain','radar_range_factor','radar_targets','radar_weapons','lookdown','flir','esm_gain','rwr_resolution','elint_resolution','decm','jam_power','jam_range','jam_gain','jam_channels','ready_fb','ready_other','cooldown')
ROWS={
1980:('Block I: naval programme','TF30-P-109 reference',43600,82300,1,1,1,.84,1,0,0,0,0,1,1,2,.85,2,5,25,10,.40,1000,240,6,1,30,20,60),
1985:('Block II: propulsion and digital weapons','TF30 naval uprating (fictional)',47960,90530,1.10,1.05,1.06,.88,1.05,150,0,50,1,1.06,2,4,.90,2.1,5.5,22,8,.48,1250,260,6.5,2,25,18,55),
1995:('Block III: major re-engine and digital mission suite','F110-GE-400-class naval adaptation',60000,120000,1.25,1.10,1.14,.92,1.15,650,600,150,2.5,1.14,4,6,.96,2.4,6.5,17,6,.60,1700,300,7,3,20,15,45),
2003:('Block IV: networked precision and propulsion growth','F110-GE-129-class naval adaptation',65000,129000,1.40,1.15,1.22,.96,1.25,850,750,250,4,1.22,6,8,1,2.7,7.5,12,4,.72,2200,340,7.5,4,15,12,40)}
assert all(len(row)==len(FIELDS) for row in ROWS.values())
BLOCKS={year:dict(zip(FIELDS,row)) for year,row in ROWS.items()}

def sensor_id(kind,year):return f'RAN_NW_{kind}_{year}'
def pod_id(role,n,year):return ('ran_alq-131n_' if role=='ef' else 'ran_nw_ecmpod_')+str(n)+'_'+str(year)

def build_systems(mod,root,catalog,read_ini,write_ini):
    native=read_ini(root/'authoring/reference_sensors.ini')
    systems=read_ini(mod/'systems/sensors.ini');names=read_ini(mod/'language_en/ammunition_names.ini')
    for year,b in BLOCKS.items():
        for kind,donor in [('FleetRadar','AN/AWG-9'),('PhoenixControl','AN/AWG-9_Phoenix'),('StrikeRadar','AN/APQ-161')]:
            s=deepcopy(native[donor])
            s.update(Gain=str(float(s['Gain'])+b['radar_gain']),MaxRange=str(round(float(s['MaxRange'])*b['radar_range_factor'],2)),LookDownMultiplier=str(b['lookdown']),HasDataLink='True' if year>=1995 else 'False',RangeResolution=str({1980:30,1985:25,1995:18,2003:12}[year]))
            if kind!='PhoenixControl':s.update(TargetChannels=str(b['radar_targets']),WeaponChannels=str(b['radar_weapons']))
            systems[sensor_id(kind,year)]=s
        for kind,donor in [('FLIR','2nd_Gen_FLIR'),('RWR','AircraftRWR'),('ELINT','AircraftELINT'),('DECM','AircraftDECM_Late')]:
            s=deepcopy(native[donor])
            if kind=='FLIR':s.update(VIDRangeMultiplier=str(b['flir']),MaxRangeMultiplier=str(b['flir']))
            elif kind=='DECM':s['JamChance']=str(b['decm'])
            else:s.update(Gain=str(b['esm_gain']),AngularResolution=str(b['rwr_resolution'] if kind=='RWR' else b['elint_resolution']))
            systems[sensor_id(kind,year)]=s
        for n in (1,2):
            s=deepcopy(systems['RAN_ALQ99N_'+str(n)])
            s.update(PeakPower=str(b['jam_power']),MaxRange=str(b['jam_range']),Gain=str(b['jam_gain']),JamChannels=str(b['jam_channels']))
            jammer=sensor_id('OffensiveECM'+str(n),year);systems[jammer]=s
            for role,donor in [('ef','ran_alq-131n_'+str(n)),('fb','ran_nw_ecmpod_'+str(n))]:
                pid=pod_id(role,n,year);d=read_ini(mod/'ammunition'/(donor+'.ini'))
                if role=='fb':d['SensorSystem1']['SystemName']=jammer
                write_ini(mod/'ammunition'/(pid+'.ini'),d)
                catalog[pid]={**catalog[donor],'name':f'Naval offensive ECM pod {n} ({year})','earliest_edition':year,'simulation':'Two physical pods with dated native jammer power/channels; fictional programme ratings.'}
                names[pid]={'Default':f'Naval ECM pod {n} ({year}),ECM {year}','DefaultDescription':f'{year} Australian Naval Wing upgrade container.'}
    write_ini(mod/'systems/sensors.ini',systems);write_ini(mod/'language_en/ammunition_names.ini',names)

def mass_allowances(role,year):
    b=BLOCKS[year]
    return dict(investment_systems_and_controls_estimate=b['systems_mass'],propulsion_retrofit_estimate=b['engine_mass'],recon_thermal_upgrade_estimate=b['rf_thermal_mass'] if role=='rf' else 0)

def apply(d,role,year):
    b=BLOCKS[year];p=d['Performance'];fm=d['FlightModel']
    if role=='rf':
        p.update(PerEngineMaxThrust=str(round(320000*b['acceleration'])),PerEngineMaxAfterburnerThrust=str(round(480000*b['acceleration'])))
        cruise=2.52
    else:
        p.update(PerEngineMaxThrust=str(b['dry_n']),PerEngineMaxAfterburnerThrust=str(b['afterburner_n']));cruise=b['cruise']
    _,rng=p['SpeedAndRange_Cruise'].split(',')
    p['SpeedAndRange_Cruise']=f'{cruise},{round(float(rng)*b["range_factor"])}'
    p['MaxClimbRate']=str(round(float(p['MaxClimbRate'])*b['climb_factor']))
    for key in ('VelocityGain','ThrustGain'):fm[key]=f'{float(fm[key])*b["acceleration"]:.6f}'.rstrip('0').rstrip('.')
    for key in ('PitchGain','HeadingGain','BankGain'):fm[key]=f'{float(fm[key])*b["controls"]:.6f}'.rstrip('0').rstrip('.')
    mapping={'AN/AWG-9':'FleetRadar','AN/AWG-9_Phoenix':'PhoenixControl','AN/APQ-161':'StrikeRadar','2nd_Gen_FLIR':'FLIR','AircraftRWR':'RWR','AircraftELINT':'ELINT','AircraftDECM_Med':'DECM','AircraftDECM_Late':'DECM','RAN_ALQ99N_1':'OffensiveECM1','RAN_ALQ99N_2':'OffensiveECM2'}
    for section,s in d.items():
        if re.fullmatch(r'SensorSystem\d+',section) and s.get('SystemName') in mapping:s['SystemName']=sensor_id(mapping[s['SystemName']],year)
        if section.startswith('WeaponSystem') and 'ReadyUpTime' in s:s.update(ReadyUpTime=str(b['ready_fb'] if role=='fb' else b['ready_other']),CoolDownTime=str(b['cooldown']))
        if re.fullmatch(r'WeaponSystem\d+\D.*',section):
            for key,value in list(s.items()):
                if not re.fullmatch(r'Station\d+',key):continue
                store,*rack=value.split('|')
                for n in (1,2):
                    if store in ('ran_alq-131n_'+str(n),'ran_nw_ecmpod_'+str(n)):s[key]=pod_id(role,n,year)+('|'+rack[0] if rack else '')

def describe(role,year):
    b=BLOCKS[year]
    result={**b,'engine':'Fictional Australian Mach 3 propulsion package' if role=='rf' else b['engine'],'status':'Hypothetical investment; controls, installed thrust, sensor ratings and retrofit masses are estimates','radar_description':('AWG-9-class' if year<1995 else 'APG-71-class digital adaptation') if role=='f' else 'Naval multimode radar and mission computer','cockpit_visuals':'Original mesh retained; no new interactive cockpit or MFDs'}
    if role=='rf':result.update(dry_n=round(320000*b['acceleration']),afterburner_n=round(480000*b['acceleration']),cruise=2.52)
    return result
