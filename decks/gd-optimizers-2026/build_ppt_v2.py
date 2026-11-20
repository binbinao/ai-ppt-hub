# -*- coding: utf-8 -*-
"""Build v2 of the optimizers teaching deck: larger type, more visuals (39 pages)."""
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

from _helpers import *  # noqa
from _helpers import (BG, DARK, NAVY, TEXT, MUTED, LINE, WHITE, TEAL, TEAL2,
                      AMBER, AMBER2, BLUE, PURPLE, RED, GREEN, SLATE, CARD,
                      SW, SH, add_text, add_rich_text, add_rect, add_line,
                      add_circle, add_pill, slide_bg, rgb)

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
MATH = "Times New Roman"
MONO = "Menlo"

M = 0.62
CW = 12.09
RIGHT = 12.71

CUR = [0]


def bump():
    CUR[0] += 1
    return CUR[0]


# ---------------------------------------------------------------- primitives
def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def header(s, kicker, title, subtitle=None, source=None, accent=TEAL):
    p = bump()
    slide_bg(s)
    add_rect(s, 0, 0, SW, 0.10, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, M, 0.32, 11.6, 0.26, kicker, size=11, bold=True, color=accent)
    add_text(s, M, 0.62, 11.9, 0.62, title, size=30, bold=True, color=TEXT, line_spacing=0.98)
    if subtitle:
        add_text(s, M, 1.19, 11.9, 0.34, subtitle, size=13.5, color=MUTED)
        y = 1.64
    else:
        y = 1.52
    add_line(s, M, y, RIGHT, y, color=LINE, width=1)
    add_line(s, M, 7.12, RIGHT, 7.12, color=LINE, width=0.75)
    if source:
        add_text(s, M, 7.17, 10.8, 0.22, source, size=9, color=MUTED)
    add_text(s, 12.05, 7.15, 0.66, 0.24, f"{p:02d}", size=9.5, bold=True,
             color=MUTED, align=PP_ALIGN.RIGHT)
    return p


def takeaway(s, text, accent=TEAL, y=6.40):
    add_rect(s, M, y, CW, 0.55, fill=WHITE, line=LINE, radius=0.10)
    add_rect(s, M, y, 0.08, 0.55, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, M + 0.22, y + 0.15, 0.62, 0.28, "记住", size=10.5, bold=True, color=accent)
    add_text(s, M + 0.86, y + 0.10, CW - 1.0, 0.38, text, size=13.5, color=TEXT)


def card(s, x, y, w, h, title=None, body=None, accent=TEAL, title_size=14.5,
         body_size=13, fill=CARD, title_color=TEXT, body_color=TEXT):
    add_rect(s, x, y, w, h, fill=fill, line=LINE, radius=0.06)
    add_rect(s, x, y, 0.07, h, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    ty = y + 0.16
    if title:
        add_text(s, x + 0.24, ty, w - 0.44, 0.32, title, size=title_size, bold=True,
                 color=title_color)
        ty += 0.40
    if body:
        add_text(s, x + 0.24, ty, w - 0.44, h - (ty - y) - 0.14, body, size=body_size,
                 color=body_color, line_spacing=1.18)


def math_run(p, text, size, italic=False, bold=False, color=TEXT, baseline=None):
    r = p.add_run()
    r.text = text
    f = r.font
    f.size = Pt(size)
    f.italic = italic
    f.bold = bold
    f.name = MATH
    f.color.rgb = color
    rPr = r._r.get_or_add_rPr()
    for tag, face in (("a:ea", "Arial Unicode MS"), ("a:cs", MATH)):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", face)
    if baseline is not None:
        rPr.set("baseline", str(baseline))


def add_math(s, x, y, w, h, paras, size=20, color=TEXT, align=PP_ALIGN.CENTER,
             line_spacing=1.32, anchor=MSO_ANCHOR.MIDDLE):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = line_spacing
        for text, opts in para:
            opts = opts or ""
            sz = size * (0.64 if ("sub" in opts or "sup" in opts) else 1.0)
            base = -22000 if "sub" in opts else (30000 if "sup" in opts else None)
            math_run(p, text, sz,
                     italic=("i" in opts and "sub" not in opts and "sup" not in opts),
                     bold=("b" in opts), color=color, baseline=base)
    return tb


def formula(s, x, y, w, h, paras, size=20, label=None, accent=TEAL, note=None,
            fill=CARD, align=PP_ALIGN.CENTER):
    add_rect(s, x, y, w, h, fill=fill, line=LINE, radius=0.05)
    add_rect(s, x, y, 0.06, h, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    top = y + 0.10
    if label:
        add_text(s, x + 0.24, top, w - 0.4, 0.24, label, size=10, bold=True, color=accent)
        top += 0.26
    bottom = y + h - (0.30 if note else 0.08)
    add_math(s, x + 0.24, top, w - 0.48, bottom - top, paras, size=size, align=align)
    if note:
        add_text(s, x + 0.24, y + h - 0.30, w - 0.44, 0.24, note, size=10, color=MUTED)


def bullets(s, x, y, w, items, size=13, gap=0.62, bullet_color=TEAL):
    cur = y
    for it in items:
        add_circle(s, x, cur + 0.10, 0.085, fill=bullet_color, line=None)
        if isinstance(it, tuple):
            head, rest = it
            add_rich_text(s, x + 0.22, cur, w - 0.22, gap - 0.06,
                          [[(head, True, TEXT, None), (rest, False, TEXT, None)]],
                          size=size, line_spacing=1.16)
        else:
            add_text(s, x + 0.22, cur, w - 0.22, gap - 0.06, it, size=size,
                     line_spacing=1.16)
        cur += gap
    return cur


ASPECT = {
    "fig_surface3d.png": 1.778, "fig_momentum.png": 1.480,
    "fig_adam_flow.png": 2.581, "fig_adamw.png": 2.332,
    "fig_spectrum.png": 2.604, "fig_compute.png": 2.579,
    "fig_lowrank.png": 2.682, "fig_adaptive.png": 2.328,
    "fig_traj.png": 1.328, "fig_lr.png": 1.500,
    "fig_bias.png": 1.909, "fig_descent.png": 1.617,
}


def figure(s, name, x, y, w, h, caption=None):
    r = ASPECT[name]
    if w / h > r:
        w2 = h * r
        x2 = x + (w - w2) / 2
        y2 = y
    else:
        w2 = w
        h2 = w / r
        x2 = x
        y2 = y + (h - h2) / 2
        h = h2
    s.shapes.add_picture(os.path.join(FIGS, name), Inches(x2), Inches(y2),
                         Inches(w2), Inches(h))
    if caption:
        add_text(s, x, y + h + 0.06, w, 0.28, caption, size=10.5, color=MUTED)


def caption(s, x, y, w, text):
    add_text(s, x, y, w, 0.28, text, size=10.5, color=MUTED)


def code_block(s, x, y, w, h, lines, size=12, title=None):
    add_rect(s, x, y, w, h, fill=NAVY, line=None, radius=0.04)
    top = y + 0.14
    if title:
        add_text(s, x + 0.2, y + 0.10, w - 0.3, 0.24, title, size=9.5, bold=True, color=SLATE)
        top = y + 0.40
    step = size * 1.42 / 72.0
    cur = top
    for item in lines:
        if isinstance(item, tuple):
            txt, col = item
            if isinstance(col, str):
                col = rgb(col)
        else:
            txt, col = item, rgb("E2E8F0")
        add_text(s, x + 0.2, cur, w - 0.32, step, txt, size=size, color=col,
                 font_ea=MONO, font_lat=MONO)
        cur += step


def table(s, x, y, w, data, col_widths, row_h=0.46, body=11, head=11.5,
          header_fill=NAVY, first_bold=True):
    rows, cols = len(data), len(data[0])
    shp = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w),
                             Inches(row_h * rows))
    t = shp.table
    for j, cw in enumerate(col_widths):
        t.columns[j].width = Inches(cw)
    for i in range(rows):
        t.rows[i].height = Inches(row_h)
        for j in range(cols):
            c = t.cell(i, j)
            c.margin_left = Inches(0.08)
            c.margin_right = Inches(0.08)
            c.margin_top = Inches(0.02)
            c.margin_bottom = Inches(0.02)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            c.fill.fore_color.rgb = header_fill if i == 0 else (
                WHITE if i % 2 == 1 else rgb("F8FAFC"))
            p = c.text_frame.paragraphs[0]
            p.space_before = Pt(0)
            p.space_after = Pt(0)
            r = p.add_run()
            r.text = str(data[i][j])
            from _helpers import set_run_font
            set_run_font(r, size=(head if i == 0 else body),
                         bold=(i == 0 or (first_bold and j == 0)),
                         color=(WHITE if i == 0 else TEXT))
    return t


