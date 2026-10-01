#!/usr/bin/env python3
"""Paint source UV atlases without resampling or moving any UV island.

Authorised code-paint workflow: colours and vector decals are projected onto
the original surfaces; the input alpha channel and normal/specular maps stay intact.
"""
from pathlib import Path
import sys, re, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
from build_mod import ROOT, U, F, OUT, MOD, VARIANTS, read_ini, write_ini

package = Path(__file__).resolve().parent.parent
if (package/'RAN-F111N-Naval-Wing').is_dir():
    OUT = package
    MOD = package/'RAN-F111N-Naval-Wing'

W,H=3072,2048
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def load_obj(path):
    verts=[]; tex=[]; norms=[]; groups={}; group=''
    for line in Path(path).open():
        t=line.split()
        if not t: continue
        if t[0]=='v': verts.append(list(map(float,t[1:4])))
        elif t[0]=='vt': tex.append(list(map(float,t[1:3])))
        elif t[0]=='vn': norms.append(list(map(float,t[1:4])))
        elif t[0]=='o': group=t[1]; groups.setdefault(group,[])
        elif t[0]=='f':
            triples=[tuple(int(y)-1 if y else -1 for y in x.split('/')) for x in t[1:]]
            for i in range(1,len(triples)-1): groups[group].append([triples[0],triples[i],triples[i+1]])
    return np.asarray(verts),np.asarray(tex),np.asarray(norms),{k:np.asarray(v) for k,v in groups.items()}

def matrix(pos='0,0,0',rot='0,0,0'):
    a,b,c=np.radians([float(x) for x in rot.split(',')])
    rx=np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
    ry=np.array([[np.cos(b),0,np.sin(b)],[0,1,0],[-np.sin(b),0,np.cos(b)]])
    rz=np.array([[np.cos(c),-np.sin(c),0],[np.sin(c),np.cos(c),0],[0,0,1]])
    m=np.eye(4);m[:3,:3]=ry@rx@rz;m[:3,3]=[float(x) for x in pos.split(',')]
    return m

def transforms(ini):
    cache={}
    def get(name):
        if name in cache:return cache[name]
        d=ini.get(name,{})
        m=matrix(d.get('Position','0,0,0'),d.get('Rotation','0,0,0'))
        if d.get('Parent'):m=get(d['Parent'])@m
        cache[name]=m;return m
    result={'hull':np.eye(4),'tank':np.eye(4)}
    for name,d in ini.items():
        if 'Mesh' in d:result[d['Mesh']]=get(name)
    return result

EXTERIOR=['hull','canopy_l','canopy_r','left_wing','right_wing','Rudder','Elevator_l','Elevator_r',
          'hang1','hang2','hang3','hang4','flap_l','flap_r','aileron_l','aileron_r',
          'nose_gear_door_l','nose_gear_door_r','gear_door','breake','tank']

def surface_fields(obj,ini):
    vertices,uv,norms,groups=obj; trs=transforms(ini)
    world=np.zeros((H,W,3),dtype=np.float32)
    normal=np.zeros_like(world); ids=np.zeros((H,W),np.uint8)
    for gid,name in enumerate(EXTERIOR,1):
        if name not in groups:continue
        tr=trs.get(name,np.eye(4)); faces=groups[name]
        for face in faces:
            tt=uv[face[:,1]]*np.array([W,-H])+np.array([0,H])
            lo=np.maximum(np.floor(tt.min(0)).astype(int),0)
            hi=np.minimum(np.ceil(tt.max(0)).astype(int),[W-1,H-1])
            if (hi<lo).any():continue
            p0,p1,p2=tt; a=p1-p0;b=p2-p0;det=a[0]*b[1]-a[1]*b[0]
            if abs(det)<1e-7:continue
            xx=np.arange(lo[0],hi[0]+1,dtype=np.float32)+.5
            yy=np.arange(lo[1],hi[1]+1,dtype=np.float32)+.5
            dx=xx[None,:]-p0[0];dy=yy[:,None]-p0[1]
            u=(dx*b[1]-dy*b[0])/det;v=(a[0]*dy-a[1]*dx)/det
            use=(u>=-0.001)&(v>=-0.001)&(u+v<=1.001)
            if not use.any():continue
            vv=vertices[face[:,0]]@tr[:3,:3].T+tr[:3,3]
            nn=norms[face[:,2]]@tr[:3,:3].T if (face[:,2]>=0).all() else np.tile(np.cross(vv[1]-vv[0],vv[2]-vv[0]),(3,1))
            pp=vv[0]+u[...,None]*(vv[1]-vv[0])+v[...,None]*(vv[2]-vv[0])
            npv=nn[0]+u[...,None]*(nn[1]-nn[0])+v[...,None]*(nn[2]-nn[0])
            sl=(slice(lo[1],hi[1]+1),slice(lo[0],hi[0]+1))
            world[sl][use]=pp[use];normal[sl][use]=npv[use];ids[sl][use]=gid
    normal/=np.maximum(np.linalg.norm(normal,axis=2)[...,None],1e-8)
    return world,normal,ids

