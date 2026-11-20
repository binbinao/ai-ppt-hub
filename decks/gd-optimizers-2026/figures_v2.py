# -*- coding: utf-8 -*-
"""Generate the additional explanatory figures for the v2 deck.

All figures are deterministic; no external data is used. Published numbers
(13.3 / 10.0 A100-hours) come from the Muon blog and are labelled as such.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl-gd")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.colors import LinearSegmentedColormap, LogNorm

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
os.makedirs(FIGS, exist_ok=True)

# ---------------------------------------------------------------- palette
DARK = "#0B1220"
NAVY = "#111827"
BG = "#F6F7FB"
CARD = "#FFFFFF"
TEXT = "#111827"
MUTED = "#64748B"
LINE = "#E2E8F0"
TEAL = "#0D9488"
TEAL2 = "#14B8A6"
AMBER = "#D97706"
AMBER2 = "#F59E0B"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
RED = "#DC2626"
GREEN = "#059669"
SLATE = "#94A3B8"

rcParams.update({
    "font.family": "Arial Unicode MS",
    "font.size": 13,
    "axes.edgecolor": LINE,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": TEXT,
    "figure.facecolor": CARD,
    "savefig.facecolor": CARD,
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",
})


def _save(fig, name, dpi=200, tight=True):
    path = os.path.join(FIGS, name)
    if tight:
        fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.08)
    else:
        fig.savefig(path, dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    from PIL import Image
    im = Image.open(path)
    print(f"{name}: {im.size[0]}x{im.size[1]}  ratio={im.size[0]/im.size[1]:.3f}")


# ---------------------------------------------------------------- 1. 3D loss surface
def fig_surface():
    fig = plt.figure(figsize=(10, 5.625), facecolor=DARK)
    ax = fig.add_axes([0.34, 0.02, 0.66, 0.96], projection="3d")
    ax.set_facecolor(DARK)

    x = np.linspace(-2.8, 2.8, 140)
    y = np.linspace(-1.9, 1.9, 120)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X ** 2 + 42 * Y ** 2)
    Z = np.log1p(Z)

    cmap = LinearSegmentedColormap.from_list(
        "gd", ["#0F2A33", "#0D9488", "#2DD4BF", "#A7F3D0"])
    ax.plot_surface(X, Y, Z, cmap=cmap, rstride=2, cstride=2, linewidth=0,
                    antialiased=True, alpha=0.96, shade=True)
    # thin contour rings projected on the floor
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=np.log1p(0) - 0.02,
               colors="#14B8A6", linewidths=0.5, alpha=0.35)

    # gradient-descent path on the surface
    pts = [(2.35, 1.45)]
    for _ in range(140):
        px, py = pts[-1]
        gx, gy = px, 42 * py
        lr = 0.045
        pts.append((px - lr * gx, py - lr * gy))
    P = np.array(pts)
    PZ = np.log1p(0.5 * (P[:, 0] ** 2 + 42 * P[:, 1] ** 2)) + 0.03
    ax.plot(P[:, 0], P[:, 1], PZ, color=AMBER2, lw=2.4, zorder=10,
            solid_capstyle="round")
    ax.scatter([P[0, 0]], [P[0, 1]], [PZ[0]], s=52, color="#FDE68A",
               edgecolor=DARK, linewidth=1.0, zorder=11, depthshade=False)
    ax.scatter([0], [0], [PZ[-1]], s=40, color="#FFFFFF", edgecolor=TEAL,
               linewidth=1.0, zorder=11, depthshade=False)

    ax.view_init(elev=34, azim=-57)
    ax.set_xlabel("θ₁", labelpad=-4, color="#94A3B8", fontsize=13)
    ax.set_ylabel("θ₂", labelpad=-4, color="#94A3B8", fontsize=13)
    ax.set_zlabel("loss", labelpad=-8, color="#94A3B8", fontsize=12)
    ax.tick_params(colors="#64748B", labelsize=8, pad=-2)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((0.04, 0.07, 0.12, 1.0))
        axis.pane.set_edgecolor((0.1, 0.16, 0.24, 1.0))
        axis._axinfo["grid"]["color"] = (0.12, 0.18, 0.26, 1.0)
        axis._axinfo["grid"]["linewidth"] = 0.5
    ax.set_zticks([])
    _save(fig, "fig_surface3d.png", tight=False)


# ---------------------------------------------------------------- 2. momentum vectors
def fig_momentum():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    x = np.linspace(-2.1, 2.1, 300)
    y = np.linspace(-1.5, 1.5, 300)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X ** 2 + 34 * Y ** 2)
    ax.contour(X, Y, Z, levels=14, colors=[LINE], linewidths=0.9)
    ax.contour(X, Y, Z, levels=[0.6, 2.2, 5.0], colors=[TEAL], linewidths=1.1,
               alpha=0.55)

    p = np.array([1.55, -1.02])
    g = np.array([p[0], 34 * p[1]])
    lr = 0.030
    v = np.array([-0.62, 0.20])  # accumulated velocity (momentum)
    step_gd = -lr * g * 3.2
    step_v = v * 0.95
    step_n = (-lr * g * 3.2) * 0.55 + v * 0.62

    def arrow(start, vec, color, lw=3.0, style="-|>", ls="-", label=None, off=(0, 0)):
        end = start + vec
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=20,
                                     color=color, lw=lw, linestyle=ls,
                                     shrinkA=0, shrinkB=0, zorder=5))
        if label:
            mid = start + vec * 0.55 + np.array(off)
            ax.text(mid[0], mid[1], label, color=color, fontsize=17, fontweight="bold",
                    ha="center", va="center", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.18", fc=CARD, ec="none", alpha=0.85))

    ax.scatter(*p, s=70, color=TEXT, zorder=7)
    arrow(p, step_gd, RED, label="−ηg  只看当前梯度", off=(0.0, 0.22))
    arrow(p, step_v, BLUE, label="动量 v  记住历史", off=(0.0, -0.26))
    arrow(p, step_n, TEAL, label="实际一步", off=(0.18, 0.0), lw=4.0)

    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    _save(fig, "fig_momentum.png")


# ---------------------------------------------------------------- 3. Adam data flow
def _box(ax, x, y, w, h, text, fc, ec, tc=TEXT, fs=17, bold=False):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.03",
                       fc=fc, ec=ec, lw=1.4, zorder=3)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", zorder=4)


def _arr(ax, p0, p1, color=MUTED, lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=15,
                                 color=color, lw=lw, shrinkA=2, shrinkB=2, zorder=2))


def fig_adam_flow():
    fig, ax = plt.subplots(figsize=(11.6, 4.4))
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    _box(ax, 0.15, 1.72, 1.25, 0.9, r"$g_t$", "#EEF2F7", LINE, TEXT, 22, True)

    # momentum branch (top)
    _box(ax, 1.95, 2.92, 2.55, 1.06, "$m_t = \\beta_1 m_{t-1}$\n$+\\ (1-\\beta_1)g_t$", "#ECFDF5", TEAL, TEXT, 14)
    _box(ax, 4.95, 2.92, 1.95, 1.06, "$\\hat{m}_t = m_t$\n$/ (1-\\beta_1^t)$", "#ECFDF5", TEAL, TEXT, 14)
    # second-moment branch (bottom)
    _box(ax, 1.95, 0.42, 2.55, 1.06, "$v_t = \\beta_2 v_{t-1}$\n$+\\ (1-\\beta_2)g_t^2$", "#EFF6FF", BLUE, TEXT, 14)
    _box(ax, 4.95, 0.42, 1.95, 1.06, "$\\hat{v}_t = v_t$\n$/ (1-\\beta_2^t)$", "#EFF6FF", BLUE, TEXT, 14)

    # combine
    _box(ax, 7.35, 1.47, 2.15, 1.42, "$\\theta_t = \\theta_{t-1}$\n$-\\ \\eta\\, \\hat{m}_t$\n$/ (\\sqrt{\\hat{v}_t}+\\epsilon)$",
         "#FFF7ED", AMBER, TEXT, 13)
    ax.text(9.85, 2.18, "每个坐标\n自己的步长", color=AMBER, fontsize=13,
            ha="left", va="center", fontweight="bold")

    _arr(ax, (1.4, 2.35), (1.9, 3.28), TEAL)
    _arr(ax, (1.4, 1.98), (1.9, 1.0), BLUE)
    _arr(ax, (4.5, 3.45), (4.9, 3.45), TEAL)
    _arr(ax, (4.5, 0.95), (4.9, 0.95), BLUE)
    _arr(ax, (4.02, 3.1), (4.02, 2.05), MUTED, 1.4, "-|>")
    ax.text(3.98, 2.62, "平方", color=MUTED, fontsize=12)

    _arr(ax, (6.9, 3.45), (7.35, 2.55), TEAL)
    _arr(ax, (6.9, 0.95), (7.35, 1.8), BLUE)

    ax.text(0.15, 4.1, "Adam：两条指数滑动平均，各自做偏差修正", fontsize=15,
            color=TEXT, fontweight="bold")
    _save(fig, "fig_adam_flow.png")


# ---------------------------------------------------------------- 4. AdamW coupling
def fig_adamw():
    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    # lane 1: Adam + L2
    ax.add_patch(FancyBboxPatch((0.15, 2.62), 11.05, 1.95,
                                boxstyle="round,pad=0.01,rounding_size=0.04",
                                fc="#FEF2F2", ec="#FECACA", lw=1.0, zorder=1))
    ax.text(0.4, 4.28, "Adam + L2 正则（旧做法）", fontsize=15, color=RED, fontweight="bold")
    _box(ax, 0.45, 3.0, 1.55, 0.75, "$g + \\lambda\\theta$", "#FFFFFF", "#FCA5A5", TEXT, 17, True)
    _box(ax, 2.5, 3.0, 2.0, 0.75, "$\\div (\\sqrt{\\hat{v}}+\\epsilon)$", "#FFFFFF", "#FCA5A5", TEXT, 16)
    _box(ax, 5.0, 3.0, 2.95, 0.75, "有效衰减 $= \\lambda\\theta/\\sqrt{\\hat{v}}$", "#FFFFFF", RED, RED, 14, True)
    _arr(ax, (2.0, 3.38), (2.45, 3.38), RED)
    _arr(ax, (4.5, 3.38), (4.95, 3.38), RED)
    ax.text(8.2, 3.38, "衰减被二阶矩缩放：\n越“陡”的坐标，正则越弱", fontsize=13,
            color=RED, va="center")

    # lane 2: AdamW
    ax.add_patch(FancyBboxPatch((0.15, 0.2), 11.05, 1.95,
                                boxstyle="round,pad=0.01,rounding_size=0.04",
                                fc="#ECFDF5", ec="#A7F3D0", lw=1.0, zorder=1))
    ax.text(0.4, 1.86, "AdamW：解耦 weight decay（现在）", fontsize=15, color=TEAL,
            fontweight="bold")
    _box(ax, 0.45, 0.58, 1.55, 0.75, "g", "#FFFFFF", TEAL, TEXT, 19, True)
    _box(ax, 2.5, 0.58, 2.0, 0.75, "$\\div (\\sqrt{\\hat{v}}+\\epsilon)$", "#FFFFFF", TEAL, TEXT, 16)
    _box(ax, 5.0, 0.58, 2.95, 0.75, "$\\theta \\leftarrow \\theta(1-\\eta\\lambda)$", "#FFFFFF", TEAL, TEAL, 16, True)
    _arr(ax, (2.0, 0.96), (2.45, 0.96), TEAL)
    _arr(ax, (4.5, 0.96), (4.95, 0.96), TEAL)
    ax.text(8.2, 0.96, "衰减只由 λ 和 η 决定：\n与梯度尺度彻底分开", fontsize=13,
            color=TEAL, va="center")
    _save(fig, "fig_adamw.png")


# ---------------------------------------------------------------- 5. Muon spectrum
def _ns5(A):
    a, b, c = 3.4445, -4.7750, 2.0315
    for _ in range(5):
        AA = A @ A.T
        A = a * A + b * (AA @ A) + c * (AA @ AA @ A)
    return A


def fig_spectrum():
    rng = np.random.default_rng(7)
    U, _ = np.linalg.qr(rng.normal(size=(64, 64)))
    V, _ = np.linalg.qr(rng.normal(size=(32, 32)))
    s = np.geomspace(1.0, 0.02, 32) * (0.85 + 0.3 * rng.random(32))
    s = np.sort(s)[::-1]
    A0 = U[:, :32] @ np.diag(s) @ V.T

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.6),
                                   gridspec_kw={"width_ratios": [1.05, 1.25]})
    its = [0, 1, 2, 5]
    colors = ["#CBD5E1", "#5EEAD4", "#14B8A6", "#0F766E"]
    for it, col in zip(its, colors):
        A = A0.copy()
        for _ in range(it):
            A = _ns5(A)
        sv = np.linalg.svd(A, compute_uv=False)
        ax1.plot(np.arange(1, 33), sv, color=col, lw=2.2,
                 label=f"第 {it} 次 NS5")
    ax1.axhspan(0.68, 1.13, color=TEAL, alpha=0.08, lw=0)
    ax1.axhline(1.0, color=TEAL, lw=1.0, ls="--", alpha=0.6)
    ax1.set_xlabel("奇异值序号", fontsize=13)
    ax1.set_ylabel(r"$\sigma_i/\sigma_{\max}$", fontsize=13)
    ax1.set_ylim(0, 1.12)
    ax1.legend(frameon=False, fontsize=10, loc="lower left")
    ax1.set_title("谱被压平到 [0.68, 1.13]", fontsize=14, color=TEXT, loc="left")
    for sp in ("top", "right"):
        ax1.spines[sp].set_visible(False)

    # heatmap of the spectrum across 8 NS5 rounds
    rounds = 8
    M = np.zeros((rounds + 1, 32))
    A = A0.copy()
    for r in range(rounds + 1):
        sv = np.linalg.svd(A, compute_uv=False)
        M[r] = sv / sv.max()
        A = _ns5(A)
    im = ax2.imshow(M, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1.0,
                    interpolation="nearest")
    ax2.set_xlabel("奇异值序号", fontsize=13)
    ax2.set_ylabel("NS5 迭代次数", fontsize=13)
    ax2.set_title("每一步把谱推向 1", fontsize=14, color=TEXT, loc="left")
    ax2.set_yticks(range(0, rounds + 1, 2))
    cb = fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.02)
    cb.ax.tick_params(labelsize=9)
    cb.outline.set_visible(False)
    fig.tight_layout(w_pad=2.0)
    _save(fig, "fig_spectrum.png")


# ---------------------------------------------------------------- 6. compute bars
def fig_compute():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.3),
                                   gridspec_kw={"width_ratios": [1.15, 1]})

    labels = ["AdamW", "Muon"]
    vals = [13.3, 10.0]
    cols = [SLATE, TEAL]
    bars = ax1.bar(labels, vals, color=cols, width=0.52)
    for b, v in zip(bars, vals):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.35, f"{v:g}",
                 ha="center", fontsize=20, fontweight="bold", color=TEXT)
    ax1.set_ylim(0, 16.2)
    ax1.set_ylabel("8×H100 小时", fontsize=13)
    ax1.set_title("1.5B 模型达到 GPT-2 XL 的 HellaSwag", fontsize=13.5,
                  color=TEXT, loc="left")
    ax1.text(0.0, -0.20, "越低越好；数据：Jordan 2024 博客", transform=ax1.transAxes,
             fontsize=9.5, color=MUTED)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.tick_params(labelsize=13)

    labels2 = ["AdamW", "Muon"]
    vals2 = [1.0, 0.5]
    bars2 = ax2.barh(labels2, vals2, color=[SLATE, TEAL], height=0.42)
    for b, v in zip(bars2, vals2):
        ax2.text(v + 0.03, b.get_y() + b.get_height() / 2, f"{v:g}×",
                 va="center", fontsize=19, fontweight="bold", color=TEXT)
    ax2.set_xlim(0, 1.25)
    ax2.set_xlabel("达到相同 loss 的相对算力", fontsize=13)
    ax2.set_title("Moonshot：约 2× 计算效率", fontsize=13.5, color=TEXT, loc="left")
    ax2.text(0.0, -0.20, "由论文 ~2× 结论换算为相对值；越低越好", transform=ax2.transAxes,
             fontsize=9.5, color=MUTED)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.tick_params(labelsize=13)
    fig.tight_layout(w_pad=2.6)
    _save(fig, "fig_compute.png")


if __name__ == "__main__":
    fig_surface()
    fig_momentum()
    fig_adam_flow()
    fig_adamw()
    fig_spectrum()
    fig_compute()


# ---------------------------------------------------------------- 7. low-rank spectrum
def fig_lowrank():
    rng = np.random.default_rng(11)
    U, _ = np.linalg.qr(rng.normal(size=(64, 64)))
    V, _ = np.linalg.qr(rng.normal(size=(32, 32)))
    s = np.geomspace(1.0, 0.015, 32)
    A = U[:, :32] @ np.diag(s) @ V.T
    sv = np.linalg.svd(A, compute_uv=False)
    energy = np.cumsum(sv ** 2) / np.sum(sv ** 2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.5),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    ax1.semilogy(np.arange(1, 33), sv, color=TEAL, lw=2.4)
    ax1.fill_between(np.arange(1, 33), sv, 1e-3, color=TEAL, alpha=0.07)
    ax1.set_xlabel("奇异值序号", fontsize=13)
    ax1.set_ylabel("奇异值（对数轴）", fontsize=13)
    ax1.set_title("梯度矩阵的谱衰减得很快", fontsize=14.5, color=TEXT, loc="left")
    ax1.annotate("少数奇异值\n携带大部分能量", xy=(5, sv[4]), xytext=(13, 0.12),
                 fontsize=12.5, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=SLATE, lw=0.9))
    ax1.spines[["top", "right"]].set_visible(False)

    ax2.plot(np.arange(1, 33), energy * 100, color=AMBER, lw=2.6)
    ax2.axhline(80, color=SLATE, lw=1.0, ls="--")
    k80 = int(np.searchsorted(energy, 0.8) + 1)
    ax2.scatter([k80], [80], s=60, color=AMBER, zorder=5)
    ax2.annotate(f"前 {k80} 个 ≈ 80%", xy=(k80, 80), xytext=(k80 + 4, 58),
                 fontsize=13, color=AMBER, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2))
    ax2.set_xlabel("保留的奇异值个数", fontsize=13)
    ax2.set_ylabel("累计能量（%）", fontsize=13)
    ax2.set_ylim(0, 104)
    ax2.set_xlim(0, 33)
    ax2.set_title("有效秩远小于矩阵维度", fontsize=14.5, color=TEXT, loc="left")
    ax2.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(w_pad=2.2)
    _save(fig, "fig_lowrank.png")


# ---------------------------------------------------------------- 8. AdaGrad per-coordinate step
def fig_adaptive():
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    t = np.arange(1, 201)
    gA = 1.0
    gB = 0.1
    stepA = 0.5 / np.sqrt(gA ** 2 * t)
    stepB = 0.5 / np.sqrt(gB ** 2 * t + 1e-12)
    ax.plot(t, stepA, color=SLATE, lw=2.6, label="坐标 A：梯度大")
    ax.plot(t, stepB, color=TEAL, lw=2.6, label="坐标 B：梯度小")
    ax.set_yscale("log")
    ax.set_xlabel("训练步数 t", fontsize=13)
    ax.set_ylabel(r"有效步长 $\eta/\sqrt{G_t}$", fontsize=13)
    ax.set_title("同一个 η，两个坐标拿到不同步长", fontsize=14.5, color=TEXT, loc="left")
    ax.legend(frameon=False, fontsize=11)
    ax.annotate("B 的步长始终约为 A 的 10 倍\n（梯度小 → 分母小 → 步长大）",
                xy=(120, stepB[119]), xytext=(60, 2.2e-3), fontsize=11.5,
                color=MUTED, arrowprops=dict(arrowstyle="-", color=SLATE, lw=0.9))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    _save(fig, "fig_adaptive.png")


if True:
    fig_lowrank()
    fig_adaptive()