# ---------------------------------------------------------------- 01 cover
def p_cover(s):
    bump()
    slide_bg(s, DARK)
    add_circle(s, 9.0, -2.0, 6.6, fill=rgb("13203A"), line=None)
    add_circle(s, 10.7, 0.4, 2.9, fill=None, line=TEAL, line_w=1)
    add_circle(s, 8.2, 5.2, 4.8, fill=rgb("0F1A2E"), line=None)
    add_rect(s, 0.72, 1.10, 0.07, 5.0, fill=TEAL, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, 1.0, 1.05, 8.4, 0.3, "教学讲义 · 深度学习优化器", size=12, bold=True, color=TEAL2)
    add_text(s, 0.98, 1.60, 10.7, 1.0, "从下山到矩阵几何", size=54, bold=True,
             color=WHITE, line_spacing=0.95)
    add_text(s, 1.0, 2.78, 10.9, 0.44,
             "梯度下降优化器的七十年：SGD → 动量 → Adam → AdamW → Muon", size=18,
             color=rgb("A8B6CC"))
    add_text(s, 1.0, 3.56, 10.4, 1.1,
             "为什么 Adam 解决了「每个坐标走多大」，\n"
             "AdamW 解决了「正则被谁绑架」，\n"
             "Muon 又为什么盯上了矩阵的奇异值。",
             size=15, color=rgb("CBD5E1"), line_spacing=1.4)
    labels = [("Adam", "2015 · 逐坐标自适应", TEAL), ("AdamW", "2019 · 解耦正则", BLUE),
              ("Muon", "2024 · 矩阵几何", AMBER)]
    for i, (name, sub, col) in enumerate(labels):
        x = 1.0 + i * 3.35
        add_rect(s, x, 5.55, 3.05, 0.92, fill=rgb("0F1A2E"), line=col, radius=0.18)
        add_circle(s, x + 0.2, 5.84, 0.34, fill=col, line=None)
        add_text(s, x + 0.66, 5.62, 2.2, 0.3, name, size=15, bold=True, color=WHITE)
        add_text(s, x + 0.66, 5.98, 2.3, 0.26, sub, size=10.5, color=rgb("94A3B8"))
    add_line(s, 1.0, 6.80, 12.0, 6.80, color=rgb("243247"), width=0.75)
    add_text(s, 1.0, 6.90, 7.0, 0.26, "39 页 · 含可复现 Toy 实验与选型清单", size=10.5,
             color=rgb("7C8BA3"))
    add_text(s, 8.0, 6.90, 4.0, 0.26, "关键数字均标注一手来源", size=10.5,
             color=rgb("7C8BA3"), align=PP_ALIGN.RIGHT)
    notes(s, "开场只讲训练里的那一行代码：优化器。先给结论——Adam、AdamW、Muon 分别在解决方向、"
             "尺度、几何三个层次的问题；全程配可复现的 toy 实验和论文里的真实数字。")


# ---------------------------------------------------------------- 02 three questions
def p_questions(s):
    header(s, "导读", "先回答三个问题", "如果这三个问题你都有答案，可以直接跳到第 13 页",
           source="本讲整理")
    qs = [
        ("同一个模型，换个优化器，训练曲线为什么完全不同？",
         "方向、步长、记忆——三个旋钮。"),
        ("Adam 已经「自适应」了，为什么还需要 AdamW？",
         "因为 L2 正则和 weight decay 在 Adam 下不是一回事。"),
        ("Muon 只改了更新方向，为什么能省 2 倍算力？",
         "因为它把「逐元素缩放」换成了「矩阵谱上的正交化」。"),
    ]
    for i, (q, a) in enumerate(qs):
        y = 1.84 + i * 1.44
        add_rect(s, M, y, 7.45, 1.28, fill=CARD, line=LINE, radius=0.06)
        add_circle(s, M + 0.20, y + 0.18, 0.36, fill=TEAL, line=None)
        add_text(s, M + 0.20, y + 0.24, 0.36, 0.26, str(i + 1), size=12, bold=True,
                 color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, M + 0.72, y + 0.14, 6.5, 0.62, q, size=14.5, bold=True,
                 color=TEXT, line_spacing=1.12)
        add_text(s, M + 0.72, y + 0.84, 6.5, 0.3, a, size=13, color=MUTED)
    add_rect(s, 8.30, 1.84, 4.41, 4.20, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 8.55, 2.00, 4.0, 0.3, "本讲路线", size=11, bold=True, color=MUTED)
    route = [("01", "下山与随机化", TEAL), ("02", "加速：方向", BLUE),
             ("03", "自适应：尺度", PURPLE), ("04", "解耦正则", AMBER),
             ("05", "矩阵几何", RED)]
    for i, (n, name, col) in enumerate(route):
        y = 2.46 + i * 0.70
        add_text(s, 8.55, y, 0.55, 0.3, n, size=12, bold=True, color=col)
        add_text(s, 9.15, y - 0.03, 3.3, 0.32, name, size=14, bold=True, color=TEXT)
        add_line(s, 8.55, y + 0.44, 12.45, y + 0.44, color=LINE, width=0.6)
    takeaway(s, "优化器在解三个层次的问题：方向、尺度、几何。", accent=TEAL)
    notes(s, "三个问题就是全篇骨架：第一个引出动量与自适应，第二个引出 AdamW，第三个引出 Muon。"
             "先别记公式，记住每一代在补哪个洞。")


# ---------------------------------------------------------------- 03 paradigms
def p_paradigms(s):
    header(s, "全景", "七十年，四次范式转移", "每一次都不是推翻前一个，而是补上它看不见的维度",
           source="本讲整理；代表工作见第 36 页时间线", accent=TEAL)
    add_line(s, 1.0, 3.62, 12.30, 3.62, color=LINE, width=2)
    items = [
        ("1951–1985", "随机化", "用带噪声的小批量梯度\n代替全量梯度", "Robbins–Monro 1951 · LMS 1960", TEAL),
        ("1964–2000", "加速", "记住过去的方向\n抵消锯齿、冲出峡谷", "Polyak 1964 · Nesterov 1983", BLUE),
        ("2011–2017", "自适应", "每个坐标有自己的\n有效步长", "AdaGrad 2011 · Adam 2015", PURPLE),
        ("2017–now", "结构化", "解耦正则；直接对\n矩阵的谱做预条件", "AdamW 2019 · Muon 2024", AMBER),
    ]
    for i, (era, name, idea, rep, col) in enumerate(items):
        cx = 1.75 + i * 3.28
        add_circle(s, cx - 0.13, 3.49, 0.26, fill=col, line=WHITE, line_w=2)
        above = (i % 2 == 0)
        if above:
            add_text(s, cx - 1.45, 1.92, 2.9, 0.26, era, size=11.5, bold=True, color=col,
                     align=PP_ALIGN.CENTER)
            add_text(s, cx - 1.45, 2.20, 2.9, 0.44, name, size=23, bold=True, color=TEXT,
                     align=PP_ALIGN.CENTER)
            add_text(s, cx - 1.45, 2.72, 2.9, 0.7, idea, size=13, color=MUTED,
                     align=PP_ALIGN.CENTER, line_spacing=1.2)
            add_line(s, cx, 3.42, cx, 3.30, color=col, width=1.2)
        else:
            add_text(s, cx - 1.45, 3.84, 2.9, 0.26, era, size=11.5, bold=True, color=col,
                     align=PP_ALIGN.CENTER)
            add_text(s, cx - 1.45, 4.12, 2.9, 0.44, name, size=23, bold=True, color=TEXT,
                     align=PP_ALIGN.CENTER)
            add_text(s, cx - 1.45, 4.64, 2.9, 0.7, idea, size=13, color=MUTED,
                     align=PP_ALIGN.CENTER, line_spacing=1.2)
            add_line(s, cx, 3.82, cx, 3.72, color=col, width=1.2)
        add_text(s, cx - 1.55, 5.52, 3.1, 0.3, rep, size=10.5, color=SLATE,
                 align=PP_ALIGN.CENTER)
    takeaway(s, "历史不是替代，而是不断把「一个标量步长」拆成方向、坐标与矩阵几何。", accent=AMBER)
    notes(s, "四次转移可以一句话串起来：先让噪声下也能收敛，再让方向更聪明，再让每个坐标有自己的步长，"
             "最后把正则和矩阵几何单独拿出来。时间有重叠，范式不是替代关系。")


# ---------------------------------------------------------------- 04 why
def p_why(s):
    header(s, "动机", "换一行代码，账单差一倍", "优化器不改模型结构、不改数据，却直接改变 token 效率与算力成本",
           source="Jordan 2024；Moonshot 2025；NanoGPT speedrun 记录", accent=TEAL)
    stats = [("NanoGPT 训练加速", "1.35×", "Muon vs 调好的 AdamW", TEAL),
             ("compute-optimal 效率", "约 2×", "Moonshot 3B/16B MoE 对比", AMBER),
             ("CIFAR-10 speedrun", "3.3→2.6", "A100-seconds，94% 精度", BLUE)]
    for i, (label, value, note_, col) in enumerate(stats):
        x = M + i * 4.03
        add_rect(s, x, 1.84, 3.86, 1.38, fill=CARD, line=LINE, radius=0.07)
        add_rect(s, x, 1.84, 0.07, 1.38, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, x + 0.24, 1.96, 3.4, 0.26, label, size=10.5, bold=True, color=MUTED)
        add_text(s, x + 0.24, 2.22, 3.3, 0.5, value, size=30, bold=True, color=TEXT)
        add_text(s, x + 0.24, 2.86, 3.4, 0.24, note_, size=10.5, color=MUTED)
    add_text(s, M, 3.46, 6.9, 0.32, "为什么这一行值钱", size=15, bold=True, color=TEXT)
    bullets(s, M, 3.90, 7.0, [
        ("训练成本 ∝ 步数 × 每步算力。", "收敛快 = 步数少，优化器同时影响两者。"),
        ("它不动架构，是「免费」收益。", "但换优化器通常要重调 lr / wd / warmup。"),
        ("失败模式更隐蔽。", "不收敛、loss spike、泛化变差，可能几十亿 token 后才暴露。"),
    ], size=13, gap=0.70)
    add_rect(s, 7.95, 3.46, 4.76, 2.58, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 8.20, 3.62, 4.3, 0.3, "算一笔粗账", size=11, bold=True, color=AMBER)
    add_text(s, 8.20, 4.02, 4.28, 1.9,
             "一次前沿模型的预训练，算力账单以千万美元计。\n"
             "10% 的训练效率差，就是数百万美元量级的差别；\n"
             "若因此多跑一次失败的大规模实验，代价还要翻倍。\n\n"
             "所以工业界选优化器，远比论文里的「快几个点」谨慎。",
             size=13, color=MUTED, line_spacing=1.32)
    takeaway(s, "优化器是训练里性价比最高、也最容易被低估的一行代码。", accent=TEAL)
    notes(s, "三个数字代表三种证据：小规模 speedrun、规模化 compute-optimal、社区复现记录。"
             "2× 是特定设定下的结论，不是任何场景都 2×。")


