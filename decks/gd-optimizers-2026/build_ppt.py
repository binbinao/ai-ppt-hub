# -*- coding: utf-8 -*-
"""Build the gradient-descent optimizers teaching deck (37 pages)."""
import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from _helpers import *  # noqa
from _helpers import (BG, DARK, NAVY, TEXT, MUTED, LINE, WHITE, TEAL, TEAL2, TEAL_L,
                      AMBER, AMBER2, AMBER_L, BLUE, BLUE_L, PURPLE, PURPLE_L,
                      RED, RED_L, GREEN, GREEN_L, SLATE, CARD, FONT_EA, FONT_LAT,
                      SW, SH, add_text, add_rich_text, add_rect, add_line,
                      add_circle, add_pill, slide_bg, header, add_metric,
                      add_bullets, add_table)

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
MATH = "Times New Roman"
MONO = "Menlo"


# ---------------------------------------------------------------- primitives
def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def bg(slide, color=BG):
    slide_bg(slide, color)


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


def add_math(slide, x, y, w, h, paras, size=16, color=TEXT, align=PP_ALIGN.CENTER,
             line_spacing=1.35, anchor=MSO_ANCHOR.MIDDLE):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
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
            sz = size * (0.62 if ("sub" in opts or "sup" in opts) else 1.0)
            base = -22000 if "sub" in opts else (30000 if "sup" in opts else None)
            math_run(p, text, sz, italic=("i" in opts and "sub" not in opts and "sup" not in opts),
                     bold=("b" in opts), color=color, baseline=base)
    return tb


