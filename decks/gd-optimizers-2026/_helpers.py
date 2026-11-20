# -*- coding: utf-8 -*-
import os, math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree

# ---------- palette ----------
BG      = RGBColor(0xF6, 0xF7, 0xFB)
DARK    = RGBColor(0x0B, 0x12, 0x20)
NAVY    = RGBColor(0x11, 0x18, 0x27)
TEXT    = RGBColor(0x0F, 0x17, 0x2A)
MUTED   = RGBColor(0x64, 0x74, 0x8B)
LINE    = RGBColor(0xE2, 0xE8, 0xF0)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
TEAL    = RGBColor(0x0D, 0x94, 0x88)
TEAL2   = RGBColor(0x14, 0xB8, 0xA6)
TEAL_L  = RGBColor(0xCC, 0xFB, 0xF1)
AMBER   = RGBColor(0xD9, 0x77, 0x06)
AMBER2  = RGBColor(0xF5, 0x9E, 0x0B)
AMBER_L = RGBColor(0xFE, 0xF3, 0xC7)
BLUE    = RGBColor(0x25, 0x63, 0xEB)
BLUE_L  = RGBColor(0xDB, 0xEA, 0xFE)
PURPLE  = RGBColor(0x7C, 0x3A, 0xED)
PURPLE_L= RGBColor(0xED, 0xE9, 0xFE)
RED     = RGBColor(0xDC, 0x26, 0x26)
RED_L   = RGBColor(0xFE, 0xE2, 0xE2)
GREEN   = RGBColor(0x05, 0x96, 0x69)
GREEN_L = RGBColor(0xD1, 0xFA, 0xE5)
SLATE   = RGBColor(0x94, 0xA3, 0xB8)
CARD    = RGBColor(0xFF, 0xFF, 0xFF)
FONT_EA = "Arial Unicode MS"
FONT_LAT = "Arial"

SW, SH = 13.333, 7.5

def rgb(hexstr):
    hexstr = hexstr.replace('#','')
    return RGBColor(int(hexstr[0:2],16), int(hexstr[2:4],16), int(hexstr[4:6],16))

def set_run_font(run, size=12, bold=False, color=TEXT, italic=False, ea=FONT_EA, latin=FONT_LAT):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = latin
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    # set East Asian font
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set('typeface', ea if tag == 'a:ea' else latin)