# ---------------------------------------------------------------- 05 hero descent
def p_hero(s):
    bump()
    slide_bg(s, DARK)
    s.shapes.add_picture(os.path.join(FIGS, "fig_surface3d.png"), Inches(0), Inches(0),
                         Inches(SW), Inches(SH))
    add_rect(s, 0, 0, 4.45, SH, fill=DARK, line=None, shape_type=MSO_SHAPE.RECTANGLE,
             transparency=0.12)
    add_text(s, 0.75, 1.05, 4.0, 0.3, "直觉", size=12, bold=True, color=TEAL2)
    add_text(s, 0.75, 1.45, 4.1, 1.3, "训练就是下山", size=36, bold=True, color=WHITE,
             line_spacing=0.98)
    add_text(s, 0.75, 2.28, 4.1, 0.6, "但山是 10⁹ 维的", size=26, color=TEAL2)
    add_text(s, 0.75, 3.15, 4.15, 2.4,
             "你站在山坡上，看不见全局，\n只能摸到脚下的坡度。\n\n"
             "每一步只决定三件事：\n往哪走、走多远、\n记不记得来时的路。\n\n"
             "优化器的全部历史，就是在这三个问题上\n不断加入更多信息。",
             size=13.5, color=rgb("CBD5E1"), line_spacing=1.42)
    add_text(s, 4.6, 6.82, 8.4, 0.26, "示意：二维损失曲面上的梯度下降轨迹", size=10,
             color=rgb("64748B"), align=PP_ALIGN.RIGHT)
    notes(s, "这一页只建立直觉：高维损失面看不见全局，只能靠局部梯度。三个决定——方向、步长、记忆——"
             "后面每个算法都在补其中一个。")


# ---------------------------------------------------------------- 06 three lines
def p_history(s):
    header(s, "历史", "三条线在 1986 年汇合", "能算梯度、能在噪声下收敛、知道怎么下降——深度学习才真正开始",
           source="Cauchy 1847；Robbins & Monro 1951；Rumelhart et al. 1986", accent=TEAL)
    items = [
        ("1847", "Cauchy：最速下降", "证明负梯度是局部最速方向。\n但每步都要算全量梯度。", TEAL),
        ("1951", "Robbins–Monro：随机近似", "梯度带噪声也能收敛。\nSGD 的理论地基。", BLUE),
        ("1986", "反向传播：梯度可算", "第一次能高效算出\n上百万维参数的梯度。", PURPLE),
    ]
    add_line(s, 1.0, 2.30, 12.3, 2.30, color=LINE, width=2)
    for i, (year, title, body, col) in enumerate(items):
        x = M + i * 4.03
        cx = x + 1.85
        add_circle(s, cx - 0.11, 2.19, 0.22, fill=col, line=WHITE, line_w=2)
        add_text(s, x, 2.50, 3.6, 0.7, year, size=40, bold=True, color=col)
        add_text(s, x, 3.25, 3.6, 0.62, title, size=16, bold=True, color=TEXT, line_spacing=1.1)
        add_text(s, x, 4.00, 3.55, 1.5, body, size=13, color=MUTED, line_spacing=1.35)
    add_text(s, M, 5.62, 12.0, 0.36, "三条线各自解决一个必要条件，缺一个都跑不起来。",
             size=14, color=TEXT)
    takeaway(s, "深度学习的起点，不是某个模型，而是「梯度终于算得动」这件事。", accent=TEAL)
    notes(s, "1847 给了方向，1951 给了噪声下的收敛保证，1986 给了计算可行性。"
             "三条线在 1986 年汇合，才有今天的大规模训练。")


# ---------------------------------------------------------------- 07 SGD troubles
def p_sgd(s):
    header(s, "SGD", "两个麻烦：噪声与曲率", "一个来自「看不清」，一个来自「地形歪」",
           source="本讲整理；条件数示例见下页实验", accent=TEAL)
    blocks = [
        ("σ", "噪声：小批量 ≠ 全量", "小批量梯度是全量梯度的有偏估计。\n方差让更新抖动，最后一段在最小值\n附近来回打转，收敛慢。", BLUE),
        ("κ", "曲率：等高线是峡谷", "条件数 κ 大时，同一个标量 lr\n对一个方向太大、对另一个太小；\n只能取折中，于是来回撞墙。", AMBER),
    ]
    for i, (glyph, title, body, col) in enumerate(blocks):
        x = M + i * 6.14
        add_rect(s, x, 1.86, 5.95, 3.55, fill=CARD, line=LINE, radius=0.06)
        add_rect(s, x, 1.86, 0.07, 3.55, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, x + 0.28, 1.98, 1.2, 1.0, glyph, size=54, bold=True, color=col)
        add_text(s, x + 1.35, 2.14, 4.3, 0.36, title, size=17, bold=True, color=TEXT)
        add_text(s, x + 1.35, 2.66, 4.35, 2.4, body, size=13, color=MUTED, line_spacing=1.45)
    add_text(s, M, 5.66, 12.0, 0.36,
             "两个麻烦对应两条技术路线：降噪（动量 / 平均）与预条件（逐坐标 / 矩阵）。",
             size=13.5, color=TEXT)
    takeaway(s, "SGD 的两个麻烦，正好是后面所有优化器的两个研究方向。", accent=TEAL)
    notes(s, "噪声来自随机采样，曲率来自损失面的各向异性。后面动量降噪，AdaGrad/Adam 做逐坐标预条件，"
             "Muon 做矩阵级预条件。")


# ---------------------------------------------------------------- 08 canyon
def p_canyon(s):
    header(s, "实验 1", "峡谷里，SGD 来回撞墙", "同一个二次函数，三种优化器各自网格搜索学习率，降到初始损失的 1e-6",
           source="本讲 Toy 实验：f(θ)=½(θ₁²+100θ₂²)，40 点 lr 网格", accent=TEAL)
    figure(s, "fig_traj.png", M, 1.80, 7.15, 4.30)
    add_text(s, 8.05, 1.90, 4.6, 0.32, "读图", size=11, bold=True, color=TEAL)
    bullets(s, 8.05, 2.30, 4.55, [
        ("SGD 263 步。", "在狭长方向反复过冲，只能靠小 lr 稳住。"),
        ("动量 90 步。", "沿长轴积累速度，抵消横向锯齿。"),
        ("Adam 83 步。", "逐坐标缩放，两个方向各走各的。"),
    ], size=13, gap=0.86)
    add_text(s, 8.05, 5.05, 4.55, 0.9,
             "条件数 κ=100：横轴曲率是纵轴的 100 倍。\n同一个标量步长不可能同时适配两边。",
             size=11.5, color=MUTED, line_spacing=1.3)
    takeaway(s, "曲率不是细节，它决定了「逐坐标」为什么重要。", accent=AMBER)
    notes(s, "轴对齐的二次函数已经对 SGD 最友好；把峡谷旋转 25° 后，逐坐标自适应的优势会变窄，"
             "这正是 Muon 的出发点。三种优化器各自做了 40 点 lr 网格搜索，比较的是各自最好成绩。")


# ---------------------------------------------------------------- 09 lr robustness
def p_lr(s):
    header(s, "实验 2", "Adam 的鲁棒，是归一化换来的", "固定 200 步，扫描学习率：SGD 稳定到 0.019，动量到 0.037，Adam 全区间可训",
           source="本讲 Toy 实验：lr ∈ geomspace(0.001, 3.0, 55)", accent=TEAL)
    figure(s, "fig_lr.png", M, 1.84, 7.35, 4.25)
    add_text(s, 8.25, 1.94, 4.4, 0.32, "三个区间", size=11, bold=True, color=TEAL)
    rows = [("SGD", "0.001 – 0.019", SLATE), ("动量", "0.001 – 0.037", BLUE),
            ("Adam", "0.001 – 3.0", TEAL)]
    for i, (name, rng, col) in enumerate(rows):
        y = 2.38 + i * 0.78
        add_text(s, 8.25, y, 1.0, 0.3, name, size=14, bold=True, color=col)
        add_text(s, 9.20, y, 3.4, 0.3, rng, size=14, color=TEXT)
    add_text(s, 8.25, 4.86, 4.4, 1.2,
             "Adam 把更新除以 √v̂，相当于给每个坐标\n配了自动增益：梯度大就压，梯度小就抬。\n"
             "代价是它可能把「有用的陡峭方向」也压平。",
             size=11.5, color=MUTED, line_spacing=1.32)
    takeaway(s, "鲁棒性不是免费的：归一化拿掉了「步长要随曲率调」这件事，也拿掉了部分信息。", accent=TEAL)
    notes(s, "55 个学习率、每个跑 200 步，看最终损失是否发散。Adam 在整个区间都能训，"
             "这就是它在工业界成为默认选项的工程原因。")


# ---------------------------------------------------------------- divider
def divider(s, num, era, title, sub, accent):
    bump()
    slide_bg(s, DARK)
    add_circle(s, 8.4, -2.4, 7.0, fill=rgb("111C30"), line=None)
    add_circle(s, 10.2, 3.0, 4.4, fill=None, line=accent, line_w=1)
    add_text(s, 8.82, 0.9, 3.9, 2.6, num, size=150, bold=True, color=rgb("1A2A40"))
    add_text(s, 0.95, 2.05, 6.0, 0.34, era, size=15, bold=True, color=accent)
    add_text(s, 0.92, 2.48, 7.55, 1.2, title, size=42, bold=True, color=WHITE, line_spacing=1.02)
    add_rect(s, 0.95, 3.78, 1.1, 0.06, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, 0.95, 4.02, 7.2, 0.6, sub, size=15, color=rgb("A8B6CC"))
    notes(s, f"章节过渡：{title}。{sub}")


