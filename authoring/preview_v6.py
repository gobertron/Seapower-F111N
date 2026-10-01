#!/usr/bin/env python3
"""Render V6 shipped geometry; this is visual QA, not a game execution."""
from PIL import Image,ImageDraw,ImageFont
from render_preview import scene,render
from paint_textures import FONT
from era_upgrade import ROOT,MOD,ROLES,unit_id

def main():
    panels=[]
    choices={'f':'AirToAir','fb':'PopeyeStrike','rf':'ReconLongRange','ef':'EscortSEAD'}
    descriptions={'f':'ASRAAM + AMRAAM | M61 configured','fb':'Popeye + control pod | bay preserved | M61 configured',
                  'rf':'2 ASRAAM + 4 tanks | Mach 3 | M61 configured','ef':'2 ECM pods + 2 offensive ECM | SEAD escort'}
    for role,v in ROLES.items():
        uid=unit_id(role,2003);print('Rendering',uid,flush=True)
        im=render(scene(uid,True,choices[role]));draw=ImageDraw.Draw(im)
        draw.text((30,25),v[0]+' '+v[1]+' - 2003',font=ImageFont.truetype(FONT,28),fill=(35,53,65))
        draw.text((30,68),descriptions[role],font=ImageFont.truetype(FONT,16),fill=(64,83,93))
        draw.text((30,642),'Shipped mesh preview; stock weapon bundles omitted; no runtime test',font=ImageFont.truetype(FONT,14),fill=(85,102,111))
        im.save(ROOT/(uid+'_preview.png'));panels.append(im)
    contact=Image.new('RGB',(2240,1420),(233,237,240))
    for i,im in enumerate(panels):contact.paste(im,((i%2)*1120,(i//2)*680))
    ImageDraw.Draw(contact).text((35,1384),'V6 - 1980 / 1985 / 1995 / 2003 editions - Original airframes and liveries preserved',font=ImageFont.truetype(FONT,21),fill=(45,62,71))
    contact.save(ROOT/'RAN-F111N-preview.png')

if __name__=='__main__':main()
