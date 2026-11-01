#!/usr/bin/env python3
"""Add two full skins using the existing bay-door hinges and hull UV atlas.

The skins are alternate-history geometry, generated with the Python standard
library. Their outline follows the native leaves' measured world footprint.
The original objects and all non-bay vertices and faces are kept unchanged.
"""
import re

NAMES = ('ran_bay_panel_l', 'ran_bay_panel_r')
OLD = ('bay_l', 'bay_r')

# (world z, half-width). The stock door pivots are (±.00993,-.012672,.063121).
# Samples trace the pre-existing door outline; adjacent samples are interpolated.
OUTLINE = ((.03230,.01032),(.03300,.01101),(.04000,.01077),
           (.05000,.01042),(.06000,.01007),(.07000,.00968),
           (.08000,.00927),(.08500,.00906),(.09000,.00762),
           (.09300,.00678),(.09500,.00623),(.09680,.00572))

def patch_obj(text):
    present = [bool(re.search(r'(?m)^o '+re.escape(name)+r'\s*$', text)) for name in NAMES]
    if all(present):
        return text
    if any(present):
        raise ValueError('partial generated panel geometry detected')
    for name in OLD:
        if len(re.findall(r'(?m)^o '+name+r'\s*$', text)) != 1:
            raise ValueError('expected original OBJ object '+name)
    counts = {prefix: len(re.findall(r'(?m)^'+prefix+r' ', text)) for prefix in ('v','vt','vn')}
    chunks = [text.rstrip('\n')+'\n']
    for side, name, pivot_x, uv_u, uv_v in (
        (1, NAMES[0], .009929, .4956, .0821),
        (-1, NAMES[1], -.009936, .4919, .4159),
    ):
        chunks.append('\n# Naval Wing V9 closed-bay surface; local to original hinge\no '+name+'\n')
        v0, t0, n0 = counts['v'], counts['vt'], counts['vn']
        for thickness in (0., .00018):
            for z,width in OUTLINE:
                # The centre seam is lowest; outside rises with the belly.
                # The back face is offset so it is not coplanar with the skin.
                for world_x, world_y in ((0.,-.01422), (side*width,-.01306)):
                    chunks.append('v %.7f %.7f %.7f\n' % (world_x-pivot_x,world_y+thickness+.012672,z-.063121))
        for z,width in OUTLINE:
            # Nondegenerate UVs stay inside a plain, opaque nearby belly patch.
            t = (z-OUTLINE[0][0])/(OUTLINE[-1][0]-OUTLINE[0][0])
            chunks.append('vt %.7f %.7f\nvt %.7f %.7f\n' % (uv_u-.00035,uv_v+(t-.5)*.0007,uv_u+.00035,uv_v+(t-.5)*.0007))
        # Opposing normals and faces permit the door to be seen while open.
        chunks.append('vn %.6f -0.993000 0.000000\n' % (side*.118))
        chunks.append('vn %.6f 0.993000 0.000000\n' % (-side*.118))
        def face(i,j,k,n,inside=False):
            return 'f '+' '.join('%d/%d/%d' % (v0+q+(len(OUTLINE)*2 if inside else 0),t0+q,n0+n) for q in (i,j,k))+'\n'
        for i in range(len(OUTLINE)-1):
            a,b,c,d=2*i+1,2*i+2,2*i+3,2*i+4
            tris=((a,b,d),(a,d,c)) if side==1 else ((a,d,b),(a,c,d))
            for p in tris:
                chunks.append(face(*p,1));chunks.append(face(p[2],p[1],p[0],2,True))
        counts['v'] += len(OUTLINE)*4
        counts['vt'] += len(OUTLINE)*2
        counts['vn'] += 2
    return ''.join(chunks)

def patch_aircraft(text):
    for old,new in zip(OLD,NAMES):
        pattern=r'(?ms)(^\['+old+r'\]\s*\n)(.*?)(?=^\[|\Z)'
        matches=list(re.finditer(pattern,text))
        if len(matches)!=1:
            raise ValueError('expected one section '+old)
        section=matches[0].group(2)
        values=re.findall(r'(?m)^Mesh=([^\r\n]*)',section)
        if values == [new]: continue
        if values != [old]: raise ValueError('unexpected '+old+' mesh')
        replacement=re.sub(r'(?m)^Mesh='+old+r'[ \t]*\r?$', 'Mesh='+new, section,count=1)
        text=text[:matches[0].start(2)]+replacement+text[matches[0].end(2):]
    return text