# ---------------------------------------------------------------- 10 momentum
def p_momentum(s):
    header(s, "加速", "动量：让方向记住历史", "不是每一步都重新决策，而是把过去几步的方向累积起来",
           source="Polyak 1964；Nesterov 1983", accent=BLUE)
    figure(s, "fig_momentum.png", M, 1.92, 5.7, 3.55)
    formula(s, 6.55, 1.90, 6.16, 1.32, [
        [("v", "i"), ("t", "sub"), (" = β v", ""), ("t−1", "sub"), (" + g", ""), ("t", "sub")],
        [("θ", "i"), ("t", "sub"), (" = θ", ""), ("t−1", "sub"), (" − η v", ""), ("t", "sub")],
    ], size=21, label="heavy-ball 动量", accent=BLUE)
    bullets(s, 6.55, 3.50, 6.1, [
        ("抵消锯齿。", "横向分量正负抵消，纵向分量累积。"),
        ("β=0.9 ≈ 记住 10 步。", "等效学习率放大 1/(1−β) 倍。"),
        ("Nesterov 更进一步。", "先在预判点取梯度，再看要不要修正。"),
    ], size=13, gap=0.85, bullet_color=BLUE)
    takeaway(s, "动量把「历史」变成方向信息：这一步不只由当前梯度决定。", accent=BLUE)
    notes(s, "动量解决的是「方向抖」；它并不改变每个坐标的尺度。Nesterov 的区别是先按动量走一步，"
             "在预判点算梯度，相当于带前瞻的修正。")


# ---------------------------------------------------------------- 11 adagrad
def p_adagrad(s):
    header(s, "自适应", "AdaGrad：给每个坐标一根尺子", "梯度大的坐标走小步，梯度小的坐标走大步——第一次把「逐坐标」写进更新式",
           source="Duchi, Hazan & Singer 2011, JMLR", accent=PURPLE)
    formula(s, M, 1.82, CW, 1.12, [
        [("G", "i"), ("t", "sub"), (" = G", ""), ("t−1", "sub"), (" + g", ""), ("t", "sub"), ("²", "sup"),
         ("        θ", "i"), ("t", "sub"), (" = θ", ""), ("t−1", "sub"), (" − η g", ""), ("t", "sub"),
         (" / √(G", ""), ("t", "sub"), (" + ε)", "")],
    ], size=19, label="AdaGrad", accent=PURPLE)
    figure(s, "fig_adaptive.png", M, 3.12, 6.35, 2.72)
    add_text(s, 7.25, 3.18, 5.4, 0.3, "两坐标，同一个 η", size=11, bold=True, color=PURPLE)
    bullets(s, 7.25, 3.58, 5.3, [
        ("分母是历史平方和。", "每个坐标独立累积，互不影响。"),
        ("稀疏特征受益。", "很少出现的特征，分母小、步长大。"),
        ("致命缺点。", "G 单调增 → 步长终将衰减到 0。"),
    ], size=13, gap=0.82, bullet_color=PURPLE)
    takeaway(s, "AdaGrad 提出了正确的问题：步长应该逐坐标；但「记一辈子」不是答案。", accent=PURPLE)
    notes(s, "这张图是示意：两个坐标梯度相差 10 倍，有效步长也相差约 10 倍。"
             "AdaGrad 的问题在非平稳目标上尤其明显——学习率会过早衰减。")


# ---------------------------------------------------------------- 12 rmsprop
def p_rmsprop(s):
    header(s, "自适应", "RMSProp：把「一辈子」换成「一阵子」", "用指数滑动平均代替累加，非平稳目标也能跟得上",
           source="Hinton 2012 Coursera 讲义（未正式发表）", accent=PURPLE)
    formula(s, M, 1.82, CW, 1.12, [
        [("E[g²]", "i"), ("t", "sub"), (" = ρ E[g²]", ""), ("t−1", "sub"),
         (" + (1−ρ) g", ""), ("t", "sub"), ("²", "sup"),
         ("        θ", "i"), ("t", "sub"), (" = θ", ""), ("t−1", "sub"),
         (" − η g", ""), ("t", "sub"), (" / √(E[g²]", ""), ("t", "sub"), (" + ε)", "")],
    ], size=19, label="RMSProp", accent=PURPLE)
    # EMA weight bars
    add_text(s, M, 3.20, 5.6, 0.3, "ρ=0.9 时，历史权重的记忆长度", size=11, bold=True, color=PURPLE)
    for i in range(12):
        h = 0.10 + 1.55 * (0.9 ** i)
        add_rect(s, M + 0.05 + i * 0.42, 4.95 - h, 0.28, h, fill=TEAL if i < 3 else rgb("CBD5E1"),
                 line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, M, 5.06, 5.4, 0.28, "越近的梯度权重越大；大约 10 步后衰减到 1/e", size=10, color=MUTED)
    bullets(s, 6.55, 3.20, 6.1, [
        ("忘记过去。", "不累积全部历史，只保留最近一段。"),
        ("适合非平稳目标。", "损失面在训练中一直在变。"),
        ("留下一个旋钮。", "ρ 控制记忆长度，0.9 是常见默认。"),
    ], size=13, gap=0.86, bullet_color=PURPLE)
    takeaway(s, "RMSProp 修好了 AdaGrad 的「步长归零」，但还没有修「冷启动」。", accent=PURPLE)
    notes(s, "RMSProp 从未正式发表，但在实践中几乎无处不在。它和动量结合，就是 Adam。")


# ---------------------------------------------------------------- 13 adam
def p_adam(s):
    header(s, "Adam", "两条滑动平均，各修一个毛病", "动量修方向，二阶矩修尺度，偏差修正修冷启动",
           source="Kingma & Ba, ICLR 2015；默认 β₁=0.9, β₂=0.999, ε=1e-8, lr=1e-3", accent=TEAL)
    figure(s, "fig_adam_flow.png", 0.95, 1.88, 11.45, 3.72)
    add_text(s, M, 5.86, 12.0, 0.34,
             "m̂ 和 v̂ 分别除以 (1−βᵗ)：训练初期 EMA 从 0 起步，不修就会系统性偏小。",
             size=13, color=MUTED)
    takeaway(s, "Adam = 动量（方向）+ RMSProp（尺度）+ 偏差修正（冷启动）。", accent=TEAL)
    notes(s, "这张图是 Adam 的全部计算图。注意两条 EMA 是并行的，最后在更新式里汇合。"
             "默认超参在 Transformer 时代几乎成了通用起点。")


# ---------------------------------------------------------------- 14 bias
def p_bias(s):
    header(s, "Adam", "为什么除以 1−βᵗ", "偏差修正不是「提高精度」，而是修掉从 0 起步的系统性偏差",
           source="Kingma & Ba 2015, §3", accent=TEAL)
    figure(s, "fig_bias.png", M, 1.95, 6.0, 3.14)
    formula(s, 6.95, 1.95, 5.75, 1.55, [
        [("m̂", "i"), ("t", "sub"), (" = m", ""), ("t", "sub"), (" / (1 − β₁", ""), ("t", "sup"), (")", "")],
        [("v̂", "i"), ("t", "sub"), (" = v", ""), ("t", "sub"), (" / (1 − β₂", ""), ("t", "sup"), (")", "")],
    ], size=20, label="偏差修正", accent=TEAL)
    add_rect(s, 6.95, 3.70, 5.75, 1.90, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 7.18, 3.84, 5.3, 0.3, "t=1 时会发生什么", size=11, bold=True, color=AMBER)
    add_text(s, 7.18, 4.20, 5.3, 1.3,
             "m₁=0.1g，v₁=0.001g² → m₁/√v₁ ≈ 3.16·sign(g)\n"
             "除以 (1−β₁)、(1−β₂) 后回到 1·sign(g)。\n"
             "不修：第一步就会走过头约 3 倍。",
             size=12, color=TEXT, line_spacing=1.35)
    takeaway(s, "偏差修正修的是「冷启动」，不是精度；它让第一步就可信。", accent=TEAL)
    notes(s, "t=1 的算术很直观：EMA 只见到一个梯度，估计值只有真实值的 1−β。"
             "修正后第一步的更新幅度和后续一致，避免 warmup 之前就炸掉。")


# ---------------------------------------------------------------- 15 what Adam solved
def p_solved(s):
    header(s, "小结", "Adam 之后，还剩什么", "它把「方向」和「逐坐标尺度」都做到了极致，但没有回答「正则」和「矩阵」",
           source="本讲整理", accent=TEAL)
    layers = [
        ("方向", "动量 / Nesterov", "Adam 已具备", TEAL, True),
        ("尺度", "AdaGrad / RMSProp", "Adam 逐坐标做到极致", BLUE, True),
        ("几何", "矩阵谱 / 正交化", "Adam 看不见", AMBER, False),
    ]
    for i, (name, methods, status, col, done) in enumerate(layers):
        y = 1.95 + i * 1.36
        add_rect(s, M, y, CW, 1.12, fill=CARD, line=(col if not done else LINE),
                 line_w=(1.6 if not done else 1), radius=0.06)
        add_text(s, M + 0.28, y + 0.30, 1.4, 0.4, name, size=20, bold=True, color=col)
        add_text(s, M + 1.75, y + 0.18, 4.6, 0.34, methods, size=14, bold=True, color=TEXT)
        add_text(s, M + 1.75, y + 0.60, 4.8, 0.3,
                 "这一层已经被解决" if done else "这一层还没有被解决", size=11, color=MUTED)
        add_text(s, 9.0, y + 0.32, 3.4, 0.4, status, size=15, bold=True, color=col,
                 align=PP_ALIGN.RIGHT)
    add_text(s, M, 6.02, 12.0, 0.3,
             "下一步的两条路：把正则从梯度里拿出来（AdamW），或直接对矩阵的谱做预条件（Muon）。",
             size=13, color=MUTED)
    takeaway(s, "Adam 之后，问题从「每个坐标」转移到「正则」与「矩阵结构」。", accent=AMBER)
    notes(s, "这一页是全篇的转折。前两层 Adam 做得很好，所以 AdamW 不在更新式上改，而在正则上改；"
             "Muon 则换了一个空间——矩阵的谱。")