def pig_badge(kind,tactical=False):
    im=Image.new('RGBA',(640,480));d=ImageDraw.Draw(im)
    ink=(54,41,40,255);pink=(230,146,148,255);light=(247,243,235,255)
    if tactical:ink=(84,98,109,255);pink=(150,164,174,255);light=(199,208,212,255)
    # Wings echo the supplied flying-pig artwork, with clean vector edges.
    d.polygon([(295,257),(208,170),(125,96),(100,91),(110,131),(148,167),(115,151),(102,152),(117,184),(171,211),(137,204),(137,218),(192,247),(230,274)],fill=light,outline=ink,width=7)
    d.line([(123,133),(196,195),(247,244)],fill=(158,158,156),width=5)
    d.line([(135,175),(204,221)],fill=(158,158,156),width=5)
    d.polygon([(280,248),(287,160),(344,113),(371,108),(348,145),(321,175),(363,151),(380,154),(358,188),(322,208),(367,197),(379,207),(344,240),(298,275)],fill=light,outline=ink,width=7)
    d.ellipse((174,226,431,380),fill=pink,outline=ink,width=8)
    d.polygon([(394,247),(415,202),(454,243)],fill=pink,outline=ink,width=7)
    d.ellipse((382,236,502,345),fill=pink,outline=ink,width=8)
    d.ellipse((462,276,550,332),fill=pink if tactical else (244,173,171),outline=ink,width=7)
    d.ellipse((490,291,502,308),fill=ink);d.ellipse((517,291,529,308),fill=ink)
    d.ellipse((441,259,455,281),fill=ink);d.ellipse((445,262,450,269),fill=(255,255,255,255))
    d.arc((416,288,473,335),0,150,fill=ink,width=5)
    d.polygon([(211,343),(194,411),(215,424),(246,367)],fill=pink,outline=ink,width=6)
    d.polygon([(326,359),(339,412),(362,415),(364,350)],fill=pink,outline=ink,width=6)
    d.polygon([(184,409),(215,415),(216,430),(180,427)],fill=ink)
    d.polygon([(333,408),(367,409),(369,425),(337,425)],fill=ink)
    d.arc((124,248,193,305),75,335,fill=pink,width=13);d.arc((139,257,176,290),20,315,fill=ink,width=4)
    if kind=='ef':d.polygon([(168,96),(138,165),(177,163),(151,224),(210,143),(176,147),(196,96)],fill=ink if tactical else (219,175,34,255),outline=ink,width=5)
    if kind=='rf':
        for y in [300,333,367]:d.line([(69,y),(142,y)],fill=(82,111,133,255),width=10)
    if kind=='fb':
        mud=(112,125,135,255) if tactical else (123,93,66,255)
        d.ellipse((233,288,287,314),fill=mud);d.ellipse((292,331,342,350),fill=mud)
    return im

def text_image(text,size=170,ink=(25,29,32,255)):
    font=ImageFont.truetype(FONT,size)
    bb=font.getbbox(text);im=Image.new('RGBA',(bb[2]+16,bb[3]-bb[1]+16))
    ImageDraw.Draw(im).text((8,8-bb[1]),text,font=font,fill=ink)
    return im