def add_text(slide, x, y, w, h, text, size=12, bold=False, color=TEXT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.05,
             margins=(0,0,0,0), font_ea=FONT_EA, font_lat=FONT_LAT, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    lines = text.split('\n') if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        set_run_font(r, size=size, bold=bold, color=color, italic=italic, ea=font_ea, latin=font_lat)
    return tb

def add_rich_text(slide, x, y, w, h, runs, size=12, color=TEXT, align=PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.TOP, line_spacing=1.05, margins=(0,0,0,0)):
    """runs: list of paragraphs; each paragraph list of (text, bold, color, size_override)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = line_spacing
        for item in para:
            txt, bold, col, sz = item
            r = p.add_run()
            r.text = txt
            set_run_font(r, size=(sz or size), bold=bold, color=(col or color))
    return tb

def add_rect(slide, x, y, w, h, fill=WHITE, line=None, line_w=1, radius=None,
             shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, transparency=None):
    shp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if transparency is not None:
            # alpha on solid fill
            spPr = shp.fill._xPr
            srgb = spPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
            alpha = etree.SubElement(srgb, qn('a:alpha')); alpha.set('val', str(int((1-transparency)*100000)))
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    if radius is not None and shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        try: shp.adjustments[0] = radius
        except Exception: pass
    return shp

def add_line(slide, x1, y1, x2, y2, color=LINE, width=1, dash=None):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    if dash: ln.line.dash_style = dash
    return ln

def add_circle(slide, x, y, d, fill=TEAL, line=None, line_w=1):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.shadow.inherit = False
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    return shp

def add_pill(slide, x, y, w, h, text, fill=TEAL_L, color=TEAL, size=9, bold=True):
    shp = add_rect(slide, x, y, w, h, fill=fill, line=None, radius=0.5)
    tf = shp.text_frame; tf.word_wrap=False; tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    set_run_font(r, size=size, bold=bold, color=color)
    return shp

def slide_bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid(); fill.fore_color.rgb = color

def header(slide, kicker, title, subtitle=None, page=None, source=None, accent=TEAL):
    slide_bg(slide)
    add_rect(slide, 0, 0, SW, 0.10, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(slide, 0.62, 0.33, 11.5, 0.25, kicker, size=9.5, bold=True, color=accent)
    add_text(slide, 0.62, 0.60, 11.9, 0.55, title, size=25, bold=True, color=TEXT, line_spacing=0.98)
    y = 1.16
    if subtitle:
        add_text(slide, 0.62, 1.12, 11.9, 0.32, subtitle, size=10.5, color=MUTED)
        y = 1.50
    add_line(slide, 0.62, y, 12.71, y, color=LINE, width=1)
    # footer
    add_line(slide, 0.62, 7.12, 12.71, 7.12, color=LINE, width=0.75)
    if source:
        add_text(slide, 0.62, 7.18, 10.9, 0.20, source, size=7.5, color=MUTED)
    if page is not None:
        add_text(slide, 12.20, 7.18, 0.5, 0.2, f"{page:02d}", size=8, bold=True, color=MUTED, align=PP_ALIGN.RIGHT)
    return y

def add_metric(slide, x, y, w, h, label, value, note='', accent=TEAL, fill=CARD, value_size=20):
    add_rect(slide, x, y, w, h, fill=fill, line=LINE, radius=0.08)
    add_rect(slide, x, y, 0.06, h, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(slide, x+0.18, y+0.10, w-0.28, 0.2, label, size=8.5, bold=True, color=MUTED)
    add_text(slide, x+0.18, y+0.29, w-0.28, 0.34, value, size=value_size, bold=True, color=TEXT)
    if note:
        add_text(slide, x+0.18, y+h-0.28, w-0.28, 0.2, note, size=8, color=MUTED)

def add_bullets(slide, x, y, w, h, items, size=11.5, color=TEXT, bullet_color=TEAL, gap=0.06):
    """items: list of (bold_prefix, rest) or plain str"""
    cur = y
    for it in items:
        add_circle(slide, x, cur+0.075, 0.075, fill=bullet_color, line=None)
        if isinstance(it, tuple):
            head, rest = it
            add_rich_text(slide, x+0.17, cur-0.02, w-0.17, 0.5,
                          [[(head, True, color, None), (rest, False, color, None)]],
                          size=size, color=color, line_spacing=1.12)
        else:
            add_text(slide, x+0.17, cur-0.02, w-0.17, 0.5, it, size=size, color=color, line_spacing=1.12)
        cur += gap + 0.44
    return cur

def add_label_value(slide, x, y, w, label, value, size=10):
    add_text(slide, x, y, w, 0.18, label, size=8, color=MUTED, bold=True)
    add_text(slide, x, y+0.18, w, 0.25, value, size=size, color=TEXT, bold=True)

def add_table(slide, x, y, w, h, data, col_widths, header_fill=NAVY, header_color=WHITE,
              body_size=9.5, header_size=9.5, row_height=0.34, first_col_bold=True,
              align=None, zebra=True):
    rows, cols = len(data), len(data[0])
    shp = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    table = shp.table
    for j, cw in enumerate(col_widths):
        table.columns[j].width = Inches(cw)
    for i in range(rows):
        table.rows[i].height = Inches(row_height)
        for j in range(cols):
            cell = table.cell(i, j)
            cell.margin_left = Inches(0.06); cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02); cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = (WHITE if (not zebra or i%2==1) else rgb('F8FAFC'))
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (align[j] if align else PP_ALIGN.LEFT)
            p.space_before=Pt(0); p.space_after=Pt(0)
            r = p.add_run(); r.text = str(data[i][j])
            set_run_font(r, size=(header_size if i==0 else body_size),
                         bold=(i==0 or (first_col_bold and j==0)),
                         color=(header_color if i==0 else TEXT))
    return table

def add_kpi_row(slide, y, items, x=0.62, total_w=12.05, gap=0.14, h=0.92):
    n = len(items)
    w = (total_w - gap*(n-1))/n
    for i, (label, value, note, color) in enumerate(items):
        add_metric(slide, x+i*(w+gap), y, w, h, label, value, note, accent=color)