# ---------------------------------------------------------------- 16 two crises
def p_crises(s):
    header(s, "Adam 的两次危机", "一次说它泛化差，一次说它不收敛", "两次都没有杀死 Adam，但都指出了「自适应」的盲区",
           source="Wilson et al. 2017；Reddi et al. 2018", accent=RED)
    blocks = [
        ("危机 1 · 泛化", "Wilson et al. 2017",
         "主张：自适应方法在测试集上泛化更差。\n"
         "证据：小数据、toy 任务上 SGD 胜出。\n"
         "后续：调好 wd / lr 后差距大幅缩小；\n这不是定论，但提醒了「自适应 ≠ 更好」。", BLUE),
        ("危机 2 · 收敛", "Reddi et al. 2018",
         "主张：Adam 可能不收敛（构造反例）。\n"
         "原因：二阶矩 EMA 可能让有效步长变大。\n"
         "修复：AMSGrad 用 max(v) 保证步长非增。\n"
         "代价：可能过保守，工业界更常用调好的 AdamW。", RED),
    ]
    for i, (title, who, body, col) in enumerate(blocks):
        x = M + i * 6.14
        add_rect(s, x, 1.86, 5.95, 3.95, fill=CARD, line=LINE, radius=0.06)
        add_rect(s, x, 1.86, 0.07, 3.95, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, x + 0.28, 2.02, 5.4, 0.38, title, size=18, bold=True, color=col)
        add_text(s, x + 0.28, 2.46, 5.4, 0.3, who, size=11, color=MUTED)
        add_text(s, x + 0.28, 2.90, 5.4, 2.7, body, size=13, color=TEXT, line_spacing=1.5)
    takeaway(s, "两次危机暴露的是同一件事：逐坐标自适应，看不到「全局」与「谱」。", accent=RED)
    notes(s, "Wilson 的结论在社区里争议很大，关键在调参预算是否公平。Reddi 的反例是构造性的，"
             "AMSGrad 修好了收敛性，但工程上很少直接用。")


# ---------------------------------------------------------------- 17 amsgrad
def p_amsgrad(s):
    header(s, "修复", "AMSGrad：给分母加一个「不降」约束", "保证有效步长不增，从而拿到收敛保证——代价是可能过保守",
           source="Reddi, Kale & Kumar, ICLR 2018", accent=RED)
    formula(s, M, 1.90, CW, 1.55, [
        [("v̂", "i"), ("t", "sub"), (" = max(v̂", ""), ("t−1", "sub"), (", v", ""), ("t", "sub"), (")", "")],
        [("θ", "i"), ("t", "sub"), (" = θ", ""), ("t−1", "sub"), (" − η m", ""), ("t", "sub"),
         (" / (√v̂", ""), ("t", "sub"), (" + ε)", "")],
    ], size=22, label="AMSGrad", accent=RED)
    bullets(s, M, 3.80, 12.0, [
        ("分母非降 → 有效步长非增。", "这是收敛证明需要的单调性。"),
        ("代价是可能过保守。", "在真正需要放大的方向上，它也会压住步长。"),
        ("工程上更常用什么？", "调好的 AdamW + warmup，而不是直接换 AMSGrad。"),
    ], size=13, gap=0.78, bullet_color=RED)
    takeaway(s, "AMSGrad 是「理论补丁」，不是「默认答案」；它提醒我们 Adam 的收敛性依赖假设。", accent=RED)
    notes(s, "AMSGrad 的核心是把二阶矩的 running max 拿来做分母，保证步长不增。"
             "实际大模型训练几乎没人直接用，但它是理解 Adam 收敛性的必经之路。")


# ---------------------------------------------------------------- 18 decouple
def p_decouple(s):
    header(s, "AdamW 的起点", "weight decay ≠ L2", "对 SGD 等价，对 Adam 不等价——差别就在「谁先被自适应缩放」",
           source="Loshchilov & Hutter, ICLR 2019, §2", accent=AMBER)
    figure(s, "fig_adamw.png", 1.05, 1.84, 11.3, 4.20)
    add_text(s, M, 6.12, 12.0, 0.26,
             "SGD：g+λθ 等价于在 loss 上加 λ/2·||θ||²；Adam：g+λθ 会先被 √v̂ 除，衰减被逐坐标缩放。",
             size=11.5, color=MUTED)
    takeaway(s, "同一个 λ，在 SGD 里是正则，在 Adam 里是「被梯度绑架的衰减」。", accent=AMBER)
    notes(s, "这是全篇最关键的一次代数推导。L2 是在梯度上加 λθ，weight decay 是直接缩小参数；"
             "SGD 里两者等价，因为梯度会原样作用到参数上。Adam 里中间隔了一个 1/√v̂，等价性被破坏。")


# ---------------------------------------------------------------- 19 AdamW
def p_adamw(s):
    header(s, "AdamW", "把正则从梯度里拿出来", "解耦之后，weight decay 只由 λ 和 η 决定，不再被二阶矩缩放",
           source="Loshchilov & Hutter, ICLR 2019", accent=AMBER)
    formula(s, M, 1.84, CW, 1.42, [
        [("θ", "i"), ("t", "sub"), (" = θ", ""), ("t−1", "sub"), (" − η · m̂", ""), ("t", "sub"),
         (" / (√v̂", ""), ("t", "sub"), (" + ε)  − η λ θ", ""), ("t−1", "sub")],
    ], size=21, label="AdamW：解耦 weight decay", accent=AMBER)
    bullets(s, M, 3.52, 7.0, [
        ("衰减只由 λ、η 决定。", "不再经过 1/√v̂，每个坐标被同等对待。"),
        ("默认 lr=1e-3 下，15% relative test error 改进。", "CIFAR-10 与 ImageNet32x32 都成立。"),
        ("让 Adam 能和 SGD+momentum 正面竞争。", "这是 ICLR 2019 论文的核心主张。"),
    ], size=13, gap=0.86, bullet_color=AMBER)
    add_rect(s, 7.95, 3.52, 4.76, 2.52, fill=rgb("FFF7ED"), line=rgb("FED7AA"), radius=0.06)
    add_text(s, 8.20, 3.68, 4.3, 0.3, "一句话记住", size=11, bold=True, color=AMBER)
    add_text(s, 8.20, 4.04, 4.25, 1.8,
             "Adam 的自适应是「按坐标」的，\n"
             "所以正则也必须「按坐标之外」\n"
             "的方式施加。\n\n"
             "解耦，就是把两个旋钮分开。",
             size=13, color=TEXT, line_spacing=1.42)
    takeaway(s, "AdamW 不是新优化器，而是把 Adam 的正则放回它该在的位置。", accent=AMBER)
    notes(s, "更新式最后一项 −ηλθ 是直接乘在参数上的，不经过 m̂/√v̂。这就是「解耦」的全部含义。"
             "15% 是相对测试误差，不是绝对准确率。")


# ---------------------------------------------------------------- 20 evidence + llama
def p_evidence(s):
    header(s, "证据", "15% 从哪来，工业界怎么用", "论文证据 + Llama 3 的真实配方，一起看",
           source="AdamW 论文 §1/§5；Llama 3 405B 论文 §3.1", accent=AMBER)
    add_rect(s, M, 1.84, 5.55, 3.20, fill=CARD, line=LINE, radius=0.06)
    add_text(s, M + 0.26, 2.00, 5.0, 0.3, "15% 是什么", size=11, bold=True, color=AMBER)
    add_text(s, M + 0.26, 2.28, 5.05, 0.88, "15%", size=44, bold=True, color=TEXT)
    add_text(s, M + 0.26, 3.20, 5.05, 1.65,
             "relative improvement in test error\n"
             "CIFAR-10 与 ImageNet32x32，默认 lr=1e-3\n"
             "对比对象：Adam + L2 正则\n\n"
             "不是绝对准确率提升 15 个点，\n而是相对误差下降 15%。",
             size=12, color=TEXT, line_spacing=1.4)
    add_text(s, 6.55, 1.90, 6.2, 0.3, "Llama 3 405B 的 AdamW 配方", size=11, bold=True, color=AMBER)
    data = [["超参", "取值"],
            ["优化器", "AdamW"],
            ["峰值学习率", "8e-5"],
            ["warmup", "8000 步"],
            ["衰减", "cosine → 8e-7"],
            ["weight decay", "0.1"],
            ["训练步数", "1.2M"]]
    table(s, 6.55, 2.24, 6.15, data, [1.9, 4.25], row_h=0.44, body=12, head=12.5)
    add_text(s, 6.55, 5.48, 6.15, 0.5,
             "论文正文未给出 β₁/β₂；不要把它背成「AdamW 一定更好」。",
             size=10.5, color=MUTED, line_spacing=1.3)
    takeaway(s, "AdamW 是「默认起点」：先解耦，再按任务调 λ 与 lr。", accent=AMBER)
    notes(s, "15% 在论文的引言和实验部分，不在摘要。Llama 3 的配方说明：到了 405B，大家用的还是 AdamW，"
             "关键是 warmup、cosine 和 weight decay 的配合。")


