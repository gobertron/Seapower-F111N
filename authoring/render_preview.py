#!/usr/bin/env python3
"""Render actual shipped OBJ meshes and textures for visual QA (not a game test)."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from build_mod import MOD,OUT,ROOT,read_ini,VARIANTS
from paint_textures import load_obj,matrix,FONT

package = Path(__file__).resolve().parent.parent
if (package/'RAN-F111N-Naval-Wing').is_dir():
    OUT = package
    MOD = package/'RAN-F111N-Naval-Wing'

CACHE={}
def obj(p):
    p=Path(p)
    if p not in CACHE:CACHE[p]=load_obj(p)
    return CACHE[p]

def pose(ini,flight):
    data={s:d.copy() for s,d in ini.items()}
    if flight:
        ani=read_ini(MOD/'animations'/(data['Animations']['AnimationFile_1']+'.ini'))
        a=ani['Gear_Retract']
        for n in range(1,int(a['NumberOfSequencesToPlay'])+1):
            target=a[f'Sequence{n}_Model'];seq=ani[a[f'Sequence{n}']]
            last=seq['Step'+seq['NumberOfSteps']].split('|')
            for field,new in [('Position',last[1]),('Rotation',last[2])]:
                old=data[target].get(field,'0,0,0').split(',')
                values=[o if x in ['x','y','z'] else x for x,o in zip(new.split(','),old)]
                data[target][field]=','.join(values)
    cache={}
    def transform(name):
        if name in cache:return cache[name]
        d=data.get(name,{})
        m=matrix(d.get('Position','0,0,0'),d.get('Rotation','0,0,0'))
        if d.get('Parent'):m=transform(d['Parent'])@m
        cache[name]=m;return m
    return transform

def scene(unit,flight,loadout):
    ini=read_ini(MOD/f'aircraft/{unit}.ini');tr=pose(ini,flight)
    meshes=[];models=ini['Models'];root=MOD/models['ResourcesFolder']/models['ResourcesRoot']
    squad=read_ini(MOD/f'aircraft/{unit}_squadrons.ini')['Default']
    diffuse=MOD/squad['ResourcesLiveryFolder']/squad['LiveryTexture']
    maintex=np.asarray(Image.open(diffuse))
    meshes.append((obj(root),models['ResourcesMesh'],np.eye(4),maintex,None))
    hidden=set()
    for name,d in ini.items():
        if name.startswith('WeaponSystem') and name.endswith(loadout):hidden.update(d.get('SubModelsToHide','').split(','))
    for name in ini['Submodels'].values():
        if name in hidden or name=='Afterburner':continue
        s=ini[name]
        if 'ResourcesMeshFolder' in s:
            path=MOD/s['ResourcesMeshFolder']/s.get('RootMesh','')
            if not path.is_file():continue
        else:path=root
        color=None;tex=maintex
        if s.get('Material')=='cockpit_glass':color=np.array([50,79,94,255]);tex=None
        elif s.get('Material','').endswith('pilot_a_mat'):color=np.array([78,86,68,255]);tex=None
        meshes.append((obj(path),s['Mesh'],tr(name),tex,color))
    for i in range(1,int(ini['WeaponSystems']['NumberOfWeaponSystems'])+1):
        ws=ini.get(f'WeaponSystem{i}',{});ld=ini.get(f'WeaponSystem{i}{loadout}',{})
        for key,value in ld.items():
            if not key.startswith('Station'):continue
            ammo=value.split('|')[0].split('*')[0]
            if not ammo.startswith('ran_'):continue
            ad=read_ini(MOD/f'ammunition/{ammo}.ini');md=ad['Models']
            path=MOD/md['ResourcesFolder']/md['ResourcesRoot']
            # Stock meshes are supplied by the installed game, not this ZIP.
            if not path.is_file():continue
            mat=read_ini(MOD/md['ResourcesFolder']/md['ResourcesMaterial'])
            texture=maintex if ammo.startswith('ran_tank_600_') else np.asarray(Image.open(MOD/mat['Textures']['_MainTex']))
            position=ws[key]
            transform=matrix(position,ws.get(key+'Rotation','0,0,0'))
            if '|' in value:
                rack=value.split('|')[1]
                positions=ws[rack+'Positions'].split('|')
                rotations=ws.get(rack+'Rotations','0,0,0').split('|')
                for n,offset in enumerate(positions):
                    meshes.append((obj(path),md['ResourcesMesh'],transform@matrix(offset,rotations[n] if n<len(rotations) else rotations[0]),texture,None))
            else:meshes.append((obj(path),md['ResourcesMesh'],transform,texture,None))
    return meshes

def render(meshes,width=1120,height=680,transparent=False,side=False,eye_vector=None,scale=2400):
    bg=np.empty((height,width,3),np.uint8)
    for y in range(height):bg[y]=[226-int(y/height*12),232-int(y/height*12),236-int(y/height*12)]
    depth=np.full((height,width),-np.inf)
    eye=np.array(eye_vector if eye_vector is not None else ([1.,.05,.03] if side else [.8,.36,.68]));eye/=np.linalg.norm(eye)
    # Match the Unity camera basis, calibrated against the supplied in-game
    # side view. The previous right-handed projection masked mirrored text.
    right=np.cross(eye,[0,1,0]);right/=np.linalg.norm(right)
    up=np.cross(right,eye);light=np.array([.4,.8,.3]);light/=np.linalg.norm(light)
    center=np.array([0,0,.025])
    for (vertices,uv,normals,groups),name,tr,texture,color in meshes:
        if name not in groups:continue
        world=vertices@tr[:3,:3].T+tr[:3,3];q=world-center
        screen=np.column_stack([width/2+q@right*scale,height/2-q@up*scale,q@eye])
        rn=normals@tr[:3,:3].T
        for face in groups[name]:
            idx=face[:,0];p=screen[idx];tt=uv[face[:,1]];nn=rn[face[:,2]]
            lo=np.maximum(np.floor(p[:,:2].min(0)).astype(int),0)
            hi=np.minimum(np.ceil(p[:,:2].max(0)).astype(int),[width-1,height-1])
            if (hi<lo).any():continue
            a=p[1,:2]-p[0,:2];b=p[2,:2]-p[0,:2];det=a[0]*b[1]-a[1]*b[0]
            if abs(det)<1e-7:continue
            xx=np.arange(lo[0],hi[0]+1)+.5;yy=np.arange(lo[1],hi[1]+1)+.5
            dx=xx[None,:]-p[0,0];dy=yy[:,None]-p[0,1]
            u=(dx*b[1]-dy*b[0])/det;v=(a[0]*dy-a[1]*dx)/det
            z=p[0,2]+u*(p[1,2]-p[0,2])+v*(p[2,2]-p[0,2])
            sl=(slice(lo[1],hi[1]+1),slice(lo[0],hi[0]+1))
            use=(u>=0)&(v>=0)&(u+v<=1)&(z>depth[sl])
            if not use.any():continue
            ns=nn[0]+u[...,None]*(nn[1]-nn[0])+v[...,None]*(nn[2]-nn[0])
            ns/=np.maximum(np.linalg.norm(ns,axis=2)[...,None],1e-8)
            lit=.58+.42*np.clip(ns@light,0,1)
            if texture is not None:
                coords=tt[0]+u[...,None]*(tt[1]-tt[0])+v[...,None]*(tt[2]-tt[0])
                ty=np.clip(((1-coords[:,:,1])*texture.shape[0]).astype(int),0,texture.shape[0]-1)
                tx=np.clip((coords[:,:,0]*texture.shape[1]).astype(int),0,texture.shape[1]-1)
                rgba=texture[ty,tx];use&=rgba[:,:,3]>50
            else:rgba=np.broadcast_to(color,(*u.shape,4))
            bg[sl][use]=np.clip(rgba[:,:,:3][use]*lit[use,None],0,255).astype(np.uint8)
            depth[sl][use]=z[use]
    if transparent:
        return Image.fromarray(np.dstack([bg,((depth>-np.inf)*255).astype(np.uint8)]),'RGBA')
    return Image.fromarray(bg)

def main():
    panels=[]
    for short,cfg in VARIANTS.items():
        unit='ran_'+short+'-111n'
        loadout='AirToAirLongRange' if short=='f' else 'AntiShipLongRange' if short=='fb' else 'Default'
        print('Rendering',unit,flush=True)
        im=render(scene(unit,True,loadout))
        d=ImageDraw.Draw(im)
        d.text((36,28),cfg['name']+' '+cfg['nickname'],font=ImageFont.truetype(FONT,30),fill=(35,53,65))
        details={'f':'2 AAM + 2 Phoenix + 2 tanks','fb':'2 AIM-9L + 5 AGM-84C + 2 tanks',
                 'rf':'2 AAM + 4 tanks | Mach 2.52 cruise / Mach 3 max','ef':'2 AAM + 2 tanks + 2 ECM pods / 2 offensive ECM'}[short]
        d.text((36,74),details,font=ImageFont.truetype(FONT,19),fill=(64,83,93))
        d.text((36,642),'Airframe/tanks/ECM render; native missile and bomb meshes omitted',font=ImageFont.truetype(FONT,16),fill=(85,102,111))
        im.save(OUT/(unit+'_preview.png'));panels.append(im)
        profile=render(scene(unit,True,'Default'),transparent=True,side=True)
        profile=profile.crop(profile.getbbox());profile.thumbnail((751,206),Image.Resampling.LANCZOS)
        icon=Image.new('RGBA',(771,226));icon.alpha_composite(profile,((771-profile.width)//2,(226-profile.height)//2))
        dest=MOD/'ui/profiles';dest.mkdir(parents=True,exist_ok=True);icon.save(dest/(unit+'.png'))
    contact=Image.new('RGB',(2240,1420),(233,237,240))
    for i,im in enumerate(panels):contact.paste(im,((i%2)*1120,(i//2)*680))
    ImageDraw.Draw(contact).text((38,1384),'RAN Naval Wing V5 | Source-model visual check; Sea Power runtime testing still required.',font=ImageFont.truetype(FONT,20),fill=(45,62,71))
    contact.save(OUT/'RAN-F111N-preview.png')
    im=render(scene('ran_f-111n',False,'AirToAirLongRange'))
    im.save(OUT/'waterpig_gear_extended.png')

if __name__=='__main__':main()
