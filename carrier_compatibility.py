#!/usr/bin/env python3
"""Generate carrier compatibility files inside this mod from installed data.

Source game/Workshop files are read-only. The resulting copies are native mod
overrides. The aircraft remain fixed-wing; VTOL-only carrier decks gain a
fictional arrested recovery point for the Naval Wing.
"""
from pathlib import Path
from collections import OrderedDict
import re,json,sys

IDS=('ran_f-111n', 'ran_f-111n_1985', 'ran_f-111n_1995', 'ran_f-111n_2003', 'ran_fb-111n', 'ran_fb-111n_1985', 'ran_fb-111n_1995', 'ran_fb-111n_2003', 'ran_rf-111n', 'ran_rf-111n_1985', 'ran_rf-111n_1995', 'ran_rf-111n_2003', 'ran_ef-111n', 'ran_ef-111n_1985', 'ran_ef-111n_1995', 'ran_ef-111n_2003')
CIRCUIT='0.5,800,-4.5|0.5,800,2.5|-0.75,800,3.2|-2,800,2.2|-2,500,-2.5|-0.75,500,-3.5|0.42,500,-3'
HOLD='-2.7,2000,-6|-1.9,2000,-6.6|-1.1,2000,-6|-1.9,2000,-4.7'

def parse(text):
    data=OrderedDict();section=None
    for raw in text.splitlines():
        line=raw.split('//',1)[0].strip()
        if not line or line.startswith(('#',';')):continue
        m=re.match(r'^\[([^]]+)\]',line)
        if m:
            section=m[1];data.setdefault(section,OrderedDict())
        elif section and '=' in line:
            k,v=line.split('=',1);data[section][k.strip()]=v.strip()
    return data

def put(text,section,key,value):
    # Change only the named key; preserve all unrelated source text and comments.
    pattern=re.compile(r'(?m)^\['+re.escape(section)+r'\][^\r\n]*$')
    match=pattern.search(text)
    if not match:return text.rstrip()+'\n\n['+section+']\n'+key+'='+str(value)+'\n'
    start=match.end();nxt=re.search(r'(?m)^\[',text[start:])
    end=start+nxt.start() if nxt else len(text)
    block=text[start:end]
    key_pattern=re.compile(r'(?m)^\s*'+re.escape(key)+r'\s*=.*$')
    new=key+'='+str(value)
    if key_pattern.search(block):block=key_pattern.sub(lambda m:new,block,count=1)
    else:block=block.rstrip()+'\n'+new+'\n\n'
    block='\n'+block.lstrip('\r\n')
    return text[:start]+block+text[end:]

def types(section):return {x.strip() for x in section.get('AllowedType','').split(',') if x.strip()}

def deduplicate(text):
    # Some exported carriers repeat active keys. Preserve the last value,
    # matching the game's INI reader, and retain every source comment.
    lines=text.splitlines(keepends=True);last={};entries={};section=None
    for i,line in enumerate(lines):
        value=line.split('//',1)[0].strip()
        if not value or value.startswith(('#',';')):continue
        m=re.match(r'^\[([^]]+)\]',value)
        if m:section=m[1]
        elif section and '=' in value:
            key=(section,value.split('=',1)[0].strip());last[key]=i;entries[i]=key
    return ''.join(line for i,line in enumerate(lines) if i not in entries or last[entries[i]]==i)

def is_carrier(data,name):
    if 'FlightDeck' not in data:return False
    # Detect aviation decks from their actual permissions, including modded
    # carriers with names such as hms_ark_royal rather than a _cv_ unit ID.
    fixed_wing_deck=any(
        types(point)&{'Plane','VTOL'} for section,point in data.items()
        if re.fullmatch(r'(?:Launch|Recovery)Point\d+',section))
    if fixed_wing_deck:return True
    # Helicopter-only carriers still need their role/name classification;
    # ordinary frigate/destroyer helicopter decks remain unchanged.
    role=data.get('General',{}).get('Role','').casefold()
    return ('carrier' in role or 'carrier' in name.casefold() or
        bool(re.search(r'(?:^|_)(?:cv[nleha]?|takr|lha|lhd|pkr)(?:_|$)',name,re.I)))