# ---------------------------------------------------------------- 21 boundaries
def p_bounds(s):
    header(s, "边界", "AdamW 也不是万能答案", "它修好了正则，但没有修掉自适应方法的所有问题",
           source="本讲整理；结合 Wilson 2017 与工业实践", accent=AMBER)
    blocks = [
        ("仍需调参", "解耦只是把 lr 和 wd 两个旋钮分开，不是免调。\n大模型里 λ 常按参数组设置：\nembedding / LayerNorm 往往设 0 或更小。", BLUE),
        ("泛化争议未消失", "小数据、分布偏移、需要强正则的任务上，\n调好的 SGD+momentum 仍可能更好。\n不要默认「新的一定赢」。", RED),
        ("不是所有参数都该衰减", "bias、LayerNorm 的 scale、embedding\n通常不参与 weight decay。\n分组设 wd 比一个全局 λ 更常见。", AMBER),
    ]
    for i, (title, body, col) in enumerate(blocks):
        y = 1.90 + i * 1.48
        add_rect(s, M, y, CW, 1.26, fill=CARD, line=LINE, radius=0.06)
        add_rect(s, M, y, 0.07, 1.26, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, M + 0.28, y + 0.18, 3.4, 0.36, title, size=16, bold=True, color=col)
        add_text(s, M + 3.9, y + 0.16, 8.0, 0.95, body, size=13, color=TEXT, line_spacing=1.35)
    takeaway(s, "AdamW 是默认起点，不是万能答案；先问任务，再问超参。", accent=AMBER)
    notes(s, "这一页是给「无脑 AdamW」泼冷水的。三个边界都是实践中真实存在的：分组 wd、泛化争议、"
             "以及解耦并不减少调参工作量。")


# ---------------------------------------------------------------- 22 low rank
def p_lowrank(s):
    header(s, "Muon 的出发点", "更新矩阵，几乎是低秩的", "谱衰减很快：少数奇异值携带大部分能量，逐元素缩放看不到这件事",
           source="Jordan 2024；本讲 Toy 谱分析（合成 64×32 矩阵）", accent=RED)
    figure(s, "fig_lowrank.png", 0.95, 1.82, 11.45, 3.90)
    add_text(s, M, 5.92, 12.0, 0.34,
             "逐元素自适应看到的是「每个坐标」；Muon 看到的是「整个矩阵的谱」。",
             size=13, color=TEXT)
    takeaway(s, "如果更新是低秩的，逐元素缩放就是在错误的空间里做微调。", accent=RED)
    notes(s, "这张图是合成的 64×32 矩阵，谱从 1 衰减到 0.015，前几个奇异值就占了大部分能量。"
             "真实训练里的梯度矩阵也常呈现这种重尾谱。Muon 的问题就是：能不能直接对谱做预条件？")


# ---------------------------------------------------------------- 23 muon algo
def p_muon_algo(s):
    header(s, "Muon", "三步：动量 → 正交化 → 缩放", "只改 2D hidden 参数的更新方向；embedding、head、标量仍交给 AdamW",
           source="Jordan 2024 博客；Moonshot 2025 §2", accent=RED)
    steps = [
        ("1", "Nesterov 动量", "M = μM + G，先按 M 预判一步；\n再用 G + μM 作为要正交化的方向。"),
        ("2", "Newton–Schulz 正交化", "O = NS5(G + μM)，把奇异值压到 1 附近；\n不做 SVD，只用矩阵乘法。"),
        ("3", "缩放后更新", "W ← W − η(0.2·O·√max(A,B) + λW)；\nscale 让 update RMS 对齐 AdamW。"),
    ]
    for i, (n, title, body) in enumerate(steps):
        y = 1.90 + i * 1.40
        add_circle(s, M, y + 0.10, 0.42, fill=RED if i < 2 else AMBER, line=None)
        add_text(s, M, y + 0.17, 0.42, 0.28, n, size=12, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER)
        add_text(s, M + 0.60, y + 0.04, 5.0, 0.34, title, size=15, bold=True, color=TEXT)
        add_text(s, M + 0.60, y + 0.44, 5.4, 0.8, body, size=11.5, color=MUTED, line_spacing=1.3)
    code_block(s, 6.55, 1.90, 6.16, 3.95, [
        ("for W in hidden_2d:", "E2E8F0"),
        ("    G = grad(W)", "E2E8F0"),
        ("    M = mu * M + G", "5EEAD4"),
        ("    O = ns5(G + mu * M)", "5EEAD4"),
        ("    W -= lr * (", "E2E8F0"),
        ("      0.2 * O * sqrt(max(A, B))", "FCD34D"),
        ("      + wd * W)", "FCD34D"),
    ], size=12, title="核心循环（示意）")
    add_text(s, 6.55, 5.98, 6.2, 0.3, "Q / K / V 分开做效果更好；4D 卷积可 flatten 成 3D。",
             size=10.5, color=MUTED)
    takeaway(s, "Muon 把「逐元素缩放」换成「矩阵正交化」：更新的每个方向都走同样远。", accent=RED)
    notes(s, "注意 Muon 不是所有参数都用：embedding、最终 classifier、标量/向量参数仍然用 AdamW。"
             "Q/K/V 分开优化是实践中的细节。")


# ---------------------------------------------------------------- 24 NS
def p_ns(s):
    header(s, "数学", "Newton–Schulz：5 步把谱压平", "不做 SVD，用矩阵乘法迭代逼近极分解的 U 因子",
           source="Jordan 2024；系数 a,b,c = 3.4445, −4.7750, 2.0315", accent=RED)
    figure(s, "fig_spectrum.png", 0.95, 1.82, 11.45, 4.10)
    add_text(s, M, 6.06, 12.0, 0.28,
             "NS5 后 σ ∈ [0.682, 1.132]；算子开销 ≤1%（NanoGPT 0.7%，Llama 405B 0.5%）。",
             size=12, color=TEXT)
    takeaway(s, "正交化的目的不是「变正交」，而是把谱压平，让每个方向都走同样远。", accent=RED)
    notes(s, "NS 迭代是 G ← aG + b(AAᵀ)G + c(AAᵀ)²G 的 5 次复合，bf16 就能跑。"
             "它逼近的是 polar factor UVᵀ，也就是最近的半正交矩阵。")


# ---------------------------------------------------------------- 25 evidence 2
def p_evidence2(s):
    header(s, "战绩", "三条证据，三种规模", "CIFAR speedrun、NanoGPT、1.5B——都在说同一件事：每步更值钱",
           source="Jordan 2024 博客；NanoGPT speedrun 记录", accent=RED)
    figure(s, "fig_compute.png", 1.05, 1.84, 11.25, 4.05)
    add_text(s, M, 6.02, 12.0, 0.3,
             "CIFAR-10 94%：3.3 → 2.6 A100-seconds；NanoGPT：1.35×；12 次记录由 7 位研究者保持。",
             size=11.5, color=TEXT)
    takeaway(s, "小规模 speedrun 与 1.5B 都成立，但都还没到前沿规模——这是 Muon 当时的边界。", accent=RED)
    notes(s, "三条证据的说服力不同：CIFAR 是玩具，NanoGPT 是可复现的中等规模，1.5B 才接近工业。"
             "注意 10 vs 13.3 是达到同一 HellaSwag 水平所需的 8×H100 小时。")


# ---------------------------------------------------------------- 26 moonshot
def p_scale(s):
    header(s, "规模化", "Moonshot：先让 Muon 的尺度和 AdamW 可比", "两个关键修正：加 weight decay、按参数调 update scale",
           source="Moonshot AI, arXiv 2502.16982", accent=RED)
    formula(s, M, 1.84, CW, 1.45, [
        [("W", "i"), ("t", "sub"), (" = W", ""), ("t−1", "sub"), (" − η(0.2 · O · √max(A,B) + λ W", ""),
         ("t−1", "sub"), (")", "")],
    ], size=20, label="Muon 的规模化更新式", accent=RED)
    bullets(s, M, 3.62, 7.2, [
        ("加 weight decay。", "原始 Muon 没有 wd；规模化必须补上。"),
        ("对齐 update scale。", "0.2·O·√max(A,B)，让 update RMS 落在 AdamW 的 0.2–0.4。"),
        ("结果：约 2× compute efficiency。", "Moonlight 3B/16B MoE，5.7T tokens，wd=0.1，lr=4.2e-4。"),
    ], size=13, gap=0.82, bullet_color=RED)
    add_rect(s, 8.05, 3.62, 4.66, 2.40, fill=rgb("FEF2F2"), line=rgb("FECACA"), radius=0.06)
    add_text(s, 8.28, 3.78, 4.2, 0.3, "为什么 scale 重要", size=11, bold=True, color=RED)
    add_text(s, 8.28, 4.14, 4.18, 1.7,
             "Muon 的更新是半正交矩阵，\n"
             "每个元素的量级由矩阵形状决定。\n\n"
             "不按 √max(A,B) 缩放，\n"
             "不同层的有效学习率会差一个量级。",
             size=11.5, color=TEXT, line_spacing=1.35)
    takeaway(s, "Muon 要规模化，先得让它的更新尺度和 AdamW 可比。", accent=RED)
    notes(s, "0.2 不是魔法数：它让 Muon 的 update RMS 和调好的 AdamW 接近。"
             "Moonlight 是 3B/16B MoE，5.7T tokens，证明 Muon 在 MoE 上也能跑。")


