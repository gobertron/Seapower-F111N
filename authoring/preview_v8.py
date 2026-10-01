#!/usr/bin/env python3
"""Render actual V8 assets and lettering; visual QA, not game execution."""
from PIL import Image,ImageDraw,ImageFont
from render_preview import scene,render
from paint_textures import FONT
from era_upgrade import ROOT,MOD,ROLES,unit_id
import argparse

def font(size):return ImageFont.truetype(FONT,size)

def contact_sheet():
    """Rebuild release branding from the existing native mesh-render panels."""
    contact=Image.new('RGB',(2240,2860),(233,237,240))
    for row,role in enumerate(ROLES):
        for col,year in enumerate((1995,2003)):
            with Image.open(ROOT/(unit_id(role,year)+'_preview.png')) as panel:
                contact.paste(panel.convert('RGB'),(col*1120,row*680))
    draw=ImageDraw.Draw(contact)
    draw.text((35,2752),'V8: eight dedicated 1995/2003 liveries; original UV geometry, transparency and mechanical atlas regions preserved.',font=font(21),fill=(45,62,71))
    draw.text((35,2795),'Paint approximates FS35237 / FS36320 / FS36375. Native asset render, not a Sea Power screenshot.',font=font(19),fill=(64,83,93))
    contact.save(ROOT/'RAN-F111N-USN-1995-2003-preview.png')
    contact.save(ROOT/'RAN-F111N-preview.png')

def main():
    contact=Image.new('RGB',(2240,2860),(233,237,240))
    sides=Image.new('RGB',(2240,2720),(233,237,240))
    choices={'f':'FleetIntercept','fb':'AntiShipLongRange','rf':'ReconLongRange','ef':'EWLongRange'}
    for row,(role,v) in enumerate(ROLES.items()):
        for col,year in enumerate((1995,2003)):
            uid=unit_id(role,year);print('Rendering',uid,flush=True)
            meshes=scene(uid,True,choices[role]);im=render(meshes);draw=ImageDraw.Draw(im)
            draw.text((30,25),f'{v[0]} {v[1]} - {year}',font=font(28),fill=(35,53,65))
            draw.text((30,68),f'USN-inspired tactical greys | Australian markings | Block {"III" if year==1995 else "IV"}',font=font(17),fill=(64,83,93))
            draw.text((30,642),'Shipped geometry; stock weapon meshes omitted; runtime untested',font=font(15),fill=(85,102,111))
            im.save(ROOT/(uid+'_preview.png'));contact.paste(im,(col*1120,row*680))
            profile=render(scene(uid,True,'Default'),transparent=True,side=True)
            profile=profile.crop(profile.getbbox());profile.thumbnail((751,206),Image.Resampling.LANCZOS)
            icon=Image.new('RGBA',(771,226));icon.alpha_composite(profile,((771-profile.width)//2,(226-profile.height)//2));icon.save(MOD/'ui/profiles'/(uid+'.png'))
            if year==2003:
                for n,eye in enumerate(([1.,.05,.02],[-1.,.05,.02])):
                    im=render(meshes,eye_vector=eye);draw=ImageDraw.Draw(im)
                    draw.text((30,25),f'{v[0]} 2003 - {"starboard" if n==0 else "port"} lettering',font=font(27),fill=(35,53,65));sides.paste(im,(n*1120,row*680))
    draw=ImageDraw.Draw(contact)
    draw.text((35,2752),'V8: eight dedicated 1995/2003 liveries; original UV geometry, transparency and mechanical atlas regions preserved.',font=font(21),fill=(45,62,71))
    draw.text((35,2795),'Paint approximates FS35237 / FS36320 / FS36375. Native asset render, not a Sea Power screenshot.',font=font(19),fill=(64,83,93))
    contact.save(ROOT/'RAN-F111N-USN-1995-2003-preview.png');contact.save(ROOT/'RAN-F111N-preview.png');sides.save(ROOT/'lettering_both_sides_V8.png')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contact-only',action='store_true')
    if parser.parse_args().contact_only:contact_sheet()
    else:main()
