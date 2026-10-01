#!/usr/bin/env python3
"""Bake code-native USN-inspired surface materials and vector decals into UVs.
Original geometry/UVs/alpha stay exact; cockpit/mechanical atlas areas protected.
RGB approximates FS35237/36320/36375, not certified Federal Standard chips.
"""
from functools import lru_cache
import hashlib,json,subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter,distance_transform_edt
from era_upgrade import ROOT,MOD,ROLES,read_ini,write_ini,unit_id
from paint_textures import load_obj,surface_fields,EXTERIOR,project,pig_badge,text_image,W,H
PALETTE={'upper':[136,151,163],'sides':[158,169,180],'under':[184,194,202],'stencil':[71,85,97]}

def protected_pixels():
    yy,xx=np.indices((H,W))
    return ((xx<1024)&(yy<1024))|((xx>=2048)&(yy>=1024))|((xx>=1440)&(xx<1840)&(yy<130))

@lru_cache(maxsize=1)
def roundel():
    svg=ROOT/'authoring/roundel_tactical.svg';png=svg.with_suffix('.png')
    source=(ROOT/'authoring/roundel.svg').read_text()
    for old,new in [('#012169','#536777'),('#fff','#b8c2ca'),('#c8102e','#536777')]:source=source.replace(old,new)
    svg.write_text(source)
    subprocess.run(['inkscape',str(svg),'--export-type=png',f'--export-filename={png}','--export-width=602'],check=True,capture_output=True)
    return Image.open(png).convert('RGBA')

def bake(original,world,norm,ids,role,year):
    out=original.copy();rgb=original[:,:,:3].astype(np.float32)
    x,y,z=np.moveaxis(world,-1,0);ext=(ids>0)&(original[:,:,3]>0)
    protected=protected_pixels();hull=(ids==1)
    fin=(hull|(ids==EXTERIOR.index('Rudder')+1))&(y>.021)&(z<-.068)
    luma=rgb.mean(2);detail=np.clip(luma-gaussian_filter(luma,5),-25,16)
    base=np.empty_like(rgb);base[:]=PALETTE['sides']
    base[norm[:,:,1]>.38]=PALETTE['upper'];base[norm[:,:,1]<-.38]=PALETTE['under']
    fade=2 if year==1995 else 5
    weather=fade*np.sin(x*730+z*210)*np.cos(z*510+y*150)
    base+=detail[...,None]+weather[...,None]
    if year==2003:base[(np.sin(z*430+x*270)>.62)&(np.cos(x*420+y*740)>.45)]+=4
    gray=(rgb.max(2)-rgb.min(2)<65)&(luma>64)&(luma<231)
    red=(rgb[:,:,0]>75)&(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>rgb[:,:,2]*1.4)
    yellow=(rgb[:,:,0]>155)&(rgb[:,:,1]>140)&(rgb[:,:,2]<110)
    exhaust=hull&(z<-.102)&(y<.018)
    use=ext&gray&~(protected|red|yellow|exhaust)
    use|=fin&ext&~protected
    nose=hull&(z>.145)&(y<.02)&ext&~protected
    base[nose]=np.array(PALETTE['sides'])-10+detail[nose,None];use|=nose
    out[:,:,:3][use]=np.clip(base[use],0,255).astype(np.uint8)
    distance,nearest=distance_transform_edt(~ext,return_indices=True)
    bleed=(distance<=10)&~ext&gray&~protected&(original[:,:,3]>0)
    iy,ix=nearest;out[:,:,:3][bleed]=out[iy[bleed],ix[bleed],:3]
    stripe=fin&(z<-.108)&(z>-.118)&(y>.025)&~protected
    checks=((np.floor((y-.025)/.0042)+np.floor((z+.118)/.0035)).astype(int)%2)==0
    out[stripe&checks,:3]=[90,106,118];out[stripe&~checks,:3]=[179,190,198]
    out[fin&(y>.045)&~protected,:3]=[90,106,118]
    if role=='ef':
        fairing=hull&(y>.043)&(z<-.068)&ext&~protected
        out[:,:,:3][fairing]=np.clip(base[fairing],0,255).astype(np.uint8)
    body=hull&(abs(norm[:,:,0])>.45)&(abs(x)>.007)&(y<.015)&~protected
    wing=((ids==EXTERIOR.index('left_wing')+1)|(ids==EXTERIOR.index('right_wing')+1))&~protected
    project(out,roundel(),body,(.068-z)/.009+.5,(-.0018-y)/.009+.5)
    project(out,roundel(),wing,(.0004-z)/.009+.5,(.10044-abs(x))/.009+.5)
    project(out,pig_badge(role,tactical=True),fin&~protected,(z+.0905)/.014+.5,(.034-y)/.0105+.5)
    serial={'f':'A8-201','fb':'A8-301','rf':'A8-401','ef':'A8-501'}[role]
    side=np.where(x>=0,1.,-1.);ink=tuple(PALETTE['stencil'])+(255,)
    project(out,text_image(serial,ink=ink),fin&~protected,side*(z+.092)/.012+.5,(.0248-y)/.0026+.5)
    project(out,text_image('NAVY',ink=ink),body,side*(z-.048)/.011+.5,(.005-y)/.0035+.5)
    out[protected]=original[protected];out[:,:,3]=original[:,:,3]
    return out

def main():
    fields={};records=[];folder=MOD/'assets/textures/ran_f111n';protected=protected_pixels()
    for role in ROLES:
        d=read_ini(MOD/'aircraft'/(unit_id(role,1980)+'.ini'));models=d['Models']
        mesh=MOD/models['ResourcesFolder']/models['ResourcesRoot']
        if mesh not in fields:
            print('Mapping original geometry:',mesh.name,flush=True)
            fields[mesh]=surface_fields(load_obj(mesh),d)
        source=folder/f'ran_{role}-111n_1990.png';original=np.asarray(Image.open(source).convert('RGBA'))
        for year in (1995,2003):
            uid=unit_id(role,year);filename=f'ran_{role}-111n_{year}_usn_tps.png';path=folder/filename
            pixels=bake(original,*fields[mesh],role,year);Image.fromarray(pixels).save(path,optimize=True)
            squad=read_ini(MOD/'aircraft'/(uid+'_squadrons.ini'))
            for section,s in squad.items():
                if section!='General':s['LiveryTexture']=filename;s['FueltankTextures']=f'ran_tank_600_{role}111n,assets/textures/ran_f111n/{filename}'
            write_ini(MOD/'aircraft'/(uid+'_squadrons.ini'),squad)
            records.append(dict(aircraft=uid,year=year,texture=str(path.relative_to(MOD)),source=str(source.relative_to(MOD)),dimensions=[pixels.shape[1],pixels.shape[0]],alpha_preserved=bool(np.array_equal(pixels[:,:,3],original[:,:,3])),cockpit_mechanical_preserved=bool(np.array_equal(pixels[protected],original[protected])),changed_pixels=int(np.count_nonzero(np.any(pixels!=original,axis=2))),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            print('Baked',filename,flush=True)
    result={'status':'PASS' if all(r['alpha_preserved'] and r['cockpit_mechanical_preserved'] and r['changed_pixels']>0 for r in records) else 'FAIL','maps':records,'palette_rgb':PALETTE,'scope':'Exact 3072x2048 native UV maps; alpha and cockpit/mechanical regions preserved; no mesh, normal or specular changes.','runtime_tested':False}
    (ROOT/'USN_TEXTURE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