def project(canvas,art,sel,u,v):
    a=np.asarray(art.convert('RGBA'));h,w=a.shape[:2]
    valid=sel&(u>=0)&(u<=1)&(v>=0)&(v<=1)
    iy,ix=np.nonzero(valid)
    if not len(ix):return
    sampled=a[np.minimum((v[valid]*h).astype(int),h-1),np.minimum((u[valid]*w).astype(int),w-1)]
    alpha=sampled[:,3:4].astype(np.float32)/255
    canvas[iy,ix,:3]=(canvas[iy,ix,:3]*(1-alpha)+sampled[:,:3]*alpha).astype(np.uint8)

def paint(source,world,norm,ids,short,era):
    orig=np.asarray(Image.open(source).convert('RGBA'))
    out=orig.copy();rgb=orig[:,:,:3].astype(np.float32)
    ext=(ids>0)&(orig[:,:,3]>0)
    x,y,z=np.moveaxis(world,-1,0)
    hull=(ids==1);fin=(hull|(ids==EXTERIOR.index('Rudder')+1))&(y>.021)&(z<-.068)
    if short=='ef':
        detail=(rgb.mean(2)-gaussian_filter(rgb.mean(2),5))*.75
        paintable=ext&(rgb.max(2)>32)&(rgb.max(2)<230)
    else:
        palette=np.array([[51,54,51],[66,77,65],[150,130,98],[88,95,80],[60,72,60],[80,89,80],[47,51,47]],np.float32)
        dist=np.full((H,W),np.inf,np.float32);nearest=np.zeros_like(rgb)
        for c in palette:
            dd=((rgb-c)**2).sum(2);use=dd<dist;dist[use]=dd[use];nearest[use]=c
        detail=np.clip((rgb-nearest).mean(2),-48,28)*.75
        yy,xx=np.indices((H,W))
        # Paint the original camouflage bleed around each island as well. This
        # preserves mip-map borders, without moving or redrawing a UV edge.
        exterior_band=((xx>=1024)&~((xx>=2048)&(yy>=1024)))|((xx>=400)&(xx<1024)&(yy>=1390)&(yy<1570))
        paintable=(ext|exterior_band)&(dist<4200)&(rgb.max(2)>22)&(orig[:,:,3]>0)
    # Keep warning-red, formation lights and reflective yellow markers.
    red=(rgb[:,:,0]>75)&(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>rgb[:,:,2]*1.4)
    yellow=(rgb[:,:,0]>155)&(rgb[:,:,1]>140)&(rgb[:,:,2]<110)
    paintable&=~(red|yellow)
    yy,xx=np.indices((H,W))
    protected=((xx<1024)&(yy<1024))|((xx>=2048)&(yy>=1024))
    protected|=((xx>=1440)&(xx<1840)&(yy<130))
    paintable&=~protected
    # Metallic exhaust texture is preserved rather than greywashed.
    paintable&=~(hull&(z<-.102)&(y<.018))
    target=np.zeros_like(rgb);base=np.array([195,203,208]) if era==1985 else np.array([168,181,193])
    target[:]=base
    target[norm[:,:,1]>.4]=base-np.array([7,6,4])
    target[norm[:,:,1]<-.4]=[216,220,220] if era==1985 else [195,204,212]
    target+=detail[...,None]
    out[:,:,:3][paintable]=np.clip(target[paintable],0,255).astype(np.uint8)
    # Radome colour is applied on the original nose surface, using real geometry.
    nose=hull&(z>.145)&(y<.02)&ext
    forebody=hull&(z>.105)&(z<=.145)&(y<.02)&ext&~(red|yellow)
    out[:,:,:3][forebody]=np.clip(target[forebody],0,255).astype(np.uint8)
    out[:,:,:3][nose]=np.clip(np.array([39,43,47])+detail[nose,None],0,255).astype(np.uint8)
    # Replace prior nationality/fin codes only in their mapped decal areas.
    for xa,ya,xb,yb in [(1816,1290,1875,1330),(1192,1665,1270,1710),
                       (1785,1200,1950,1330),(1070,1510,1220,1660)]:
        sl=(slice(ya,yb),slice(xa,xb));remove=ext[sl]
        out[sl][:,:,:3][remove]=np.clip(target[sl][remove],0,255).astype(np.uint8)
    # The fin stripe projects over the fixed fin and hinged rudder consistently.
    stripe=fin&(z<-.108)&(z>-.118)&(y>.025)
    checks=((np.floor((y-.025)/.0042)+np.floor((z+.118)/.0035)).astype(int)%2)==0
    out[stripe&checks,:3]=[179,37,43];out[stripe&~checks,:3]=[241,239,232]
    tip=fin&(y>.045)
    out[tip,:3]=[179,37,43]
    if short=='ef':
        # The Raven's raised ECM fairing is aircraft grey, not a red fin tip.
        fairing=hull&(y>.043)&(z<-.068)&ext
        out[:,:,:3][fairing]=np.clip(target[fairing],0,255).astype(np.uint8)
    if era==1985:
        wing=(ids==EXTERIOR.index('left_wing')+1)|(ids==EXTERIOR.index('right_wing')+1)
        out[wing&(abs(x)>.133),:3]=[176,41,46]
    roundel=Image.open(ROOT/'roundel.png')
    body=hull&(abs(norm[:,:,0])>.45)&(abs(x)>.007)&(y<.015)
    project(out,roundel,body,(.068-z)/.009+.5,(-.0018-y)/.009+.5)
    wing=(ids==EXTERIOR.index('left_wing')+1)|(ids==EXTERIOR.index('right_wing')+1)
    project(out,roundel,wing,(.0004-z)/.009+.5,(.10044-abs(x))/.009+.5)
    badge=pig_badge(short)
    project(out,badge,fin,(z+.0905)/.014+.5,(.034-y)/.0105+.5)
    serial={'f':'A8-201','fb':'A8-301','rf':'A8-401','ef':'A8-501'}[short]
    # Sea Power/Unity uses a left-handed camera basis. On the +X side, the
    # nose (+Z) is screen-right. The supplied game screenshot confirms that
    # the opposite convention used by the old preview mirrored both labels.
    side=np.where(x>=0,1.,-1.)
    project(out,text_image(serial),fin,side*(z+.092)/.012+.5,(.0248-y)/.0026+.5)
    project(out,text_image('NAVY'),body,side*(z-.048)/.011+.5,(.005-y)/.0035+.5)
    # Exact alpha preservation prevents material/cockpit transparency regressions.
    out[:,:,3]=orig[:,:,3]
    out[protected]=orig[protected]
    return Image.fromarray(out,'RGBA')