def formula_card(slide, x, y, w, h, paras, label=None, accent=TEAL, size=16,
                 note=None, fill=CARD, line_spacing=1.35):
    add_rect(slide, x, y, w, h, fill=fill, line=LINE, radius=0.05)
    add_rect(slide, x, y, 0.055, h, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    if label:
        add_text(slide, x + 0.22, y + 0.12, w - 0.4, 0.2, label, size=8.5, bold=True, color=MUTED)
        top = y + 0.34
    else:
        top = y + 0.08
    add_math(slide, x + 0.22, top, w - 0.44, h - (top - y) - (0.34 if note else 0.08),
             paras, size=size, color=TEXT, line_spacing=line_spacing)
    if note:
        add_text(slide, x + 0.22, y + h - 0.34, w - 0.44, 0.24, note, size=8, color=MUTED)


def card(slide, x, y, w, h, title=None, body=None, accent=TEAL, fill=CARD,
         title_color=TEXT, title_size=11.5, body_size=10, body_color=TEXT, pad=0.2):
    add_rect(slide, x, y, w, h, fill=fill, line=LINE, radius=0.06)
    add_rect(slide, x, y, 0.055, h, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    ty = y + 0.14
    if title:
        add_text(slide, x + pad, ty, w - 2 * pad, 0.26, title, size=title_size, bold=True,
                 color=title_color)
        ty += 0.34
    if body:
        add_text(slide, x + pad, ty, w - 2 * pad, h - (ty - y) - 0.12, body,
                 size=body_size, color=body_color, line_spacing=1.2)


def takeaway(slide, text, y=6.45, accent=TEAL, label="记住"):
    add_rect(slide, 0.62, y, 12.09, 0.46, fill=WHITE, line=LINE, radius=0.12)
    add_rect(slide, 0.62, y, 0.07, 0.46, fill=accent, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(slide, 0.85, y + 0.11, 0.62, 0.24, label, size=8.5, bold=True, color=accent)
    add_text(slide, 1.55, y + 0.09, 10.95, 0.3, text, size=10.5, color=TEXT)


def section_num(slide, x, y, n, color=TEAL, d=0.34):
    add_circle(slide, x, y, d, fill=color, line=None)
    add_text(slide, x, y + 0.055, d, 0.24, str(n), size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER)


def code_card(slide, x, y, w, h, lines, title=None, size=10):
    add_rect(slide, x, y, w, h, fill=NAVY, line=None, radius=0.04)
    if title:
        add_text(slide, x + 0.18, y + 0.1, w - 0.3, 0.2, title, size=8, bold=True, color=SLATE)
        top = y + 0.34
    else:
        top = y + 0.14
    step = size * 1.32 / 72.0
    cur = top
    for item in lines:
        if isinstance(item, tuple):
            text, col = item
        else:
            text, col = item, rgb("E2E8F0")
        add_text(slide, x + 0.18, cur, w - 0.3, step + 0.06, text, size=size,
                 color=col, font_ea=MONO, font_lat=MONO)
        cur += step


def num_item(slide, x, y, w, n, head, body, accent=TEAL, h=1.1):
    section_num(slide, x, y + 0.02, n, color=accent)
    add_text(slide, x + 0.46, y - 0.02, w - 0.46, 0.3, head, size=11.5, bold=True, color=TEXT)
    add_text(slide, x + 0.46, y + 0.3, w - 0.46, h - 0.3, body, size=10, color=MUTED,
             line_spacing=1.2)


# ---------------------------------------------------------------- pages
def s01_cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, DARK)
    add_circle(s, 9.2, -1.8, 6.2, fill=rgb("13203A"), line=None)
    add_circle(s, 10.6, 0.2, 3.0, fill=None, line=TEAL, line_w=1)
    add_circle(s, 8.4, 5.4, 4.4, fill=rgb("0F1A2E"), line=None)
    add_rect(s, 0.72, 1.05, 0.06, 5.2, fill=TEAL, line=None, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, 1.0, 1.0, 8.0, 0.3, "教学讲义 · 深度学习优化器", size=10, bold=True, color=TEAL2)
    add_text(s, 0.98, 1.55, 10.6, 0.95, "从下山到矩阵几何", size=46, bold=True, color=WHITE,
             line_spacing=0.95)
    add_text(s, 1.0, 2.62, 10.8, 0.7,
             "梯度下降优化器的七十年：SGD → 动量 → Adam → AdamW → Muon",
             size=17, color=rgb("A8B6CC"))
    add_text(s, 1.0, 3.55, 10.4, 0.9,
             "为什么 Adam 解决了“每个坐标走多大”，\nAdamW 解决了“正则被谁绑架”，Muon 又为什么盯上了矩阵的奇异值。",
             size=12.5, color=rgb("CBD5E1"), line_spacing=1.35)
    labels = [("Adam", "2015 · 自适应", TEAL), ("AdamW", "2019 · 解耦正则", BLUE),
              ("Muon", "2024 · 矩阵几何", AMBER)]
    for i, (name, sub, col) in enumerate(labels):
        x = 1.0 + i * 3.2
        add_rect(s, x, 5.25, 2.9, 0.82, fill=rgb("0F1A2E"), line=col, radius=0.18)
        add_circle(s, x + 0.18, 5.5, 0.32, fill=col, line=None)
        add_text(s, x + 0.6, 5.33, 2.1, 0.28, name, size=12, bold=True, color=WHITE)
        add_text(s, x + 0.6, 5.62, 2.1, 0.24, sub, size=8.5, color=rgb("94A3B8"))
    add_line(s, 1.0, 6.62, 11.9, 6.62, color=rgb("243247"), width=0.75)
    add_text(s, 1.0, 6.75, 7.0, 0.25, "2026 · 37 页 · 含可复现 Toy 实验与选型清单", size=8.5,
             color=rgb("7C8BA3"))
    add_text(s, 8.0, 6.75, 4.0, 0.25, "所有关键数字均标注一手来源", size=8.5,
             color=rgb("7C8BA3"), align=PP_ALIGN.RIGHT)
    notes(s, "开场：今天不讲某个模型的架构，只讲训练里那一行最常见的代码——优化器。"
             "先给结论：Adam、AdamW、Muon 分别在解决方向、尺度、几何三个不同层次的问题。"
             "全程会穿插我们自己能复现的 toy 实验，以及论文里的真实数字。")


def s02_agenda(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "导读", "先回答三个问题", "如果这三个问题你已经有答案，可以直接跳到第 18 页",
           page=2, source="本讲整理")
    qs = [
        ("为什么同一个模型，换个优化器训练曲线就完全不同？", "方向、步长、记忆——三个旋钮。"),
        ("Adam 已经“自适应”了，为什么还需要 AdamW？", "因为 L2 正则和 weight decay 在 Adam 下不是一回事。"),
        ("Muon 只改了更新方向，为什么能省 2 倍算力？", "因为它把“逐元素缩放”换成了“矩阵谱上的正交化”。"),
    ]
    for i, (q, a) in enumerate(qs):
        y = 1.72 + i * 1.52
        add_rect(s, 0.62, y, 7.0, 1.32, fill=CARD, line=LINE, radius=0.06)
        section_num(s, 0.82, y + 0.18, i + 1)
        add_text(s, 1.3, y + 0.14, 6.1, 0.58, q, size=12, bold=True, color=TEXT, line_spacing=1.15)
        add_text(s, 1.3, y + 0.82, 6.1, 0.3, a, size=9.5, color=MUTED)
    add_rect(s, 7.95, 1.72, 4.76, 4.36, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 8.18, 1.86, 4.3, 0.3, "本讲路线", size=10, bold=True, color=MUTED)
    route = [("01", "历史与直觉", "第 3–10 页", TEAL),
             ("02", "自适应家族", "第 11–17 页", BLUE),
             ("03", "解耦正则", "第 18–22 页", PURPLE),
             ("04", "矩阵几何", "第 23–31 页", AMBER)]
    for i, (n, name, pages, col) in enumerate(route):
        y = 2.32 + i * 0.9
        add_text(s, 8.18, y, 0.5, 0.3, n, size=10, bold=True, color=col)
        add_text(s, 8.75, y - 0.02, 2.4, 0.3, name, size=11.5, bold=True, color=TEXT)
        add_text(s, 8.75, y + 0.28, 2.4, 0.24, pages, size=8.5, color=MUTED)
        add_line(s, 8.18, y + 0.64, 12.45, y + 0.64, color=LINE, width=0.6)
    takeaway(s, "优化器在解三个不同的问题：方向、尺度、几何。", accent=TEAL)
    notes(s, "三个问题就是全篇的骨架。第一个问题引出动量与自适应；第二个问题引出 AdamW；"
             "第三个问题引出 Muon。先别急着记公式，记住每代方法在补哪个洞。")


def s03_paradigms(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "全景", "七十年，四次范式转移", "每一次都不是推翻前一个，而是补上它看不见的维度",
           page=3, source="本讲整理；代表工作见第 34 页时间线")
    cards = [
        ("1951–1985", "随机化", "用带噪声的小批量梯度，\n代替全量梯度。", "Robbins–Monro 1951\nSGD / LMS 1960", TEAL),
        ("1964–2000", "加速", "记住过去的方向，\n抵消锯齿、冲出峡谷。", "Polyak 动量 1964\nNesterov 1983", BLUE),
        ("2011–2017", "自适应", "每个坐标有自己的\n有效步长。", "AdaGrad 2011\nRMSProp 2012 · Adam 2015", PURPLE),
        ("2017–now", "结构化", "解耦正则；直接对\n矩阵的谱做预条件。", "AdamW 2019\nMuon 2024", AMBER),
    ]
    for i, (era, name, idea, rep, col) in enumerate(cards):
        x = 0.62 + i * 3.06
        add_rect(s, x, 1.72, 2.9, 3.55, fill=CARD, line=LINE, radius=0.06)
        add_rect(s, x, 1.72, 2.9, 0.07, fill=col, line=None, shape_type=MSO_SHAPE.RECTANGLE)
        add_text(s, x + 0.2, 1.92, 2.5, 0.24, era, size=8.5, bold=True, color=col)
        add_text(s, x + 0.2, 2.2, 2.5, 0.4, name, size=16, bold=True, color=TEXT)
        add_text(s, x + 0.2, 2.72, 2.55, 1.0, idea, size=9.8, color=MUTED, line_spacing=1.3)
        add_line(s, x + 0.2, 3.86, x + 2.7, 3.86, color=LINE, width=0.7)
        add_text(s, x + 0.2, 3.98, 2.55, 0.8, rep, size=8, color=SLATE, line_spacing=1.3)
        add_text(s, x + 0.2, 4.82, 2.5, 0.3, f"0{i+1}", size=9, bold=True, color=LINE)
    labels = ["随机化", "加速", "自适应", "结构化"]
    cols = [TEAL, BLUE, PURPLE, AMBER]
    for i, (lab, col) in enumerate(zip(labels, cols)):
        x = 0.62 + i * 3.06
        add_pill(s, x, 5.52, 2.9, 0.4, lab, fill=WHITE, color=col, size=9)
        if i < 3:
            add_text(s, x + 2.92, 5.56, 0.16, 0.3, "›", size=16, bold=True, color=SLATE)
    takeaway(s, "优化的历史，是把“一个标量步长”拆成“方向、坐标、矩阵几何”的历史。", accent=AMBER)
    notes(s, "四次转移可以用一句话串起来：先让梯度带噪声也能收敛（随机化），再让方向更聪明（加速），"
             "再让每个坐标有自己的步长（自适应），最后把正则和矩阵几何单独拿出来（结构化）。"
             "注意时间有重叠，范式不是替代关系。")


def s04_why(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "动机", "换一行代码，账单差一倍", "优化器不改模型结构、不改数据，却直接改变 token 效率和算力成本",
           page=4, source="Jordan 2024；Moonshot 2025；NanoGPT speedrun 记录")
    data = [("NanoGPT 训练加速", "1.35×", "Muon vs 调好的 AdamW", TEAL),
            ("计算效率（compute-optimal）", "约 2×", "Moonshot 3B/16B MoE 对比", AMBER),
            ("CIFAR-10 speedrun", "3.3→2.6", "A100-seconds，94% 精度", BLUE)]
    for i, (label, value, note_, col) in enumerate(data):
        add_metric(s, 0.62 + i * 4.02, 1.72, 3.86, 1.42, label, value, note_, accent=col,
                   value_size=24)
    add_text(s, 0.62, 3.45, 6.3, 0.35, "为什么这一行值钱", size=12, bold=True, color=TEXT)
    add_bullets(s, 0.62, 3.85, 6.2, 2.4, [
        ("训练成本 ∝ 步数 × 每步算力。", "优化器同时影响两者：收敛快 = 步数少。"),
        ("它不动架构，所以是“免费”的收益。", "但换优化器通常要重调 lr / wd / warmup。"),
        ("失败模式也更隐蔽。", "不收敛、loss spike、泛化变差，往往几十亿 token 后才暴露。"),
    ], size=10.5, gap=0.1)
    add_rect(s, 7.15, 3.45, 5.56, 2.72, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 7.38, 3.6, 5.1, 0.3, "算一笔粗账", size=10, bold=True, color=AMBER)
    add_text(s, 7.38, 3.98, 5.05, 2.0,
             "一次前沿模型的预训练，算力账单以千万美元计。\n"
             "10% 的训练效率差，就是数百万美元量级的差别；\n"
             "如果因此多跑一次失败的大规模实验，代价还要翻倍。\n\n"
             "所以工业界对优化器的选择，远比论文里的“快几个点”谨慎。",
             size=10, color=MUTED, line_spacing=1.35)
    takeaway(s, "优化器是训练里性价比最高、也最容易被低估的一行代码。", accent=TEAL)
    notes(s, "三个数字分别代表三种证据：小规模 speedrun、规模化 compute-optimal、以及社区的复现记录。"
             "注意 2× 是 Moonshot 在 compute-optimal 设定下的结论，不是任何场景都 2×。")


def s05_descent(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "直觉", "训练就是下山，但山是 10⁹ 维的", "每一步只做三个决定：往哪走、走多远、记不记得来时的路",
           page=5, source="本讲绘制")
    add_rect(s, 0.62, 1.66, 6.55, 4.62, fill=WHITE, line=LINE, radius=0.05)
    s.shapes.add_picture(os.path.join(FIGS, "fig_descent.png"), Inches(0.72), Inches(1.76),
                         width=Inches(6.35))
    add_text(s, 0.82, 5.92, 6.2, 0.28, "一维示意：梯度是切线斜率；步长 η 决定这一步走多远。",
             size=8.5, color=MUTED)
    items = [("方向", "用哪个梯度：全量、mini-batch、还是加动量？", TEAL),
             ("步长", "η 是全局的，还是每个坐标一个？", BLUE),
             ("记忆", "要不要用过去几步的梯度？", AMBER)]
    for i, (head, body, col) in enumerate(items):
        y = 1.72 + i * 1.05
        add_text(s, 7.5, y, 1.0, 0.3, head, size=12, bold=True, color=col)
        add_text(s, 8.35, y + 0.02, 4.3, 0.55, body, size=10, color=MUTED, line_spacing=1.2)
        add_line(s, 7.5, y + 0.72, 12.6, y + 0.72, color=LINE, width=0.6)
    formula_card(s, 7.5, 5.0, 5.1, 1.2,
                 [[("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η ∇L(θ", ""), ("t", "sub"), (")", "")]],
                 accent=TEAL, size=18, note=None)
    takeaway(s, "所有优化器的差别，都可以还原成这三个决定的不同做法。", accent=TEAL)
    notes(s, "先建立共同语言：任何优化器都在决定方向、步长、记忆。SGD 只用当前梯度；动量加了记忆；"
             "自适应改了每个坐标的步长；Muon 改的是方向本身——把矩阵更新正交化。")


def s06_history(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "历史", "三条线在 1986 年汇合", "确定性下降、随机近似、反向传播——缺一条都没有今天的大模型训练",
           page=6, source="Cauchy 1847；Robbins & Monro 1951；Rumelhart et al. 1986")
    lanes = [("1847", "Cauchy", "梯度下降", "沿着负梯度走，函数值一定下降——但要求梯度可算、且是确定性的。", TEAL),
             ("1951", "Robbins–Monro", "随机近似", "梯度带噪声也能收敛：只要步长满足一定条件，噪声会被平均掉。", BLUE),
             ("1986", "Rumelhart 等", "反向传播", "用链式法则高效算出每个参数的梯度，深度网络才真正可训练。", PURPLE)]
    for i, (year, who, what, body, col) in enumerate(lanes):
        y = 1.72 + i * 1.28
        add_text(s, 0.62, y + 0.04, 0.95, 0.32, year, size=15, bold=True, color=col)
        add_text(s, 1.6, y, 2.4, 0.3, f"{who} · {what}", size=11, bold=True, color=TEXT)
        add_text(s, 1.6, y + 0.34, 6.6, 0.62, body, size=9.8, color=MUTED, line_spacing=1.25)
        add_line(s, 1.6, y + 1.02, 8.4, y + 1.02, color=LINE, width=0.6)
    add_rect(s, 9.0, 2.05, 3.7, 2.55, fill=NAVY, line=None, radius=0.06)
    add_text(s, 9.25, 2.22, 3.2, 0.3, "汇合之后", size=8.5, bold=True, color=TEAL2)
    add_text(s, 9.25, 2.55, 3.2, 1.8,
             "现代 SGD：\n小批量梯度\n+ 反向传播\n+ 学习率调度",
             size=13, bold=True, color=WHITE, line_spacing=1.4)
    add_text(s, 9.25, 4.02, 3.2, 0.3, "1986 年之后的一切，都从这里出发", size=8, color=SLATE)
    takeaway(s, "先有“往哪走”，再有“噪声下也能走”，最后才有“算得动”——三者合流，深度学习才开跑。",
             accent=TEAL)
    notes(s, "这一页是历史骨架：1847 年 Cauchy 给出确定性方法；1951 年 Robbins-Monro 证明噪声下也能收敛；"
             "1986 年反向传播解决“梯度怎么算”。三条线在 1986 年后合成现代 SGD。")


def s07_sgd(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "SGD", "两个麻烦：噪声与曲率", "一个来自“梯度估得不准”，一个来自“不同方向曲率差太多”",
           page=7, source="本讲整理")
    card(s, 0.62, 1.7, 5.9, 2.1, "麻烦一：梯度有噪声",
         "mini-batch 梯度是真实梯度的无偏估计，\n方差约与 1/B 成正比。\n"
         "噪声能帮模型跳出尖锐极小值，\n但也让损失曲线抖动、难收敛。", accent=BLUE)
    card(s, 6.8, 1.7, 5.9, 2.1, "麻烦二：曲率病态",
         "Hessian 的最大/最小特征值差很多。\n沿大曲率方向，步长稍大就震荡；\n"
         "沿小曲率方向，步长又太小、走不动。\n一个全局 η 顾此失彼。", accent=AMBER)
    formula_card(s, 0.62, 4.08, 7.4, 1.25,
                 [[("κ = λ", ""), ("max", "sub"), (" / λ", ""), ("min", "sub"),
                   ("       η < 2 / λ", ""), ("max", "sub")]],
                 label="曲率与稳定性", accent=AMBER, size=17)
    add_text(s, 8.35, 4.12, 4.2, 0.3, "两条技术路线", size=10, bold=True, color=MUTED)
    add_pill(s, 8.35, 4.5, 2.0, 0.42, "动量：改方向", fill=BLUE_L, color=BLUE, size=9.5)
    add_pill(s, 10.55, 4.5, 2.0, 0.42, "自适应：改步长", fill=AMBER_L, color=AMBER, size=9.5)
    add_text(s, 8.35, 5.05, 4.2, 0.9, "一个对抗噪声与峡谷震荡，\n一个对抗坐标尺度差异。",
             size=10, color=MUTED, line_spacing=1.3)
    takeaway(s, "后面所有方法，本质上都在分别处理这两个麻烦。", accent=AMBER)
    notes(s, "噪声和曲率是 SGD 的两大痛点。注意它们对应两种完全不同的修法：动量改的是方向（用历史平均），"
             "自适应改的是每个坐标的步长。这个二分法会一直用到 Muon。")


def s08_traj(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "实证 1", "峡谷里，SGD 在来回撞墙", "同一个二次函数，同一初始点，各自做 40 点学习率网格搜索",
           page=8, source="本地实验：f(θ)=½(θ₁²+100θ₂²)，experiment.py")
    s.shapes.add_picture(os.path.join(FIGS, "fig_traj.png"), Inches(0.62), Inches(1.62),
                         height=Inches(4.75))
    items = [("SGD", "263 步", "在窄方向来回震荡，宽方向几乎不动——步长被最大曲率卡死。", SLATE),
             ("动量", "90 步", "用历史方向抵消震荡，沿峡谷加速；但会超调、绕圈。", AMBER),
             ("Adam", "83 步", "每个坐标除以自己的梯度尺度，窄方向不再“炸”，路径接近折线。", TEAL)]
    for i, (name, steps, body, col) in enumerate(items):
        y = 1.72 + i * 1.5
        add_text(s, 7.55, y, 1.1, 0.3, name, size=11, bold=True, color=col)
        add_text(s, 8.55, y - 0.06, 1.3, 0.34, steps, size=16, bold=True, color=TEXT)
        add_text(s, 7.55, y + 0.36, 4.95, 0.8, body, size=9.5, color=MUTED, line_spacing=1.25)
        add_line(s, 7.55, y + 1.22, 12.55, y + 1.22, color=LINE, width=0.6)
    add_text(s, 7.55, 6.0, 5.0, 0.6, "注意：这条结论依赖“轴对齐”的曲率。旋转后的峡谷，逐坐标自适应的优势会变窄——这正是 Muon 的出发点。",
             size=8.2, color=SLATE, line_spacing=1.25)
    notes(s, "这张图是我们自己跑的：条件数 100 的二次函数，三个优化器各自网格搜 lr。SGD 263 步，动量 90 步，"
             "Adam 83 步。视觉上最重要的是形状：SGD 在峡谷里来回撞，Adam 的路径更直。")


def s09_lr(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "实证 2", "Adam 的鲁棒，是“归一化”换来的", "固定跑 200 步，横轴是学习率，纵轴是最终相对损失（越低越好）",
           page=9, source="本地实验，experiment.py")
    s.shapes.add_picture(os.path.join(FIGS, "fig_lr.png"), Inches(0.62), Inches(1.75),
                         height=Inches(4.4))
    items = [("SGD", "稳定区间约 0.001–0.019；超过 0.02 直接发散。", SLATE),
             ("动量", "稳定区间略宽（到 0.037），但仍有明显的“悬崖”。", AMBER),
             ("Adam", "0.001 到 3.0 都在可训练范围，最优区间很宽。", TEAL)]
    for i, (name, body, col) in enumerate(items):
        y = 1.8 + i * 1.2
        add_text(s, 7.6, y, 1.1, 0.3, name, size=11, bold=True, color=col)
        add_text(s, 7.6, y + 0.32, 4.9, 0.6, body, size=9.8, color=MUTED, line_spacing=1.25)
        add_line(s, 7.6, y + 0.95, 12.55, y + 0.95, color=LINE, width=0.6)
    add_rect(s, 7.6, 5.5, 4.95, 1.1, fill=AMBER_L, line=None, radius=0.06)
    add_text(s, 7.78, 5.6, 4.6, 0.85, "但“对 lr 鲁棒”不等于“更快”或“泛化更好”。\n"
             "鲁棒性只是降低了调参成本，别把它当成质量证明。",
             size=9, color=rgb("92400E"), line_spacing=1.3)
    notes(s, "右图是 lr 敏感性。SGD 的稳定区间很窄，Adam 跨三个数量级都能训。这解释了为什么大模型默认 AdamW："
             "不是每一步都更优，而是不容易因为 lr 设错而炸掉。但鲁棒性不等于最终质量，下一页的争议就是证据。")


def s10_momentum(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "加速", "动量：给梯度加一个“记忆”", "Polyak 1964 的 heavy-ball；Nesterov 1983 的“先看一步再算梯度”",
           page=10, source="Polyak 1964；Nesterov 1983")
    formula_card(s, 0.62, 1.72, 6.0, 1.95,
                 [[("v", "i"), ("t", "sub"), (" = β v", "i"), ("t−1", "sub"),
                   (" + g", "i"), ("t", "sub")],
                  [("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η v", "i"), ("t", "sub")]],
                 label="heavy-ball 动量", accent=BLUE, size=19,
                 note="β 通常 0.9：有效记忆约 1/(1−β)=10 步")
    add_text(s, 0.62, 3.95, 6.0, 0.3, "Nesterov：先按动量走一步，再在那一点算梯度", size=9, color=MUTED)
    add_math(s, 0.62, 4.28, 6.0, 0.5,
             [[("v", "i"), ("t", "sub"), (" = β v", "i"), ("t−1", "sub"),
               (" + ∇L(θ", ""), ("t", "sub"), (" − ηβ v", "i"), ("t−1", "sub"), (")", "")]],
             size=15, align=PP_ALIGN.LEFT)
    items = [("抵消锯齿", "相邻步方向相反时，历史动量相互抵消，震荡被压下去。", BLUE),
             ("峡谷加速", "方向一致时，动量逐步累加，等效步长变大。", TEAL),
             ("代价", "β 或 η 太大就会超调、绕圈，甚至发散。", AMBER)]
    for i, (head, body, col) in enumerate(items):
        y = 1.8 + i * 1.3
        add_text(s, 7.15, y, 1.1, 0.3, head, size=11, bold=True, color=col)
        add_text(s, 8.1, y + 0.02, 4.4, 0.75, body, size=10, color=MUTED, line_spacing=1.25)
        add_line(s, 7.15, y + 1.02, 12.55, y + 1.02, color=LINE, width=0.6)
    takeaway(s, "动量是“沿着历史方向平滑”，它不改变每个坐标的相对步长。", accent=BLUE)
    notes(s, "动量解决的是方向和震荡，不是尺度。β=0.9 意味着大约记得过去 10 步。Nesterov 的区别是"
             "先用动量探一步，再在探到的位置算梯度，理论上更“先知先觉”。")


def s11_adagrad(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "自适应 · 1", "AdaGrad：每个坐标自己的步长", "Duchi 等 2011：梯度大的坐标自动减速，梯度小的坐标自动加速",
           page=11, source="Duchi, Hazan & Singer, JMLR 2011")
    formula_card(s, 0.62, 1.72, 6.1, 1.9,
                 [[("G", "i"), ("t", "sub"), (" = G", "i"), ("t−1", "sub"),
                   (" + g", "i"), ("t", "sub"), ("²", "sup")],
                  [("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η g", "i"), ("t", "sub"), (" / (√G", ""), ("t", "sub"),
                   (" + ε)", "")]],
                 label="AdaGrad", accent=AMBER, size=19)
    add_rect(s, 0.62, 3.85, 6.1, 2.35, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.85, 3.98, 5.6, 0.3, "一个数值例子（两步梯度恒定）", size=9.5, bold=True, color=MUTED)
    add_text(s, 0.85, 4.32, 5.6, 1.8,
             "坐标 A：g=1.0，100 步后 G=100，有效步长 ∝ 0.10\n"
             "坐标 B：g=0.08，100 步后 G=0.64，有效步长 ∝ 1.25\n\n"
             "同样的 η，B 的有效步长是 A 的 12.5 倍——\n"
             "梯度小的坐标反而走得更快。",
             size=9.8, color=TEXT, line_spacing=1.3)
    items = [("优点", "不需要手动把不同特征的尺度对齐；稀疏特征很友好。", TEAL),
             ("缺点", "G 只增不减，步长单调衰减到 0；非凸深层网络里很快“走不动”。", RED),
             ("遗产", "Adam 的二阶矩 v 就是它的指数滑动平均版本。", PURPLE)]
    for i, (head, body, col) in enumerate(items):
        y = 1.8 + i * 1.25
        add_text(s, 7.0, y, 1.0, 0.3, head, size=10.5, bold=True, color=col)
        add_text(s, 7.75, y, 4.8, 0.75, body, size=9.8, color=MUTED, line_spacing=1.25)
        add_line(s, 7.0, y + 0.98, 12.55, y + 0.98, color=LINE, width=0.6)
    takeaway(s, "AdaGrad 第一次把“一个全局 η”变成“每个坐标一个有效 η”。", accent=AMBER)
    notes(s, "AdaGrad 的核心是把历史梯度平方累加进分母。数值例子说明：梯度大的坐标分母大、步长小。"
             "它的致命问题是分母只增不减，训练后期步长趋近于零。这直接催生了 RMSProp。")


def s12_rmsprop(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "自适应 · 2", "RMSProp：把“累加”换成“滑动平均”", "Hinton 2012 的 Coursera 讲义，从未正式发表，却成了 Adam 的一半",
           page=12, source="Hinton, Coursera 讲义 2012（未正式发表）")
    formula_card(s, 0.62, 1.72, 6.0, 1.9,
                 [[("v", "i"), ("t", "sub"), (" = β v", "i"), ("t−1", "sub"),
                   (" + (1−β) g", "i"), ("t", "sub"), ("²", "sup")],
                  [("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η g", "i"), ("t", "sub"), (" / (√v", ""), ("t", "sub"),
                   (" + ε)", "")]],
                 label="RMSProp", accent=TEAL, size=19, note="β 通常 0.9；分母是最近一段时间的均方梯度")
    rows = [("历史梯度", "全部累加（只增）", "指数滑动平均（可忘）"),
            ("步长趋势", "单调衰减到 0", "跟随近期梯度，不消失"),
            ("适用", "凸问题 / 稀疏特征", "非平稳、深度网络"),
            ("发表", "JMLR 2011", "讲义 2012，未正式发表")]
    add_table(s, 7.0, 1.72, 5.55, 2.6, [["对比", "AdaGrad", "RMSProp"]] + [list(r) for r in rows],
              [1.0, 2.1, 2.45], body_size=9, header_size=9, row_height=0.5)
    add_rect(s, 7.0, 4.75, 5.55, 1.3, fill=TEAL_L, line=None, radius=0.06)
    add_text(s, 7.2, 4.88, 5.2, 0.3, "一句话", size=8.5, bold=True, color=TEAL)
    add_text(s, 7.2, 5.15, 5.2, 0.75, "Adam = RMSProp 的二阶矩\n+ 动量的一阶矩 + 偏差修正",
             size=12.5, bold=True, color=TEXT, line_spacing=1.25)
    takeaway(s, "RMSProp 修好了“步长消失”，但还没有把动量和偏差修正接上。", accent=TEAL)
    notes(s, "RMSProp 只改了一处：把累加换成指数滑动平均，于是步长不会单调消失。它没有正式论文，"
             "但工程影响极大。把 RMSProp 的二阶矩、动量的 momentum、再加偏差修正，就是 Adam。")


def s13_adam(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "自适应 · 3", "Adam：动量 + 二阶矩 + 偏差修正", "Kingma & Ba，arXiv 2014-12，ICLR 2015；至今仍是默认基线",
           page=13, source="Kingma & Ba, ICLR 2015")
    formula_card(s, 0.62, 1.66, 7.35, 3.55,
                 [[("m", "i"), ("t", "sub"), (" = β₁ m", "i"), ("t−1", "sub"),
                   (" + (1−β₁) g", "i"), ("t", "sub")],
                  [("v", "i"), ("t", "sub"), (" = β₂ v", "i"), ("t−1", "sub"),
                   (" + (1−β₂) g", "i"), ("t", "sub"), ("²", "sup")],
                  [("m̂", "i"), ("t", "sub"), (" = m", "i"), ("t", "sub"),
                   (" / (1−β₁", ""), ("t", "sup"), (")     v̂", "i"), ("t", "sub"),
                   (" = v", "i"), ("t", "sub"), (" / (1−β₂", ""), ("t", "sup"), (")", "")],
                  [("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η m̂", "i"), ("t", "sub"), (" / (√v̂", ""), ("t", "sub"),
                   (" + ε)", "")]],
                 label="Adam", accent=TEAL, size=16, line_spacing=1.5)
    add_text(s, 8.25, 1.72, 4.4, 0.3, "默认超参（原论文）", size=9, bold=True, color=MUTED)
    params = [("β₁", "0.9"), ("β₂", "0.999"), ("ε", "1e-8"), ("lr", "1e-3")]
    for i, (k, v) in enumerate(params):
        x = 8.25 + (i % 2) * 2.2
        y = 2.08 + (i // 2) * 0.72
        add_rect(s, x, y, 2.0, 0.6, fill=WHITE, line=LINE, radius=0.08)
        add_text(s, x + 0.12, y + 0.09, 0.5, 0.24, k, size=9, bold=True, color=TEAL)
        add_text(s, x + 0.62, y + 0.06, 1.25, 0.3, v, size=13, bold=True, color=TEXT)
    add_text(s, 8.25, 3.55, 4.4, 0.3, "三个部件各管一件事", size=9, bold=True, color=MUTED)
    parts = [("一阶矩", "方向平滑，像动量"), ("二阶矩", "每坐标步长，像 RMSProp"),
             ("偏差修正", "把早期被 0 拉低的估计掰回来")]
    for i, (k, v) in enumerate(parts):
        y = 3.9 + i * 0.55
        add_text(s, 8.25, y, 1.1, 0.26, k, size=9.5, bold=True, color=TEXT)
        add_text(s, 9.35, y, 3.4, 0.26, v, size=9.2, color=MUTED)
    takeaway(s, "Adam 把“方向”和“每坐标步长”都做了平滑估计，再加一个早期校正。", accent=TEAL)
    notes(s, "Adam 的公式看起来多，其实三件事：一阶矩平滑方向，二阶矩给每个坐标一个步长，偏差修正处理"
             "从 0 初始化带来的早期偏差。默认超参至今几乎没变。")


def s14_bias(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "Adam 细节", "为什么前几步要“除以 1−βᵗ”", "m 和 v 都从 0 开始，早期估计被 0 拉低；两者相除后偏差方向相反",
           page=14, source="Kingma & Ba 2015；本讲推导")
    s.shapes.add_picture(os.path.join(FIGS, "fig_bias.png"), Inches(0.62), Inches(1.72),
                         width=Inches(6.1))
    add_text(s, 0.8, 5.05, 5.8, 0.3, "修正系数随 t 趋近 1：训练越久，修正越可忽略。", size=8.5, color=MUTED)
    formula_card(s, 6.95, 1.72, 5.6, 1.25,
                 [[("m̂", "i"), ("t", "sub"), (" = m", "i"), ("t", "sub"),
                   (" / (1−β₁", ""), ("t", "sup"), (")        v̂", "i"), ("t", "sub"),
                   (" = v", "i"), ("t", "sub"), (" / (1−β₂", ""), ("t", "sup"), (")", "")]],
                 accent=TEAL, size=15)
    add_text(s, 6.95, 3.15, 5.6, 0.3, "首步到底差多少？令 g 恒定、忽略 ε：", size=10, bold=True, color=TEXT)
    add_math(s, 6.95, 3.5, 5.6, 0.55,
             [[("m₁/(√v₁) = 0.1g / (0.0316|g|) ≈ 3.16 · sign(g)", "")]],
             size=13, align=PP_ALIGN.LEFT)
    add_text(s, 6.95, 4.18, 5.6, 1.5,
             "m 被低估为 0.1g，√v 被低估为 0.0316|g|；\n"
             "一阶矩被低估得更多，比值反而放大 3.16 倍。\n"
             "除以 (1−β₁ᵗ) 与 (1−β₂ᵗ) 后，首步回到 1·sign(g)，\n"
             "与后续步长尺度一致。",
             size=9.8, color=MUTED, line_spacing=1.35)
    takeaway(s, "偏差修正不是“让早期步长变大”，而是把被 0 拉偏的比值拉回 1。", accent=TEAL)
    notes(s, "这里有个常见误解：以为不做修正早期步长会太小。实际算一下，首步比值约 3.16 倍，是偏大。"
             "因为 m 和 v 被 0 拉低的程度不同，相除后反而放大。修正后首步回到 sign(g)，量级正确。")


def s15_adam_why(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "Adam", "它到底解决了什么", "三个性质解释了大模型为什么默认选它——也解释了它的边界",
           page=15, source="Kingma & Ba 2015；本讲整理")
    cards3 = [("坐标尺度不变", "g → c·g 时，m 与 √v 同比例变化，\n更新量近似不变。\n不同特征尺度不用手工对齐。", TEAL),
              ("步长有界", "|Δθ| ≈ η · |m̂|/(√v̂+ε)。\n单步更新被 η 量级约束，\n不容易一步炸飞。", BLUE),
              ("稀疏友好", "很少更新的坐标 v 小，\n一旦有梯度，有效步长更大。\nEmbedding / 推荐特征受益。", PURPLE)]
    for i, (head, body, col) in enumerate(cards3):
        card(s, 0.62 + i * 4.02, 1.72, 3.86, 2.35, head, body, accent=col, body_size=9.8)
    add_rect(s, 0.62, 4.32, 5.9, 1.85, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.85, 4.45, 5.4, 0.3, "典型使用场景", size=9.5, bold=True, color=GREEN)
    add_text(s, 0.85, 4.78, 5.45, 1.3,
             "Transformer / LLM 预训练；稀疏特征与推荐；\n"
             "目标非平稳、梯度尺度差异大的任务；\n"
             "需要快速原型的实验。",
             size=9.6, color=TEXT, line_spacing=1.3)
    add_rect(s, 6.8, 4.32, 5.9, 1.85, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 7.03, 4.45, 5.4, 0.3, "但别把它当“万能”", size=9.5, bold=True, color=RED)
    add_text(s, 7.03, 4.78, 5.45, 1.3,
             "不保证收敛（Reddi 2018 有反例）；\n"
             "泛化未必优于调好的 SGD+momentum；\n"
             "L2 正则在 Adam 下会“变味”（下一页）。",
             size=9.6, color=TEXT, line_spacing=1.3)
    takeaway(s, "Adam 解决的是“尺度”，不是“泛化”，也不是“正则”。", accent=TEAL)
    notes(s, "三个性质：尺度不变、步长有界、稀疏友好。这三条让 Adam 成为默认基线。但右边三条边界同样重要，"
             "接下来的两页就是两次危机：泛化和收敛。")


def s16_wilson(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "危机 1", "训练更快，测试一定更好吗？", "Wilson 等 2017 年的论文，给“自适应一定更好”泼了一盆冷水",
           page=16, source="Wilson et al., NeurIPS 2017")
    add_rect(s, 0.62, 1.72, 7.2, 2.5, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.95, 1.9, 0.8, 0.5, "“", size=34, bold=True, color=TEAL)
    add_text(s, 1.45, 2.02, 6.0, 1.7,
             "在若干视觉任务上，把学习率调到最优后，\nSGD + momentum 的测试精度不输甚至优于\n自适应方法——训练集上的速度优势，\n没有转化为泛化优势。",
             size=13, color=TEXT, line_spacing=1.45)
    add_text(s, 1.45, 3.72, 5.9, 0.28, "（论文结论的转述，非原文引用）", size=8, color=SLATE)
    add_text(s, 0.62, 4.48, 7.2, 0.3, "作者的三个观察", size=10, bold=True, color=MUTED)
    obs = ["在 CIFAR-10 / ImageNet 上做公平调参对比；",
           "自适应方法找到的解，泛化间隙更大；",
           "“训练更快”与“泛化更好”是两个目标。"]
    for i, t in enumerate(obs):
        add_text(s, 0.62, 4.85 + i * 0.42, 7.2, 0.3, "· " + t, size=9.8, color=TEXT)
    add_rect(s, 8.1, 1.72, 4.6, 3.5, fill=AMBER_L, line=None, radius=0.06)
    add_text(s, 8.32, 1.88, 4.2, 0.3, "但这不等于 Adam 出局", size=10, bold=True, color=rgb("92400E"))
    add_text(s, 8.32, 2.25, 4.2, 2.7,
             "2019 年 AdamW 用“解耦 weight decay”\n"
             "把正则从自适应分母里拿出来，\n"
             "在图像分类上追平了 SGD+momentum。\n\n"
             "真正的问题不是“自适应”，\n"
             "而是“自适应 + L2”这个组合。",
             size=9.8, color=rgb("78350F"), line_spacing=1.35)
    takeaway(s, "优化速度与泛化，是两个目标；Adam 的第一版把正则和自适应绑在了一起。", accent=AMBER)
    notes(s, "Wilson 2017 的结论常被简化为“Adam 泛化差”。更准确的说法是：在公平调参下，自适应方法的训练优势"
             "不一定转化为测试优势。这直接指向下一页和 AdamW：问题可能出在正则与自适应的耦合。")


def s17_reddi(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "危机 2", "Adam 不保证收敛", "Reddi 等 2018 构造了反例：在凸问题上，Adam 也可能不收敛",
           page=17, source="Reddi et al., ICLR 2018")
    add_text(s, 0.62, 1.72, 6.2, 0.3, "反例的直觉", size=10, bold=True, color=MUTED)
    add_text(s, 0.62, 2.08, 6.2, 1.6,
             "Adam 的分母是滑动平均，\n它可以“忘掉”过去很大的二阶矩。\n"
             "当历史信息被忘掉，有效步长会突然变大，\n"
             "在特定梯度序列下反复横跳，无法收敛。",
             size=10.2, color=TEXT, line_spacing=1.35)
    formula_card(s, 0.62, 3.85, 6.2, 1.55,
                 [[("v̂", "i"), ("t", "sub"), (" = max(v̂", "i"), ("t−1", "sub"),
                   (", v", "i"), ("t", "sub"), (")", "")]],
                 label="AMSGrad 的修法", accent=BLUE, size=20,
                 note="用历史最大二阶矩，保证分母不下降")
    add_text(s, 0.62, 5.6, 6.2, 0.8, "代价：更保守、有效步长更小；在大模型里通常不直接用，\n但 warmup / grad clip 起了类似的兜底作用。",
             size=8.8, color=MUTED, line_spacing=1.3)
    add_rect(s, 7.2, 1.72, 5.5, 2.2, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 7.43, 1.86, 5.0, 0.3, "工程上真正在用的兜底", size=9.5, bold=True, color=GREEN)
    add_text(s, 7.43, 2.2, 5.05, 1.55,
             "· 线性 warmup：先小步走，避开早期大方差\n"
             "· 梯度裁剪：单步更新设上限\n"
             "· 监控 loss spike，必要时回滚 checkpoint",
             size=9.5, color=TEXT, line_spacing=1.4)
    add_rect(s, 7.2, 4.12, 5.5, 1.4, fill=BLUE_L, line=None, radius=0.06)
    add_text(s, 7.43, 4.25, 5.0, 0.28, "一句话", size=8.5, bold=True, color=BLUE)
    add_text(s, 7.43, 4.55, 5.05, 0.85, "Adam 是“经验上极稳”，\n不是“数学上无条件收敛”。",
             size=12, bold=True, color=TEXT, line_spacing=1.3)
    takeaway(s, "理论反例提醒我们：Adam 的稳定性来自工程配方，不只是公式。", accent=BLUE)
    notes(s, "Reddi 2018 的反例说明 Adam 的滑动平均分母可能忘掉历史，导致不收敛。AMSGrad 用 max 修，但工程上"
             "更常用 warmup 和 grad clip 兜底。这一页不是让你弃用 Adam，而是别把“能训”当成“保证收敛”。")


def s18_decouple(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "关键推导", "weight decay ≠ L2", "对 SGD 等价，对 Adam 不等价——这是 AdamW 的全部起点",
           page=18, source="Loshchilov & Hutter, ICLR 2019")
    formula_card(s, 0.62, 1.72, 5.9, 2.05,
                 [[("g̃", ""), ("t", "sub"), (" = g", "i"), ("t", "sub"),
                   (" + λ θ", "i"), ("t", "sub")],
                  [("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η · Adam(g̃", ""), ("t", "sub"), (")", "")]],
                 label="耦合式：L2 正则进入梯度", accent=RED, size=16,
                 note="λθ 会进入 m 和 v，再被自适应分母归一化")
    formula_card(s, 6.8, 1.72, 5.9, 2.05,
                 [[("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η · Adam(g", ""), ("t", "sub"), (")", "")],
                  [("        − η λ θ", "i"), ("t", "sub")]],
                 label="解耦式：正则单独减", accent=GREEN, size=16,
                 note="衰减量只与 θ 成正比，与 v 无关")
    add_text(s, 0.62, 4.08, 12.1, 0.3, "为什么对 SGD 等价、对 Adam 不等价", size=10, bold=True, color=MUTED)
    rows = [("SGD", "θ ← (1−ηλ)θ − ηg", "λθ 只是一个常数缩放，等价"),
            ("Adam", "λθ 先被 m/v 归一化", "历史 v 大的参数，衰减被削弱；v 小的参数，衰减被放大")]
    for i, (who, mech, result) in enumerate(rows):
        y = 4.48 + i * 0.82
        add_text(s, 0.62, y, 1.0, 0.3, who, size=10.5, bold=True, color=(TEAL if i == 0 else RED))
        add_text(s, 1.55, y, 4.0, 0.3, mech, size=9.6, color=TEXT)
        add_text(s, 5.7, y, 7.0, 0.6, result, size=9.6, color=MUTED, line_spacing=1.2)
        add_line(s, 0.62, y + 0.62, 12.6, y + 0.62, color=LINE, width=0.6)
    takeaway(s, "L2 把正则塞进梯度，Adam 又把梯度归一化——正则强度于是被“偷偷”改了。", accent=RED)
    notes(s, "这是全篇最重要的一页。L2 是把 λθ 加进梯度；SGD 下等价于每一步乘 (1−ηλ)。但 Adam 会把这个 λθ 也"
             "放进 m 和 v 归一化，导致衰减强度依赖历史梯度。解法很简单：把正则拿出来单独减。")


def s19_adamw(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "AdamW", "把正则从自适应分母里拿出来", "Loshchilov & Hutter：arXiv 2017-11，ICLR 2019",
           page=19, source="Loshchilov & Hutter, ICLR 2019")
    formula_card(s, 0.62, 1.72, 12.09, 1.55,
                 [[("θ", "i"), ("t+1", "sub"), (" = θ", "i"), ("t", "sub"),
                   (" − η · m̂", "i"), ("t", "sub"), (" / (√v̂", ""), ("t", "sub"),
                   (" + ε)  −  η λ θ", "i"), ("t", "sub")]],
                 label="AdamW 的一次更新", accent=GREEN, size=18,
                 note="前一项是 Adam 的自适应更新，后一项是解耦 weight decay")
    cards3 = [("只差一行", "把 λθ 从梯度里挪到更新末尾；\n实现上就是参数先乘 (1−ηλ)。", GREEN),
              ("独立可调", "lr 控制自适应步长，wd 控制收缩；\n两者不再互相纠缠。", TEAL),
              ("默认值", "PyTorch AdamW 的 weight_decay\n默认 0.01；Adam 的默认是 0。", BLUE)]
    for i, (head, body, col) in enumerate(cards3):
        card(s, 0.62 + i * 4.02, 3.58, 3.86, 1.75, head, body, accent=col, body_size=9.6)
    add_text(s, 0.62, 5.62, 12.1, 0.55, "注意：解耦之后，“weight decay 系数”不再等于 L2 系数；换实现时要重新调 λ，不能直接照搬。",
             size=9.2, color=MUTED)
    takeaway(s, "AdamW 不是新优化器，而是把 Adam 的正则接法修正了。", accent=GREEN)
    notes(s, "AdamW 的公式只差最后一项。实现上，很多框架就是先做一次 θ *= (1−lr*wd)，再做 Adam 更新。"
             "关键细节：解耦后的 wd 与 L2 的 λ 不等价，迁移时要重调。")


def s20_evidence(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "证据", "15%：不是玄学，是解耦的收益", "同一篇论文里，AdamW 在默认 lr 下把测试误差相对降低 15%",
           page=20, source="Loshchilov & Hutter, ICLR 2019, §1 与 §5（15% 在引言与实验部分）")
    add_rect(s, 0.62, 1.75, 3.6, 3.2, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.9, 1.95, 3.0, 0.3, "相对测试误差改进", size=8.5, bold=True, color=MUTED)
    add_text(s, 0.85, 2.25, 3.1, 1.0, "15%", size=58, bold=True, color=GREEN)
    add_text(s, 0.9, 3.35, 3.05, 1.3, "CIFAR-10 与 ImageNet32x32\n默认 lr=1e-3，与调好的\nAdam+L2 对比",
             size=9.2, color=MUTED, line_spacing=1.3)
    rows = [("数据集", "CIFAR-10 / ImageNet32x32（降采样版，不是完整 ImageNet）"),
            ("对比对象", "Adam + L2（耦合式 weight decay）"),
            ("关键条件", "默认 lr=1e-3，不做额外调参"),
            ("更大结论", "解耦后，Adam 可与 SGD+momentum 竞争")]
    for i, (k, v) in enumerate(rows):
        y = 1.8 + i * 1.12
        add_text(s, 4.55, y, 1.15, 0.28, k, size=8.8, bold=True, color=TEAL)
        add_text(s, 5.75, y - 0.02, 6.9, 0.7, v, size=10, color=TEXT, line_spacing=1.25)
        add_line(s, 4.55, y + 0.78, 12.6, y + 0.78, color=LINE, width=0.6)
    add_text(s, 0.62, 5.15, 3.6, 0.9, "注：15% 是相对改进，\n不是绝对准确率提升 15 个点。", size=8.2, color=RED,
             line_spacing=1.25)
    takeaway(s, "正则与自适应解耦，Adam 才能和 SGD+momentum 同台。", accent=GREEN)
    notes(s, "15% 是相对测试误差改进，不是准确率涨 15 个点。条件也要说清楚：默认 lr、CIFAR-10 和 ImageNet32x32。"
             "论文更大的结论是 AdamW 让 Adam 可以和 SGD+momentum 竞争，这为后来 LLM 默认 AdamW 铺了路。")


def s21_llama(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "工业配方", "Llama 3 405B 的 AdamW 设置", "优化器只是一行；warmup、衰减、wd 一起决定能不能训完",
           page=21, source="Llama 3 Herd of Models, 2024, §3.4")
    data = [["项目", "取值", "说明"],
            ["优化器", "AdamW", "β 值正文未给出"],
            ["峰值学习率", "8e-5", "405B 模型"],
            ["warmup", "8000 步", "线性预热"],
            ["衰减", "cosine → 8e-7", "总 1.2M 步"],
            ["weight decay", "0.1", "解耦式"]]
    add_table(s, 0.62, 1.72, 7.5, 3.7, data, [1.7, 2.2, 3.6],
              body_size=9.5, header_size=9.5, row_height=0.58)
    add_text(s, 0.62, 5.55, 7.5, 0.55, "坦白说：论文没有给出 β₁/β₂，别把默认 0.9/0.999 当成论文事实。",
             size=8.2, color=RED)
    notes_box = [("峰值 lr 很小", "405B 模型用 8e-5，比小模型低一到两个数量级。"),
                 ("warmup 很长", "8000 步，先用小步把二阶矩估计稳下来。"),
                 ("wd 不小", "0.1，解耦后才敢用这么强的收缩。")]
    for i, (h, b) in enumerate(notes_box):
        y = 1.8 + i * 1.35
        add_text(s, 8.5, y, 4.1, 0.3, h, size=10.5, bold=True, color=TEAL)
        add_text(s, 8.5, y + 0.32, 4.15, 0.7, b, size=9.4, color=MUTED, line_spacing=1.25)
        add_line(s, 8.5, y + 1.05, 12.6, y + 1.05, color=LINE, width=0.6)
    takeaway(s, "大模型训练是“优化器 + 调度 + 正则 + 裁剪”的组合拳，别只盯一行。", accent=TEAL)
    notes(s, "以 Llama 3 405B 为例：AdamW、峰值 lr 8e-5、8000 步 warmup、cosine 到 8e-7、wd 0.1。"
             "注意论文正文没有给 β，别替它编。这一页想说明：优化器不是孤立的一行，配套调度同样关键。")


def s22_limit(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "边界", "AdamW 看不见的东西", "它逐元素地看参数，但很多参数天然是矩阵——矩阵的几何被抹掉了",
           page=22, source="Jordan 2024；本讲整理")
    cards3 = [("逐元素", "AdamW 对每个元素独立缩放；\n同一个矩阵的不同行、不同列\n没有“整体”的概念。", BLUE),
              ("近似低秩", "矩阵梯度/动量的奇异值衰减很快；\n逐元素缩放不改变谱形，\n小奇异方向几乎不动。", AMBER),
              ("混合参数", "embedding、attention、分类头\n形状与稀疏性差异大；\n一套超参很难同时最优。", PURPLE)]
    for i, (head, body, col) in enumerate(cards3):
        card(s, 0.62 + i * 4.02, 1.72, 3.86, 2.35, head, body, accent=col, body_size=9.7)
    add_rect(s, 0.62, 4.45, 12.09, 1.05, fill=NAVY, line=None, radius=0.06)
    add_text(s, 0.95, 4.58, 11.4, 0.8,
             "如果更新本身是一个矩阵，为什么不直接对它的奇异值做预条件？",
             size=18, bold=True, color=WHITE)
    add_text(s, 0.62, 5.7, 12.1, 0.45, "这就是 Muon 的出发点：把“逐元素缩放”换成“矩阵谱上的正交化”。",
             size=10, color=MUTED)
    takeaway(s, "AdamW 的盲区不是“不够快”，而是“看不见矩阵的整体结构”。", accent=AMBER)
    notes(s, "这一页是转场。AdamW 很强，但它是逐元素的。很多参数是矩阵，矩阵的奇异值谱有结构。"
             "如果更新近似低秩，逐元素缩放就不会去动那些小奇异方向。Muon 正是从这里切入。")


def s23_muon(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "Muon", "把预条件从“元素”换成“矩阵”", "Keller Jordan，2024-10 发布，2024-12 博客正式介绍",
           page=23, source="Jordan, kellerjordan.github.io/posts/muon/, 2024-12-08")
    add_rect(s, 0.62, 1.72, 5.9, 3.2, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.85, 1.86, 5.4, 0.3, "它是什么", size=9.5, bold=True, color=AMBER)
    add_text(s, 0.85, 2.2, 5.45, 2.55,
             "· 只用于 2D hidden 矩阵参数\n"
             "· 先做 Nesterov 动量，再做 Newton–Schulz 正交化\n"
             "· embedding、最终分类头、标量仍用 AdamW\n"
             "· 不是“更好的 Adam”，而是换了一个预条件对象",
             size=9.8, color=TEXT, line_spacing=1.5)
    add_text(s, 6.95, 1.78, 5.6, 0.3, "与 AdamW 的一句话差别", size=9, bold=True, color=MUTED)
    add_math(s, 6.95, 2.12, 5.6, 0.55, [[("AdamW：逐元素除以 √v̂", "")]], size=14, align=PP_ALIGN.LEFT)
    add_math(s, 6.95, 2.65, 5.6, 0.55, [[("Muon：把整个矩阵的奇异值压平", "")]], size=14, align=PP_ALIGN.LEFT)
    add_text(s, 6.95, 3.35, 5.6, 1.6,
             "前者问“每个元素该走多大”，\n后者问“这个矩阵的每个方向该走多大”。\n\n"
             "对矩阵参数，后者才是几何上正确的问法。",
             size=9.8, color=MUTED, line_spacing=1.4)
    steps = [("2024-10", "Muon 发布", AMBER), ("2024-12", "博客详细介绍", AMBER),
             ("2025-02", "Moonshot 规模化", BLUE), ("2025-07", "Kimi K2 采用", PURPLE)]
    for i, (d, t, col) in enumerate(steps):
        x = 0.62 + i * 3.05
        add_circle(s, x, 5.35, 0.12, fill=col, line=None)
        if i < 3:
            add_line(s, x + 0.12, 5.41, x + 2.93, 5.41, color=LINE, width=0.8)
        add_text(s, x, 5.6, 1.5, 0.25, d, size=8.5, bold=True, color=col)
        add_text(s, x, 5.86, 2.6, 0.3, t, size=9.5, color=TEXT)
    takeaway(s, "Muon 换的不是“步子”，而是“在哪个空间里量步子”。", accent=AMBER)
    notes(s, "Muon 只处理 2D hidden 矩阵，embedding 和 head 还是 AdamW。它的核心是把动量矩阵的奇异值压平，"
             "让所有方向获得近似相同的步长。时间线：2024-10 发布，12 月博客，2025 年 Moonshot 规模化和 Kimi K2。")


def s24_insight(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "核心洞察", "矩阵更新，几乎总是低秩的", "梯度是外积的和；动量矩阵的奇异值衰减很快，逐元素缩放看不见这件事",
           page=24, source="Jordan 2024；本讲绘制")
    add_rect(s, 0.62, 1.72, 6.1, 3.35, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.85, 1.86, 5.6, 0.3, "奇异值谱示意", size=9.5, bold=True, color=MUTED)
    add_text(s, 0.85, 2.2, 2.7, 0.25, "AdamW 更新", size=8.5, color=SLATE)
    add_text(s, 3.6, 2.2, 2.7, 0.25, "Muon 更新", size=8.5, color=AMBER)
    heights_a = [1.65, 1.15, 0.75, 0.45, 0.28, 0.16, 0.09]
    heights_m = [1.45, 1.42, 1.4, 1.38, 1.36, 1.34, 1.32]
    for i in range(7):
        x = 0.9 + i * 0.34
        add_rect(s, x, 4.55 - heights_a[i], 0.24, heights_a[i], fill=SLATE, line=None,
                 shape_type=MSO_SHAPE.RECTANGLE)
        x2 = 3.65 + i * 0.34
        add_rect(s, x2, 4.55 - heights_m[i], 0.24, heights_m[i], fill=AMBER, line=None,
                 shape_type=MSO_SHAPE.RECTANGLE)
    add_line(s, 0.82, 4.58, 5.95, 4.58, color=LINE, width=0.8)
    add_text(s, 0.85, 4.7, 2.6, 0.3, "奇异值序号 →", size=8, color=SLATE)
    add_text(s, 3.65, 4.7, 2.4, 0.3, "几乎全部拉平", size=8, color=AMBER)
    items = [("梯度是外积的和", "一层矩阵的梯度由 batch 中样本的外积叠加，\n天然集中在少数方向。", TEAL),
             ("AdamW 不改谱形", "逐元素除以 √v 只改尺度，\n不会把小的奇异值抬起来。", BLUE),
             ("Muon 直接压谱", "NS 正交化把非零奇异值压到 1 附近，\n小方向也获得满步长。", AMBER)]
    for i, (head, body, col) in enumerate(items):
        y = 1.78 + i * 1.35
        add_text(s, 6.95, y, 5.6, 0.3, head, size=10.5, bold=True, color=col)
        add_text(s, 6.95, y + 0.32, 5.65, 0.75, body, size=9.5, color=MUTED, line_spacing=1.25)
    add_text(s, 6.95, 5.95, 5.6, 0.3, "博客原话：the update is approximately low rank。", size=8, color=SLATE, italic=True)
    takeaway(s, "Muon 的洞见：矩阵更新的问题不是“每个元素多大”，而是“每个方向多大”。", accent=AMBER)
    notes(s, "左边是示意图：AdamW 的更新谱衰减很快，Muon 把它拉平。右边解释原因：梯度是外积和，天然低秩；"
             "逐元素缩放不改谱形。注意“近似低秩”是博客的原话，不是严格定理。")


def s25_algo(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "算法", "Muon 的一次更新", "伪代码只有五行，难的是分布式实现和超参对齐",
           page=25, source="Jordan 2024；Moonshot 2025 的规模化版本")
    code = [("# 只对 2D hidden 矩阵参数", rgb("94A3B8")),
            ("for W in matrix_params:", rgb("E2E8F0")),
            ("    G = grad(W)", rgb("E2E8F0")),
            ("    B = mu * B + G          # 动量", rgb("E2E8F0")),
            ("    G = G + mu * B          # Nesterov", rgb("E2E8F0")),
            ("    O = NS5(G)              # 正交化", rgb("5EEAD4")),
            ("    W = W - lr * (0.2 * O * sqrt(max(A,B))", rgb("FCD34D")),
            ("                   + wd * W)", rgb("FCD34D"))]
    code_card(s, 0.62, 1.72, 7.0, 3.55, code, title="Muon update（Moonshot 缩放版）", size=11)
    ann = [("① 动量 + Nesterov", "和 SGD 动量一样，先把方向平滑。", TEAL),
           ("② NS5 正交化", "5 步 Newton–Schulz，把奇异值压平。", AMBER),
           ("③ 缩放", "0.2·√max(A,B) 把 update RMS 对齐 AdamW。", BLUE),
           ("④ 非矩阵参数", "embedding / head / 标量继续用 AdamW。", PURPLE)]
    for i, (head, body, col) in enumerate(ann):
        y = 1.78 + i * 0.98
        add_text(s, 7.95, y, 4.6, 0.28, head, size=9.8, bold=True, color=col)
        add_text(s, 7.95, y + 0.28, 4.65, 0.5, body, size=8.8, color=MUTED, line_spacing=1.2)
    add_text(s, 0.62, 5.45, 7.0, 0.7, "NS 的额外 FLOP：NanoGPT 约 0.7%，Llama 405B 约 0.5%——远小于它省下的步数。",
             size=8.5, color=MUTED, line_spacing=1.25)
    takeaway(s, "Muon 的伪代码很短，工程难点在分布式 NS 通信与缩放对齐。", accent=AMBER)
    notes(s, "伪代码五行：动量、Nesterov、NS5、缩放。缩放系数 0.2·√max(A,B) 是 Moonshot 版本，用来把 update RMS"
             "对齐到 AdamW 的 0.2。非矩阵参数继续用 AdamW。NS 的 FLOP 开销不到 1%。")


def s26_ns(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "数学", "Newton–Schulz：不用 SVD 也能正交化", "目标是最近的正交矩阵；五次多项式迭代，5 步就够",
           page=26, source="Jordan 2024；本讲 Toy 实验")
    s.shapes.add_picture(os.path.join(FIGS, "fig_muon.png"), Inches(0.85), Inches(1.56),
                         width=Inches(11.4))
    cards3 = [("目标", "对 G=USVᵀ，求 UVᵀ：\n最近的正交（半正交）矩阵。"),
              ("迭代", "X ← aX + (bXXᵀ + c(XXᵀ)²)X\n系数组 (3.4445, −4.7750, 2.0315)。"),
              ("效果", "5 步后奇异值进入 [0.68, 1.13]；\nε≈0.3 的偏差不伤 loss。")]
    for i, (head, body) in enumerate(cards3):
        x = 0.62 + i * 4.05
        add_rect(s, x, 5.62, 3.9, 0.9, fill=WHITE, line=LINE, radius=0.05)
        add_text(s, x + 0.15, 5.70, 0.9, 0.25, head, size=8.5, bold=True, color=AMBER)
        add_text(s, x + 0.95, 5.68, 2.85, 0.78, body, size=8.2, color=TEXT, line_spacing=1.18)
    notes(s, "NS 迭代不需要 SVD：五次多项式把 X 的奇异值往 1 推。左图是 64×32 的合成矩阵，右图是标量迭代。"
             "5 步后奇异值落在 0.68 到 1.13 之间，论文说不影响 loss。")
    takeaway(s, "Muon 的“正交化”不是精确 SVD，而是 5 步多项式近似——够用且便宜。", accent=AMBER, y=6.6)


def s27_evidence2(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "证据", "三条可复现的战绩", "小规模 speedrun、NanoGPT 加速、1.5B 模型——都不是“只快一点”",
           page=27, source="Jordan 2024（Muon 博客）")
    data = [("CIFAR-10 speedrun", "3.3→2.6", "达到 94% 的 A100-seconds", AMBER),
            ("NanoGPT", "1.35×", "FineWeb 上 3.28 val loss 的加速", TEAL),
            ("1.5B 模型", "10 vs 13.3", "8×H100-hours，达 GPT-2 XL HellaSwag", BLUE)]
    for i, (label, value, note_, col) in enumerate(data):
        add_metric(s, 0.62 + i * 4.02, 1.72, 3.86, 1.55, label, value, note_, accent=col,
                   value_size=22)
    add_text(s, 0.62, 3.55, 12.1, 0.3, "这些数字的共同点", size=10, bold=True, color=MUTED)
    items = [("同一个模型、同一份数据", "只换优化器，加速来自步数更少，而不是模型更大。"),
             ("可复现", "代码与超参公开；NanoGPT speedrun 是社区公认的硬基准。"),
             ("有边界", "都是预训练；微调、RL、embedding 未证明。")]
    for i, (head, body) in enumerate(items):
        y = 3.95 + i * 0.82
        add_text(s, 0.62, y, 2.6, 0.3, head, size=9.8, bold=True, color=TEXT)
        add_text(s, 3.1, y, 9.4, 0.55, body, size=9.5, color=MUTED)
        add_line(s, 0.62, y + 0.6, 12.6, y + 0.6, color=LINE, width=0.6)
    add_text(s, 0.62, 6.35, 12.1, 0.3, "截至 2024-12 博客：12 次 NanoGPT speedrun 记录由 7 位研究者用 Muon 保持。",
             size=8.5, color=SLATE)
    notes(s, "三条证据：CIFAR-10 speedrun 从 3.3 降到 2.6 A100 秒；NanoGPT 1.35 倍；1.5B 模型 10 vs 13.3 个"
             "8×H100 小时。它们都是预训练场景，别外推到微调或 RL。")


def s28_scale(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "规模化", "Moonshot：把 Muon 推到 3B/16B MoE", "两件事让它在大模型上成立：加 weight decay、按参数对齐 update scale",
           page=28, source="Moonshot AI, arXiv 2502.16982, 2025-02")
    formula_card(s, 0.62, 1.72, 7.3, 1.6,
                 [[("W ← W − η ( 0.2 · O · √max(A,B) + λ W )", "")]],
                 label="规模化后的更新式", accent=BLUE, size=15,
                 note="O 是正交化后的更新；A、B 是矩阵维度")
    keys = [("加 weight decay", "Muon 原始版本没有 wd；规模化时必须加，否则范数漂移。"),
            ("对齐 update RMS", "把 RMS 对齐 AdamW 的 0.2–0.4，取 0.2；否则 lr 不可迁移。")]
    for i, (h, b) in enumerate(keys):
        y = 3.55 + i * 0.85
        add_text(s, 0.62, y, 2.0, 0.3, h, size=10, bold=True, color=BLUE)
        add_text(s, 2.7, y - 0.02, 5.2, 0.6, b, size=9.2, color=MUTED, line_spacing=1.2)
    add_text(s, 0.62, 5.5, 7.3, 0.4, "结论：compute-optimal 对比下约 2× 计算效率。", size=10, bold=True, color=GREEN)
    stats = [("约 2×", "计算效率", GREEN), ("5.7T", "训练 tokens", TEAL), ("4.2e-4", "峰值学习率", AMBER)]
    for i, (v, l, col) in enumerate(stats):
        y = 1.75 + i * 1.35
        add_rect(s, 8.3, y, 4.4, 1.15, fill=WHITE, line=LINE, radius=0.06)
        add_text(s, 8.5, y + 0.1, 1.9, 0.3, l, size=8.3, bold=True, color=MUTED)
        add_text(s, 8.5, y + 0.35, 2.2, 0.55, v, size=24, bold=True, color=col)
    add_text(s, 8.3, 5.95, 4.4, 0.55, "Moonlight 3B/16B MoE；wd=0.1。", size=8.5, color=MUTED)
    takeaway(s, "Muon 能规模化，不是因为公式更漂亮，而是因为补上了 wd 和缩放。", accent=BLUE)
    notes(s, "Moonshot 的两个工程关键：加 weight decay，按参数调整 update scale 到 0.2。没有这两步，Muon 在大模型上"
             "不稳定。结果是 compute-optimal 下约 2 倍效率，Moonlight 3B/16B 训了 5.7T tokens。")


def s29_kimi(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "前沿", "Kimi K2：1T 参数，15.5T tokens，零 loss spike", "MuonClip = Muon + QK-clip：给注意力 logit 装一个保险丝",
           page=29, source="Kimi K2, arXiv 2507.20534, 2025-07")
    stats = [("1T / 32B", "总参数 / 激活参数", PURPLE), ("15.5T", "训练 tokens", TEAL), ("0", "loss spike", GREEN)]
    for i, (v, l, col) in enumerate(stats):
        add_metric(s, 0.62 + i * 4.02, 1.72, 3.86, 1.3, l, v, "", accent=col, value_size=26)
    add_text(s, 0.62, 3.45, 6.0, 0.3, "QK-clip 做什么", size=10, bold=True, color=MUTED)
    add_text(s, 0.62, 3.8, 6.0, 1.6,
             "Muon 更容易让注意力 logit 爆炸。\n"
             "当某个 head 的最大 logit 超过 τ=100：\n"
             "把 Wq 乘 γ^α，Wk 乘 γ^(1−α)，\n"
             "逐 head 缩放，稳定后关闭。",
             size=9.8, color=TEXT, line_spacing=1.35)
    formula_card(s, 0.62, 5.35, 6.0, 1.0,
                 [[("max logit > τ  ⇒  W", ""), ("q", "sub"), (" ← γ", ""), ("α", "sup"),
                   (" W", ""), ("q", "sub"), (",  W", ""), ("k", "sub"), (" ← γ", ""),
                   ("1−α", "sup"), (" W", ""), ("k", "sub")]],
                 accent=PURPLE, size=13)
    add_text(s, 6.95, 3.45, 5.6, 0.3, "这说明什么", size=10, bold=True, color=MUTED)
    add_text(s, 6.95, 3.82, 5.65, 2.4,
             "· Muon 不是“即插即用”：\n"
             "  大规模下要配稳定化手段。\n\n"
             "· 逐 head 而不是逐层：\n"
             "  爆炸是局部现象。\n\n"
             "· 稳定后关闭：\n"
             "  它是保险丝，不是常规正则。",
             size=9.8, color=TEXT, line_spacing=1.4)
    takeaway(s, "Muon 的生产化 = 更好的更新 + 更细的稳定化。", accent=PURPLE)
    notes(s, "Kimi K2 是 1T 总参、32B 激活的 MoE，15.5T tokens，零 loss spike。MuonClip 在 Muon 基础上加 QK-clip："
             "逐 head 监控最大 logit，超过 100 就把 Q/K 按 γ^α 缩放。稳定后关闭。这说明 Muon 需要配套稳定化。")


def s30_table(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "对比", "Adam / AdamW / Muon：一张表", "同一个目标，三种“看参数”的方式",
           page=30, source="本讲整理；细节见前述各页")
    data = [["维度", "Adam (2015)", "AdamW (2019)", "Muon (2024)"],
            ["更新对象", "所有参数，逐元素", "所有参数，逐元素", "2D hidden 矩阵"],
            ["预条件", "每坐标 √v̂", "每坐标 √v̂", "矩阵奇异值（NS 正交化）"],
            ["正则", "L2 耦合进梯度", "解耦 weight decay", "解耦 wd + update 缩放"],
            ["关键超参", "lr, β₁, β₂, ε", "lr, β₁, β₂, ε, wd", "lr, μ, wd, 缩放系数"],
            ["典型场景", "通用基线、稀疏特征", "LLM 预训练默认", "大规模矩阵预训练"],
            ["主要风险", "泛化争议、不保证收敛", "wd 与 lr 仍需重调", "稳定性、分布式通信"]]
    add_table(s, 0.62, 1.72, 12.09, 4.4, data, [1.55, 3.25, 3.45, 3.84],
              body_size=9.2, header_size=9.4, row_height=0.6)
    takeaway(s, "三者不是替代关系：Adam 是基线，AdamW 修正则，Muon 换几何。", accent=AMBER)
    notes(s, "这张表是总结：Adam 逐元素、AdamW 解耦正则、Muon 对矩阵谱做预条件。选型时先看参数形状，再看瓶颈。")


def s31_choose(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "选型", "先问三个问题，再换优化器", "默认 AdamW；只有明确收益时才上 Muon",
           page=31, source="本讲整理")
    add_rect(s, 4.55, 1.68, 4.2, 0.7, fill=NAVY, line=None, radius=0.12)
    add_text(s, 4.55, 1.82, 4.2, 0.4, "默认：AdamW", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    branches = [("参数里有大量 embedding / 稀疏特征？", "AdamW 或 Adafactor", "别用 Muon 硬套", TEAL),
                ("大规模 2D 矩阵预训练、算力是瓶颈？", "试 Muon + AdamW 兜底", "先小规模验证稳定性", AMBER),
                ("小数据 / CNN / 更在意泛化？", "SGD + momentum 仍值得试", "调好 lr 与 schedule", BLUE)]
    for i, (q, a, note_, col) in enumerate(branches):
        x = 0.62 + i * 4.02
        add_line(s, x + 1.9, 2.4, x + 1.9, 3.05, color=LINE, width=1)
        add_rect(s, x, 3.05, 3.86, 1.55, fill=WHITE, line=LINE, radius=0.06)
        add_text(s, x + 0.18, 3.15, 3.5, 0.6, q, size=9.2, bold=True, color=TEXT, line_spacing=1.2)
        add_text(s, x + 0.18, 3.78, 3.5, 0.3, a, size=10.5, bold=True, color=col)
        add_text(s, x + 0.18, 4.12, 3.5, 0.3, note_, size=8.3, color=MUTED)
    add_text(s, 0.62, 4.9, 12.1, 0.3, "换优化器时必须一起重调的", size=9.5, bold=True, color=MUTED)
    for i, t in enumerate(["学习率", "weight decay", "warmup", "梯度裁剪"]):
        add_pill(s, 0.62 + i * 2.1, 5.25, 1.9, 0.42, t, fill=WHITE, color=TEXT, size=9)
    add_text(s, 0.62, 5.85, 12.1, 0.5, "只换一行代码、其他不变，是最常见的“Muon 没效果”原因。",
             size=9.2, color=RED)
    takeaway(s, "没有银弹：先问参数形状、瓶颈、数据规模，再决定换不换。", accent=TEAL)
    notes(s, "选型树：默认 AdamW；embedding/稀疏别用 Muon；大规模矩阵预训练可以试 Muon，但要有 AdamW 兜底；"
             "小数据 CNN 仍可试 SGD+momentum。换优化器必须重调 lr、wd、warmup、clip。")


def s32_pitfalls(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "避坑", "六个最常见的错", "每一个都能让“换个优化器”变成“白跑一次”",
           page=32, source="本讲整理")
    items = [("把 weight_decay 当 L2", "Adam 下两者不等价；衰减强度被 √v 改写。", "用 AdamW / 解耦实现"),
             ("忘了偏差修正", "自己实现时漏掉 1−βᵗ，前几步步长偏大 3 倍。", "用框架默认实现"),
             ("Muon 用在 embedding", "embedding 行稀疏、形状特殊，NS 不适用。", "embedding/head 用 AdamW"),
             ("直接套 Muon 的 lr", "update RMS 没对齐，lr 不可迁移。", "先对齐 0.2 再调 lr"),
             ("大规模不做 logit 监控", "Muon 更易 logit 爆炸，几十亿 token 后才炸。", "QK-clip / 监控 max logit"),
             ("只换优化器不换配方", "warmup、wd、clip 全是按旧优化器调的。", "四项一起重调")]
    for i, (bad, why, fix) in enumerate(items):
        x = 0.62 + (i % 2) * 6.1
        y = 1.72 + (i // 2) * 1.58
        add_rect(s, x, y, 5.9, 1.42, fill=WHITE, line=LINE, radius=0.06)
        add_text(s, x + 0.16, y + 0.1, 0.3, 0.3, "✕", size=11, bold=True, color=RED)
        add_text(s, x + 0.45, y + 0.1, 5.2, 0.3, bad, size=10, bold=True, color=TEXT)
        add_text(s, x + 0.45, y + 0.44, 5.25, 0.45, why, size=8.6, color=MUTED, line_spacing=1.15)
        add_text(s, x + 0.45, y + 1.0, 5.25, 0.3, "→ " + fix, size=8.8, bold=True, color=GREEN)
    takeaway(s, "换优化器是一次“重调”，不是一次“替换”。", accent=RED)
    notes(s, "六个坑：L2 与 wd 混用、漏偏差修正、Muon 用在 embedding、lr 不迁移、不做 logit 监控、只换优化器不改配方。"
             "每一个都能让实验白跑。")


def s33_lab(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "动手", "把这三个开关改一遍", "代码与图都在仓库 decks/gd-optimizers-2026/，十分钟能跑完",
           page=33, source="experiment.py；本讲 Toy 实验")
    code = [("MPLCONFIGDIR=./.mpl python3 experiment.py", rgb("5EEAD4")),
            ("", rgb("E2E8F0")),
            ("# 三个开关", rgb("94A3B8")),
            ("kappa = 100      # 曲率比", rgb("E2E8F0")),
            ("beta  = 0.9      # 动量/二阶矩", rgb("E2E8F0")),
            ("ns_steps = 5     # NS 迭代步数", rgb("E2E8F0"))]
    code_card(s, 0.62, 1.72, 6.3, 2.35, code, title="复现实验", size=9.5)
    ex = [("把 κ 改成 1000", "观察 SGD 与动量的步数如何爆炸；Adam 是否仍然稳？"),
          ("把 β₂ 改成 0.9", "偏差修正曲线会变平；首步的 3.16 倍会变成多少？"),
          ("把 NS 步数改成 1/3/5", "看奇异值谱多久压平；1 步够不够？")]
    for i, (h, b) in enumerate(ex):
        y = 1.78 + i * 1.35
        section_num(s, 7.2, y + 0.02, i + 1, color=AMBER, d=0.3)
        add_text(s, 7.62, y, 4.9, 0.3, h, size=10.5, bold=True, color=TEXT)
        add_text(s, 7.62, y + 0.32, 4.95, 0.65, b, size=9.4, color=MUTED, line_spacing=1.25)
    add_text(s, 0.62, 4.35, 6.3, 1.3,
             "实验刻意做得很小：一个 2D 二次函数、一个合成矩阵。\n"
             "它不能证明“Muon 一定更好”，但能让你亲眼看到\n"
             "“曲率、偏差修正、谱”这三件事的形状。",
             size=9.3, color=MUTED, line_spacing=1.35)
    takeaway(s, "看懂十遍公式，不如亲手改一次 κ 和 NS 步数。", accent=AMBER)
    notes(s, "实验很小，十分钟能跑。改 κ 看曲率，改 β₂ 看偏差修正，改 NS 步数看谱。目的不是证明谁更好，"
             "而是把公式和形状对上。")


def s34_timeline(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "时间线", "从 1847 到 2025", "十个节点，四次范式转移",
           page=34, source="各原始论文；完整引用见第 36 页")
    nodes = [("1847", "Cauchy\n梯度下降", TEAL, 1),
             ("1951", "Robbins–Monro\n随机近似", TEAL, -1),
             ("1964", "Polyak\n动量", BLUE, 1),
             ("1983", "Nesterov\n加速梯度", BLUE, -1),
             ("1986", "反向传播\n可训练", BLUE, 1),
             ("2011", "AdaGrad\n每坐标步长", PURPLE, -1),
             ("2015", "Adam\n自适应矩估计", PURPLE, 1),
             ("2017", "AdamW\n解耦正则", PURPLE, -1),
             ("2024", "Muon\n矩阵几何", AMBER, 1),
             ("2025", "规模化\nMoonshot / K2", AMBER, -1)]
    add_line(s, 0.9, 3.7, 12.45, 3.7, color=rgb("CBD5E1"), width=2)
    for i, (year, label, col, side) in enumerate(nodes):
        x = 0.9 + i * 1.28
        add_circle(s, x - 0.07, 3.63, 0.14, fill=col, line=WHITE, line_w=1.5)
        add_text(s, x - 0.55, 3.32 if side == 1 else 3.92, 1.1, 0.28, year, size=8.5, bold=True,
                 color=col, align=PP_ALIGN.CENTER)
        add_text(s, x - 0.62, 2.55 if side == 1 else 4.28, 1.24, 0.7, label, size=7.6, color=TEXT,
                 align=PP_ALIGN.CENTER, line_spacing=1.15)
        if side == 1:
            add_line(s, x, 3.63, x, 3.3, color=col, width=0.8)
        else:
            add_line(s, x, 3.77, x, 4.1, color=col, width=0.8)
    add_rect(s, 0.62, 5.35, 12.09, 0.75, fill=WHITE, line=LINE, radius=0.08)
    add_text(s, 0.85, 5.47, 11.6, 0.5,
             "1847 确定性下降  →  1951 噪声下收敛  →  1986 梯度算得动  →  2011 每坐标步长  →  "
             "2017 解耦正则  →  2024 矩阵几何",
             size=9.2, color=MUTED)
    takeaway(s, "每一次范式转移，都是把“一个标量”拆成更细的结构。", accent=AMBER)
    notes(s, "十个节点串起全篇。可以让学生记四个年份：1847、1951、2015、2024，分别对应确定性、随机、自适应、矩阵几何。")


def s35_cheatsheet(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "速查", "七个更新式", "贴在显示器旁边的那张纸",
           page=35, source="本讲整理")
    data = [["方法", "更新式", "一句话"],
            ["SGD", "θ ← θ − ηg", "最朴素的负梯度"],
            ["Momentum", "v ← βv + g;  θ ← θ − ηv", "用历史平滑方向"],
            ["AdaGrad", "G ← G + g²;  θ ← θ − ηg/(√G+ε)", "每坐标累计步长"],
            ["RMSProp", "v ← βv + (1−β)g²;  θ ← θ − ηg/(√v+ε)", "滑动平均版 AdaGrad"],
            ["Adam", "m,v 滑动平均 + 偏差修正;  θ ← θ − ηm̂/(√v̂+ε)", "动量 + 每坐标步长"],
            ["AdamW", "θ ← θ − ηm̂/(√v̂+ε) − ηλθ", "正则单独减"],
            ["Muon", "O ← NS5(μB+G);  W ← W − η(0.2·O·√max(A,B)+λW)", "矩阵谱正交化"]]
    add_table(s, 0.62, 1.72, 12.09, 4.55, data, [1.35, 6.5, 4.24],
              body_size=8.8, header_size=9, row_height=0.55)
    takeaway(s, "公式是地图，不是地形；真正跑起来还要看 lr、wd、warmup。", accent=TEAL)
    notes(s, "这页是速查表，不展开。强调公式只是地图，实际训练还要看调度和正则。")


def s36_refs(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, "参考", "一手来源", "优先引用论文与作者原文；博客与代码作为工程证据",
           page=36, source="访问时间：2026-11")
    refs = [
        ("Cauchy, 1847", "Méthode générale pour la résolution des systèmes d'équations simultanées."),
        ("Robbins & Monro, 1951", "A Stochastic Approximation Method. Ann. Math. Stat."),
        ("Polyak, 1964", "Some methods of speeding up the convergence of iteration methods."),
        ("Nesterov, 1983", "A method of solving a convex programming problem with convergence rate O(1/k²)."),
        ("Rumelhart, Hinton & Williams, 1986", "Learning representations by back-propagating errors. Nature."),
        ("Duchi, Hazan & Singer, 2011", "Adaptive Subgradient Methods. JMLR 12."),
        ("Hinton, 2012", "Coursera Neural Networks, lecture 6.5 (RMSProp, unpublished)."),
        ("Kingma & Ba, 2015", "Adam: A Method for Stochastic Optimization. ICLR. arXiv:1412.6980"),
        ("Reddi et al., 2018", "On the Convergence of Adam and Beyond. ICLR. arXiv:1904.09237"),
        ("Loshchilov & Hutter, 2019", "Decoupled Weight Decay Regularization. ICLR. arXiv:1711.05101"),
        ("Wilson et al., 2017", "The Marginal Value of Adaptive Gradient Methods. NeurIPS."),
        ("Jordan, 2024", "Muon: An optimizer for hidden layers in neural networks. kellerjordan.github.io/posts/muon/"),
        ("Moonshot AI, 2025", "Muon is Scalable for LLM Training. arXiv:2502.16982"),
        ("Kimi Team, 2025", "Kimi K2: Open Agentic Intelligence. arXiv:2507.20534"),
        ("Llama Team, 2024", "The Llama 3 Herd of Models. arXiv:2407.21783"),
        ("Gupta et al., 2018", "Shampoo: Preconditioned Stochastic Tensor Optimization. arXiv:1802.09568"),
    ]
    for i, (who, what) in enumerate(refs):
        col = i // 8
        row = i % 8
        x = 0.62 + col * 6.1
        y = 1.72 + row * 0.63
        add_text(s, x, y, 5.85, 0.24, f"{who}", size=8.3, bold=True, color=TEAL)
        add_text(s, x, y + 0.21, 5.85, 0.38, what, size=7.3, color=MUTED, line_spacing=1.05)
    add_text(s, 0.62, 6.75, 12.1, 0.3, "注：部分历史细节（如 Transformer 的 Adam β₂=0.98）为领域常识，正文未逐字核验，已在相应页标注。",
             size=7.2, color=SLATE)
    notes(s, "参考文献按时间排。工程证据（Muon 博客、Moonshot、Kimi）与论文分开看：前者是实践，后者是方法。")


def s37_end(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, DARK)
    add_circle(s, 10.0, -1.2, 4.6, fill=rgb("13203A"), line=None)
    add_text(s, 0.9, 0.95, 8.0, 0.3, "结语", size=10, bold=True, color=TEAL2)
    add_text(s, 0.9, 1.45, 10.6, 0.8, "三句话带走", size=38, bold=True, color=WHITE)
    lines = [("01", "Adam 解决“每个坐标该走多大”。", TEAL),
             ("02", "AdamW 解决“正则不该被自适应分母绑架”。", BLUE),
             ("03", "Muon 解决“矩阵更新该不该按谱走”。", AMBER)]
    for i, (n, t, col) in enumerate(lines):
        y = 2.65 + i * 0.95
        add_text(s, 0.9, y, 0.6, 0.4, n, size=11, bold=True, color=col)
        add_text(s, 1.55, y - 0.05, 10.4, 0.6, t, size=17, color=WHITE)
        add_line(s, 0.9, y + 0.62, 12.3, y + 0.62, color=rgb("243247"), width=0.6)
    add_text(s, 0.9, 5.75, 11.4, 0.8,
             "没有银弹：先问参数是什么形状、瓶颈是收敛还是泛化、算力账单有多贵。",
             size=10.5, color=rgb("A8B6CC"))
    add_rect(s, 0.9, 6.55, 1.4, 0.42, fill=TEAL, line=None, radius=0.2)
    add_text(s, 0.9, 6.63, 1.4, 0.25, "Q & A", size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, 2.5, 6.62, 8.0, 0.3, "代码、图表与延伸阅读：github.com/binbinao/ai-ppt-hub", size=8.5,
             color=rgb("7C8BA3"))
    notes(s, "收尾三句话：Adam 管尺度，AdamW 管正则，Muon 管几何。最后强调没有银弹，选型要回到参数形状、"
             "瓶颈和数据规模。留 Q&A。")


def build():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    for fn in [s01_cover, s02_agenda, s03_paradigms, s04_why, s05_descent, s06_history,
               s07_sgd, s08_traj, s09_lr, s10_momentum, s11_adagrad, s12_rmsprop,
               s13_adam, s14_bias, s15_adam_why, s16_wilson, s17_reddi, s18_decouple,
               s19_adamw, s20_evidence, s21_llama, s22_limit, s23_muon, s24_insight,
               s25_algo, s26_ns, s27_evidence2, s28_scale, s29_kimi, s30_table,
               s31_choose, s32_pitfalls, s33_lab, s34_timeline, s35_cheatsheet,
               s36_refs, s37_end]:
        fn(prs)
    out = os.path.join(HERE, "out", "从下山到矩阵几何：梯度下降优化器七十年.pptx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prs.save(out)
    print("saved", out, os.path.getsize(out))
    return out


if __name__ == "__main__":
    build()