def compatible(text,name):
    data=parse(text)
    if not is_carrier(data,name):return None
    deck=data['FlightDeck'];nr=int(deck.get('NumberOfRecoveryPoints','0'))
    points=[(s,d) for s,d in data.items() if re.fullmatch(r'RecoveryPoint\d+',s)]
    launches=[(s,d) for s,d in data.items() if re.fullmatch(r'LaunchPoint\d+',s)]
    if not points or not launches:raise ValueError(name+': carrier lacks deck launch/recovery points')
    # Prefer an existing plane recovery, then the VTOL approach, then a deck spot.
    selected=min(points,key=lambda p:(0 if 'Plane' in types(p[1]) and int(p[0][13:])<=nr
        else 1 if 'Plane' in types(p[1]) else 2 if 'VTOL' in types(p[1]) else 3,int(p[0][13:])))
    recovery,rd=selected;index=int(recovery[13:])
    if 'Position' not in rd or 'AssociatedElevators' not in rd:
        raise ValueError(name+': recovery point lacks deck/elevator coordinates')
    source_recovery=recovery
    if 'Plane' not in types(rd):
        # Retain existing helicopter/VTOL approaches. Give fixed-wing aircraft
        # their own recovery point at that deck position with shared blocking.
        old_recovery=recovery
        index=max([nr]+[int(s[13:]) for s,_ in points])+1
        recovery='RecoveryPoint'+str(index)
        rd=rd.copy();rd['AllowedType']='Plane'
        for key,value in rd.items():text=put(text,recovery,key,value)
        text=put(text,recovery,'BlocksRecoveryPoints',','.join(str(int(s[13:])) for s,_ in points))
        for s,point in points:
            blocked=point.get('BlocksRecoveryPoints','').split(',')
            text=put(text,s,'BlocksRecoveryPoints',','.join(x for x in blocked+[str(index)] if x))
    text=put(text,'FlightDeck','NumberOfRecoveryPoints',max(nr,index))
    if 'Plane' not in types(rd):
        text=put(text,recovery,'AllowedType',rd.get('AllowedType','')+',Plane')
    # A conventional recovery already has an arresting-wire approach. For a
    # converted VTOL/heli spot, add the native fixed-wing circuit and arresting.
    converted=rd.get('Arrested','False').lower()!='true'
    if converted:
        text=put(text,recovery,'Arrested','True')
        text=put(text,recovery,'CircuitWaypoints',CIRCUIT)
        text=put(text,recovery,'LandingInterval',rd.get('LandingInterval','70'))
        text=put(text,'FlightDeck','HoldWaypoints',HOLD)
        text=put(text,'FlightDeck','HoldStackSeparation','1000')
        text=put(text,'FlightDeck','HoldEnterDistance','3')
    if 'LandingSpeeds' not in deck:text=put(text,'FlightDeck','LandingSpeeds','350,240,150')
    nl=int(deck.get('NumberOfLaunchPoints','0'))
    launch,ld=min(launches,key=lambda p:(0 if 'Plane' in types(p[1]) and int(p[0][11:])<=nl
        else 1 if 'Plane' in types(p[1]) else 2 if 'VTOL' in types(p[1]) else 3,int(p[0][11:])))
    text=put(text,'FlightDeck','NumberOfLaunchPoints',max(nl,int(launch[11:])))
    if 'Plane' not in types(ld):text=put(text,launch,'AllowedType',ld.get('AllowedType','')+',Plane')
    # Preserve the selected carrier's native taxi routes and elevator geometry.
    nt=int(deck.get('NumberOfTaxiPaths','0'))
    paths={s:d for s,d in data.items() if re.fullmatch(r'TaxiPath\d+',s)}
    elevators=rd['AssociatedElevators'].split(',')
    recovery_routes=[(s,d) for s,d in paths.items() if d.get('From')==recovery]
    for e in elevators:
        elev='Elevator'+e.strip()
        if elev not in data:raise ValueError(name+': missing '+elev)
        for origin,dest,position in [(recovery,elev,data[elev].get('RidePosition',data[elev].get('SpawnPosition'))),
                                      (elev,launch,ld.get('Position'))]:
            existing=[s for s,d in paths.items() if d.get('From')==origin and d.get('To')==dest]
            if existing:
                nt=max(nt,max(int(s[8:]) for s in existing));continue
            if not position:raise ValueError(name+': missing taxi coordinate '+dest)
            number=max([nt]+[int(s[8:]) for s in paths])+1
            s='TaxiPath'+str(number)
            for k,v in [('From',origin),('To',dest),('Waypoints',position)]:text=put(text,s,k,v)
            paths[s]={'From':origin,'To':dest};nt=number
        associated=data[elev].get('AssociatedLaunchPoints','').split(',')
        li=str(int(launch[11:]))
        if li not in associated:text=put(text,elev,'AssociatedLaunchPoints',','.join(x for x in associated+[li] if x))
    text=put(text,'FlightDeck','NumberOfTaxiPaths',nt)
    if 'AircraftSupported' in deck:
        supported=deck['AircraftSupported'].split(',')
        text=put(text,'FlightDeck','AircraftSupported',','.join(supported+[u for u in IDS if u not in supported]))
    return deduplicate(text),{'recovery':recovery,'source_recovery':source_recovery,'launch':launch,'converted_deck':converted,
        'aircraft':list(IDS),'carrier_air_group_preserved':True}