# ---------------------------------------------------------------- 27 kimi
def p_kimi(s):
    header(s, "前沿", "Kimi K2：1T 参数，15.5T token，零 loss spike", "MuonClip = Muon + QK-clip：给注意力 logit 装一个保险丝",
           source="Kimi K2, arXiv 2507.20534", accent=RED)
    stats = [("总参数", "1T"), ("激活参数", "32B"), ("训练 token", "15.5T"), ("loss spike", "0")]
    for i, (label, value) in enumerate(stats):
        x = M + i * 3.05
        add_rect(s, x, 1.84, 2.88, 1.10, fill=CARD, line=LINE, radius=0.06)
        add_text(s, x + 0.22, 1.96, 2.4, 0.26, label, size=10.5, bold=True, color=MUTED)
        add_text(s, x + 0.22, 2.22, 2.4, 0.44, value, size=27, bold=True, color=TEXT)
    bullets(s, M, 3.20, 7.0, [
        ("QK-clip 触发条件。", "per-head max logit 超过 τ=100，就缩放 Wq / Wk。"),
        ("逐 head，不是逐层。", "Wq ← γ^α Wq，Wk ← γ^(1−α) Wk，只压住出问题的头。"),
        ("稳定后关闭。", "clip 是训练早期的保险丝，不是永久约束。"),
    ], size=13, gap=0.86, bullet_color=RED)
    add_rect(s, 7.95, 3.20, 4.76, 2.85, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 8.18, 3.36, 4.3, 0.3, "为什么 Muon 更需要它", size=11, bold=True, color=RED)
    add_text(s, 8.18, 3.74, 4.25, 2.1,
             "Muon 的更新更「均匀」，\n"
             "注意力 logit 更容易快速变大。\n\n"
             "logit explosion 不会立刻表现为\n"
             "梯度爆炸，而是先表现为 loss 尖峰。\n"
             "QK-clip 在它变成 spike 之前动手。",
             size=11.5, color=TEXT, line_spacing=1.38)
    takeaway(s, "1T 参数把 Muon 从「实验室更快」变成「前沿可用」。", accent=RED)
    notes(s, "K2 是 1T 总参 / 32B 激活的 MoE。MuonClip 的关键是逐 head 的 max logit 监控，"
             "阈值 100，缩放指数 α 和 γ 由超参控制。")


# ---------------------------------------------------------------- 28 comparison
def p_compare(s):
    header(s, "对比", "Adam / AdamW / Muon 一张表", "不是「谁更好」，而是「谁在解决哪一层」",
           source="综合 Kingma 2015；Loshchilov 2019；Jordan 2024；Moonshot 2025", accent=AMBER)
    data = [
        ["维度", "Adam", "AdamW", "Muon"],
        ["更新方向", "动量 + 二阶矩", "同 Adam", "Nesterov 动量 + 正交化"],
        ["步长", "逐坐标自适应", "逐坐标自适应", "矩阵谱对齐"],
        ["正则", "L2 耦合在梯度里", "解耦 weight decay", "解耦 wd（规模化必需）"],
        ["参数范围", "全部参数", "全部参数", "仅 2D hidden"],
        ["额外显存", "2× 参数（m, v）", "2× 参数", "动量 + 临时矩阵"],
        ["代表", "Transformer 2017", "Llama 3 405B", "Kimi K2 / Moonlight"],
    ]
    table(s, M, 1.86, CW, data, [1.55, 3.45, 3.35, 3.74], row_h=0.52, body=12, head=12.5)
    add_text(s, M, 5.82, 12.0, 0.3,
             "选型的第一问不是「哪个 SOTA」，而是「我的参数是不是矩阵、规模多大、能不能重调超参」。",
             size=13, color=MUTED)
    takeaway(s, "三者的关系是叠加，不是替代：Muon 的 embedding 仍然用 AdamW。", accent=AMBER)
    notes(s, "表格里的「额外显存」是粗略量级：Adam 要存 m 和 v，Muon 要存动量，NS 还要临时矩阵。"
             "参数范围是 Muon 最重要的限制。")