def main():
    fields={}
    for short,cfg in VARIANTS.items():
        unit='ran_'+short+'-111n'; model=cfg['model']
        if model not in fields:
            obj=load_obj(U/f'assets/models/vechicle/aircraft/{model}/{model}.obj')
            ini=read_ini(U/'aircraft/usaf_ef-111.ini' if model=='ef-111' else F/'aircraft/raaf_f-111c1985.ini')
            print('Mapping original UV surfaces:',model,flush=True)
            fields[model]=surface_fields(obj,ini)
        source=U/'assets/textures/ef-111/42nd_ECS.png' if short=='ef' else F/'assets/textures/f-111c'/('rf-111c.png' if short=='rf' else 'f-111c.png')
        dest=MOD/'assets/textures/ran_f111n';dest.mkdir(parents=True,exist_ok=True)
        for era,suffix in [(1985,''),(1990,'_1990')]:
            im=paint(source,*fields[model],short,era)
            path=dest/(unit+suffix+'.png');im.save(path,optimize=True)
            print('Painted',path.name,flush=True)
        sqpath=MOD/f'aircraft/{unit}_squadrons.ini';sq=read_ini(sqpath)
        sq['Squadron2']['LiveryTexture']=unit+'_1990.png'
        tankid='ran_tank_600_'+short+'111n'
        sq['Squadron2']['FueltankTextures']=tankid+',assets/textures/ran_f111n/'+unit+'_1990.png'
        write_ini(sqpath,sq)
    print('Eight exact-size texture maps created.',flush=True)

if __name__=='__main__':main()
