#!/usr/bin/env python3
"""Generates the Rubik bitmap fonts used by the mod (fontfiles/*.fnt + *.png).

Only needed if you want to change the fonts or their size; the generated files are already
included in the repository and are copied into the mod by the "files" entry of mod.json.

    pip install pillow fonttools
    python tools/make_fonts.py

Output follows the layout Geode's own packager uses: <Name>.fnt/.png (standard quality),
<Name>-hd.* and <Name>-uhd.*, where every .fnt points at "<Name>.png" and GD adds the
quality suffix itself. The UHD font is rendered at SIZE px per em = SIZE/4 game points.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'fontfiles')
SIZE = 40                                   # px per em at ultra-high quality (= 10 points)
FONTS = {'Rubik': 'Rubik-Medium.ttf', 'RubikBold': 'Rubik-Bold.ttf'}
CHARSET = list(range(32, 127))              # printable ASCII
QUALITIES = [('-uhd', 1), ('-hd', 2), ('', 4)]   # suffix, size divisor
PAD = 2

def build(name, ttf_name, suffix, factor):
    ttf_path = os.path.join(HERE, 'fonts', ttf_name)
    px = SIZE // factor
    font = ImageFont.truetype(ttf_path, px, layout_engine=ImageFont.Layout.BASIC)
    tt = TTFont(ttf_path)
    upem = tt['head'].unitsPerEm
    hmtx = tt['hmtx']; cmap = tt.getBestCmap(); hhea = tt['hhea']
    line_height = round((hhea.ascent - hhea.descent + hhea.lineGap) * px / upem)
    base = round(hhea.ascent * px / upem)

    glyphs = []
    for cp in CHARSET:
        ch = chr(cp)
        adv = round(hmtx[cmap[cp]][0] * px / upem)
        l, t, r, b = font.getbbox(ch, anchor='ls')
        w, h = r - l, b - t
        img = None
        if w > 0 and h > 0:
            mask = Image.new('L', (w, h), 0)
            ImageDraw.Draw(mask).text((-l, -t), ch, font=font, anchor='ls', fill=255)
            img = mask
        glyphs.append(dict(id=cp, img=img, w=max(w, 0) if img else 0, h=max(h, 0) if img else 0,
                           xoff=l if img else 0, yoff=(px + t) if img else 0, adv=adv))

    # shelf packing
    width = max(64, 512 // factor)
    x = y = PAD; row_h = 0
    for g in sorted([g for g in glyphs if g['img']], key=lambda g: -g['h']):
        if x + g['w'] + PAD > width:
            x = PAD; y += row_h + PAD; row_h = 0
        g['x'], g['y'] = x, y
        x += g['w'] + PAD; row_h = max(row_h, g['h'])
    height = 1
    while height < y + row_h + PAD: height *= 2

    atlas = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    for g in glyphs:
        if g['img']:
            tile = Image.new('RGBA', g['img'].size, (255, 255, 255, 0)); tile.putalpha(g['img'])
            atlas.paste(tile, (g['x'], g['y']))
    atlas.save(os.path.join(OUT, f'{name}{suffix}.png'))

    lines = [
        f'info face="{ttf_name}" size={px} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=1,1',
        f'common lineHeight={line_height} base={base} scaleW={width} scaleH={height} pages=1 packed=0',
        f'page id=0 file="{name}.png"',
        f'chars count={len(glyphs)}',
    ]
    for g in sorted(glyphs, key=lambda g: g['id']):
        lines.append(f"char id={g['id']} x={g.get('x', 0)} y={g.get('y', 0)} width={g['w']} height={g['h']} "
                     f"xoffset={g['xoff']} yoffset={g['yoff']} xadvance={g['adv']} page=0 chnl=15")
    lines += ['kernings count=0', '']
    with open(os.path.join(OUT, f'{name}{suffix}.fnt'), 'w', newline='\n') as f:
        f.write('\n'.join(lines))
    return width, height, line_height

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, ttf in FONTS.items():
        for suffix, factor in QUALITIES:
            w, h, lh = build(name, ttf, suffix, factor)
            print(f'{name}{suffix}: {SIZE // factor}px em, atlas {w}x{h}, lineHeight {lh}')