# ---------------------------------------------------------------- 29 choose
def p_choose(s):
    header(s, "选型", "先问三个问题，再选优化器", "参数是不是矩阵？规模多大？能不能重调超参？",
           source="本讲整理", accent=AMBER)
    add_rect(s, 3.2, 1.84, 7.0, 0.72, fill=NAVY, line=None, radius=0.08)
    add_text(s, 3.2, 2.02, 7.0, 0.36, "你的场景更接近哪一边？", size=16, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    branches = [
        ("默认 / 微调 / 小数据", "AdamW", "先调 λ 与 lr；\nembedding、LayerNorm 分组设 wd。", BLUE),
        ("大规模预训练 + 2D hidden", "Muon + AdamW", "矩阵参数用 Muon；\nembedding / head / 标量用 AdamW。", TEAL),
        ("强正则 / 追求泛化", "SGD + momentum", "仍值得试；\n尤其在数据少、分布偏移时。", AMBER),
    ]
    for i, (scene, choice, note_, col) in enumerate(branches):
        x = M + i * 4.03
        add_text(s, x + 1.6, 2.72, 0.3, 0.4, "↓", size=24, bold=True, color=SLATE,
                 align=PP_ALIGN.CENTER)
        add_rect(s, x, 3.20, 3.86, 2.55, fill=CARD, line=LINE, radius=0.06)
        add_rect(s, x, 3.20, 3.86, 0.08, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, x + 0.24, 3.40, 3.3, 0.3, scene, size=11, bold=True, color=MUTED)
        add_text(s, x + 0.24, 3.72, 3.4, 0.42, choice, size=21, bold=True, color=col)
        add_text(s, x + 0.24, 4.26, 3.4, 1.3, note_, size=11.5, color=TEXT, line_spacing=1.35)
    add_text(s, M, 5.94, 12.0, 0.3, "没有「最好的优化器」，只有「和你的约束最匹配的优化器」。",
             size=13, color=MUTED)
    takeaway(s, "先排除参数范围，再谈效率；Muon 不是所有参数的答案。", accent=AMBER)
    notes(s, "决策树故意做得很短：三个问题就能排除大部分错误选项。实际选型还要看框架支持、"
             "分布式通信成本和团队经验。")


# ---------------------------------------------------------------- 30 pitfalls
def p_pitfalls(s):
    header(s, "避坑", "六个最常见的坑", "每一个都能让「换个优化器」变成一次事故",
           source="本讲整理；结合 Jordan 2024 与工程实践", accent=TEAL)
    items = [
        ("换优化器，不换 lr", "Adam 的合适 lr 通常比 SGD 小 1–2 个量级；直接套用会炸。"),
        ("把 wd 当 L2", "在 Adam 下两者不等价；调 wd 前先确认代码用的是哪一种。"),
        ("忘掉 warmup", "自适应方法早期方差大，没有 warmup 容易在第一步就发散。"),
        ("对 embedding 用 Muon", "Muon 只支持 2D hidden；embedding / head 必须留给 AdamW。"),
        ("忽略 logit 爆炸", "Muon 更易出现；监控 per-head max logit，必要时上 QK-clip。"),
        ("只看 loss，不看下游", "loss 更低不等于泛化更好；验证集与下游任务才是裁决。"),
    ]
    for i, (head, body) in enumerate(items):
        col = i % 3
        row = i // 3
        x = M + col * 4.03
        y = 1.88 + row * 2.16
        add_rect(s, x, y, 3.86, 1.92, fill=CARD, line=LINE, radius=0.06)
        add_text(s, x + 0.24, y + 0.16, 0.6, 0.36, f"0{i+1}", size=12, bold=True, color=TEAL)
        add_text(s, x + 0.24, y + 0.52, 3.4, 0.34, head, size=14, bold=True, color=TEXT)
        add_text(s, x + 0.24, y + 0.94, 3.4, 0.86, body, size=12, color=MUTED, line_spacing=1.3)
    takeaway(s, "换优化器是一次「重调超参」的项目，不是一行 import。", accent=TEAL)
    notes(s, "六个坑按出现频率排序。最隐蔽的是「把 wd 当 L2」和「只看 loss 不看下游」。")


# ---------------------------------------------------------------- 31 lab
def p_lab(s):
    header(s, "动手", "15 行代码，自己复现一次", "不用大模型：一个病态二次函数就能看出三种优化器的差别",
           source="本讲 experiment.py；结果见 experiment-results.json", accent=TEAL)
    code_block(s, M, 1.86, 6.55, 4.30, [
        ("import torch", "E2E8F0"),
        ("f = lambda x: 0.5*(x[0]**2 + 100*x[1]**2)", "E2E8F0"),
        ("x = torch.tensor([-2.6, 2.2], requires_grad=True)", "E2E8F0"),
        ("opt = torch.optim.Adam([x], lr=0.58)", "5EEAD4"),
        ("for step in range(200):", "E2E8F0"),
        ("    opt.zero_grad()", "E2E8F0"),
        ("    loss = f(x)", "E2E8F0"),
        ("    loss.backward()", "E2E8F0"),
        ("    opt.step()", "E2E8F0"),
        ("    if loss < 1e-6: break", "FCD34D"),
    ], size=12, title="toy.py（示意）")
    add_text(s, 7.45, 1.92, 5.2, 0.3, "跑出来应该看到", size=11, bold=True, color=TEAL)
    rows = [("SGD", "263 步", "lr=0.018", SLATE),
            ("动量", "90 步", "lr=0.00344", BLUE),
            ("Adam", "83 步", "lr=0.5789", TEAL)]
    for i, (name, steps, lr, col) in enumerate(rows):
        y = 2.32 + i * 0.78
        add_text(s, 7.45, y, 1.0, 0.3, name, size=14, bold=True, color=col)
        add_text(s, 8.50, y, 1.6, 0.3, steps, size=14, bold=True, color=TEXT)
        add_text(s, 10.15, y, 2.4, 0.3, lr, size=11.5, color=MUTED)
    add_text(s, 7.45, 4.78, 5.2, 1.3,
             "三种优化器各自做了 40 点 lr 网格搜索，\n比较的是各自最好成绩。\n\n"
             "把 100 改成 1000，再看谁先崩。",
             size=11.5, color=MUTED, line_spacing=1.35)
    takeaway(s, "亲手跑一次，比背十个公式更有用。", accent=TEAL)
    notes(s, "这个 toy 的代码在仓库 experiment.py 里，包含动量与 Adam 的实现，以及 Muon 的谱实验。"
             "建议现场改条件数，看 SGD 什么时候崩。")


# ---------------------------------------------------------------- 32 timeline
def p_timeline(s):
    header(s, "时间线", "从 1847 到 2025", "每一条竖线都是一次「补维度」，不是一次推翻",
           source="各原始论文；详见 research-notes.md", accent=TEAL)
    row1 = [("1847", "Cauchy\n最速下降"), ("1951", "Robbins–Monro\n随机近似"),
            ("1960", "Widrow–Hoff\nLMS"), ("1964", "Polyak\n动量"),
            ("1983", "Nesterov\n加速梯度"), ("1986", "反向传播\n梯度可算")]
    row2 = [("2011", "AdaGrad"), ("2012", "RMSProp"), ("2015", "Adam"),
            ("2018", "AMSGrad"), ("2019", "AdamW"), ("2023", "Lion / Sophia"),
            ("2024", "Muon"), ("2025", "Moonshot\nKimi K2")]
    for r, (row, y) in enumerate([(row1, 2.78), (row2, 5.16)]):
        add_line(s, 0.85, y, 12.45, y, color=LINE, width=2)
        n = len(row)
        gap = 11.6 / (n - 1)
        for i, (year, label) in enumerate(row):
            x = 0.85 + i * gap
            add_circle(s, x - 0.07, y - 0.07, 0.14, fill=TEAL if r == 0 else AMBER,
                       line=WHITE, line_w=1.5)
            up = (i % 2 == 0)
            if up:
                add_text(s, x - 0.85, y - 0.62, 1.7, 0.3, year, size=13.5, bold=True,
                         color=TEAL if r == 0 else AMBER, align=PP_ALIGN.CENTER)
                add_text(s, x - 0.85, y - 1.22, 1.7, 0.55, label, size=9.3, color=TEXT,
                         align=PP_ALIGN.CENTER, line_spacing=1.15)
            else:
                add_text(s, x - 0.85, y + 0.26, 1.7, 0.3, year, size=13.5, bold=True,
                         color=TEAL if r == 0 else AMBER, align=PP_ALIGN.CENTER)
                add_text(s, x - 0.85, y + 0.60, 1.7, 0.55, label, size=9.3, color=TEXT,
                         align=PP_ALIGN.CENTER, line_spacing=1.15)
    takeaway(s, "七十年只做了一件事：把「一个标量步长」拆成方向、坐标与谱。", accent=TEAL)
    notes(s, "时间线分两行：上面是理论与计算基础，下面是自适应与结构化。"
             "注意 2011 之后节奏明显加快。")


# ---------------------------------------------------------------- 33 cheatsheet
def p_cheatsheet(s):
    header(s, "速查", "七个更新式，一张表", "考前/开工前扫一眼；公式用 Times New Roman 排版",
           source="各原始论文；符号与正文一致", accent=TEAL)
    rows = [
        ("SGD", "θ ← θ − η g"),
        ("动量", "v ← βv + g;  θ ← θ − ηv"),
        ("AdaGrad", "G ← G + g²;  θ ← θ − ηg/√(G+ε)"),
        ("RMSProp", "E ← ρE + (1−ρ)g²;  θ ← θ − ηg/√(E+ε)"),
        ("Adam", "m ← β₁m+(1−β₁)g;  v ← β₂v+(1−β₂)g²\nθ ← θ − η m̂/(√v̂+ε)"),
        ("AdamW", "θ ← θ − η m̂/(√v̂+ε) − ηλθ"),
        ("Muon", "O ← NS5(G+μM);  W ← W − η(0.2·O·√max(A,B)+λW)"),
    ]
    y = 1.88
    for i, (name, formula_) in enumerate(rows):
        h = 0.62 if "\n" not in formula_ else 0.88
        add_rect(s, M, y, CW, h - 0.06, fill=CARD if i % 2 == 0 else rgb("F8FAFC"),
                 line=LINE, radius=0.04)
        add_text(s, M + 0.22, y + (h - 0.34) / 2 - 0.02, 1.7, 0.32, name, size=13,
                 bold=True, color=TEAL)
        add_text(s, M + 2.0, y + 0.06, 9.8, h - 0.16, formula_, size=13, color=TEXT,
                 font_ea=MATH, font_lat=MATH, line_spacing=1.25)
        y += h
    takeaway(s, "公式只是压缩包；真正要记的是每个符号在补哪个洞。", accent=TEAL)
    notes(s, "这一页是给学员拍照用的。建议配合第 17 页的「三层」一起记。")


# ---------------------------------------------------------------- 34 references
def p_refs(s):
    header(s, "来源", "关键来源与延伸阅读", "所有数字都能在这些文献里找到；边界与争议也标注在正文",
           source="按时间排序；完整对照见 research-notes.md", accent=TEAL)
    refs = [
        "Cauchy (1847). Méthode générale pour la résolution des systèmes d'équations simultanées.",
        "Robbins & Monro (1951). A stochastic approximation method. Ann. Math. Stat.",
        "Polyak (1964). Some methods of speeding up the convergence of iteration methods.",
        "Nesterov (1983). A method of solving a convex programming problem with convergence rate O(1/k²).",
        "Rumelhart, Hinton & Williams (1986). Learning representations by back-propagating errors.",
        "Duchi, Hazan & Singer (2011). Adaptive subgradient methods (AdaGrad). JMLR.",
        "Hinton (2012). Neural networks for machine learning, Coursera (RMSProp).",
        "Kingma & Ba (2015). Adam: A method for stochastic optimization. ICLR.",
        "Wilson et al. (2017). The marginal value of adaptive gradient methods.",
        "Reddi, Kale & Kumar (2018). On the convergence of Adam and beyond. ICLR.",
        "Loshchilov & Hutter (2019). Decoupled weight decay regularization (AdamW). ICLR.",
        "Shazeer & Stern (2018). Adafactor; You et al. (2019). LAMB.",
        "Chen et al. (2023). Lion; Liu et al. (2023). Sophia.",
        "Jordan (2024). Muon: An optimizer for hidden layers in neural networks. Blog.",
        "Moonshot AI (2025). Muon is scalable for LLM training. arXiv:2502.16982.",
        "Kimi K2 Team (2025). Kimi K2: Open agentic intelligence. arXiv:2507.20534.",
    ]
    for i, ref in enumerate(refs):
        col = i // 8
        row = i % 8
        x = M + col * 6.15
        y = 1.88 + row * 0.62
        add_text(s, x, y, 0.4, 0.24, f"{i+1:02d}", size=9, bold=True, color=TEAL)
        add_text(s, x + 0.38, y - 0.02, 5.55, 0.58, ref, size=9.5, color=TEXT, line_spacing=1.2)
    takeaway(s, "先读原始论文，再读二手总结；数字要对得上表格。", accent=TEAL)
    notes(s, "参考文献按时间排序。Muon 的博客和 Moonshot、Kimi K2 的论文是第三部分的主要依据。")


# ---------------------------------------------------------------- 35 end
def p_end(s):
    bump()
    slide_bg(s, DARK)
    add_circle(s, 9.2, -1.6, 6.2, fill=rgb("13203A"), line=None)
    add_text(s, 1.0, 1.25, 10.5, 0.4, "结语", size=13, bold=True, color=TEAL2)
    add_text(s, 0.98, 1.72, 11.2, 1.2, "三句话，带走整场", size=44, bold=True, color=WHITE)
    lines = [
        ("1", "Adam 解决「每个坐标走多大」，", "把步长从梯度大小里解耦出来。"),
        ("2", "AdamW 解决「正则被谁绑架」，", "把 weight decay 从自适应里拿出来。"),
        ("3", "Muon 解决「矩阵的谱」，", "把逐元素缩放换成矩阵正交化。"),
    ]
    for i, (n, head, tail) in enumerate(lines):
        y = 3.15 + i * 0.98
        add_text(s, 1.0, y, 0.5, 0.4, n, size=22, bold=True, color=TEAL2)
        add_text(s, 1.55, y - 0.02, 10.6, 0.4, head, size=19, bold=True, color=WHITE)
        add_text(s, 1.55, y + 0.40, 10.6, 0.36, tail, size=14, color=rgb("A8B6CC"))
    add_text(s, 1.0, 6.70, 10.0, 0.4, "谢谢 · 问题与讨论", size=15, color=rgb("7C8BA3"))
    notes(s, "收尾回到三句话：方向、正则、矩阵几何。鼓励听众回去跑第 35 页的 toy 实验。")


# ---------------------------------------------------------------- build
def build(out_name="从下山到矩阵几何：梯度下降优化器七十年-v2.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    blank = prs.slide_layouts[6]
    CUR[0] = 0
    pages = [
        p_cover, p_questions, p_paradigms, p_why, p_hero, p_history, p_sgd, p_canyon, p_lr,
        lambda s: divider(s, "02", "1964–2000", "让方向记住历史", "动量与 Nesterov：用过去几步抵消锯齿", BLUE),
        p_momentum,
        lambda s: divider(s, "03", "2011–2017", "给每个坐标一根尺子", "AdaGrad → RMSProp → Adam", PURPLE),
        p_adagrad, p_rmsprop, p_adam, p_bias, p_solved, p_crises, p_amsgrad,
        lambda s: divider(s, "04", "2017–2019", "把正则从梯度里拿出来", "AdamW：weight decay ≠ L2", AMBER),
        p_decouple, p_adamw, p_evidence, p_bounds,
        lambda s: divider(s, "05", "2024–2025", "在谱上做预条件", "Muon：从逐元素到矩阵", RED),
        p_lowrank, p_muon_algo, p_ns, p_evidence2, p_scale, p_kimi, p_compare, p_choose,
        p_pitfalls, p_lab, p_timeline, p_cheatsheet, p_refs, p_end,
    ]
    for fn in pages:
        s = prs.slides.add_slide(blank)
        fn(s)
    path = os.path.join(HERE, "out", out_name)
    prs.save(path)
    print("saved", path, "slides", len(prs.slides))
    return path


if __name__ == "__main__":
    build()