def generate(game,mod,extra_sources=()):
    game=Path(game).resolve();mod=Path(mod).resolve()
    streaming=game/'Sea Power_Data/StreamingAssets'
    roots=[streaming/'original']
    workshop=game.parents[1]/'workshop/content/1286220'
    if workshop.is_dir():roots.extend(sorted(p for p in workshop.iterdir() if p.is_dir()))
    user=streaming/'user'
    if user.is_dir():roots.extend(sorted(p for p in user.iterdir() if p.is_dir()))
    roots.extend(Path(p).resolve() for p in extra_sources)
    chosen={};duplicates={}
    for priority,root in enumerate(roots):
        if not root.is_dir() or root==mod or root.name.startswith('RAN-F111N-Naval-Wing'):continue
        # Only actual vessel-definition folders; no unrelated filesystem crawl.
        vessels=root/'vessels'
        if not vessels.is_dir():continue
        for p in sorted(vessels.rglob('*.ini')):
            if p.name.endswith('_variants.ini'):continue
            text=p.read_text(encoding='utf-8-sig')
            if not is_carrier(parse(text),p.stem):continue
            duplicates.setdefault(p.name,[]).append(str(p))
            key=(priority,p.stat().st_mtime_ns)
            if p.name not in chosen or key>chosen[p.name][0]:chosen[p.name]=(key,p,text)
    # Replace our own generated copies only; never write to any source root.
    dest=mod/'vessels';dest.mkdir(parents=True,exist_ok=True)
    report={'runtime_tested':False,'carriers':[],'errors':[],
        'source_precedence':'Explicit source > local user mods > Workshop folders (ID order) > original; current layout is retained per chosen source.'}
    for name,(_,source,text) in sorted(chosen.items()):
        try:
            result=compatible(text,Path(name).stem)
            output,detail=result
            (dest/name).write_text(output,encoding='utf-8')
            report['carriers'].append({'file':name,'source':str(source),**detail,
                'other_source_candidates':[p for p in duplicates[name] if p!=str(source)]})
        except (ValueError,KeyError) as error:report['errors'].append({'file':name,'reason':str(error)})
    (mod/'CARRIER_COMPATIBILITY.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    if len(sys.argv)<2:raise SystemExit('Usage: python3 carrier_compatibility.py "/path/to/Sea Power" [preferred-carrier-mod-folder ...]')
    report=generate(sys.argv[1],Path(__file__).resolve().parent/'RAN-F111N-Naval-Wing',sys.argv[2:])
    package=Path(__file__).resolve().parent
    if (package/'MOD_SHA256.txt').is_file():
        import hashlib
        mod=package/'RAN-F111N-Naval-Wing'
        lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(mod).as_posix()
            for p in sorted(mod.rglob('*')) if p.is_file()]
        (package/'MOD_SHA256.txt').write_text('\n'.join(lines)+'\n')
    print(json.dumps(report,indent=2))
    raise SystemExit(bool(report['errors']))
