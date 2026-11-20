# -*- coding: utf-8 -*-
"""Toy experiments + figures for the gradient-descent teaching deck.

Everything here is synthetic and reproducible:
  * ill-conditioned quadratic (condition number 100)
  * SGD / heavy-ball momentum / Adam: trajectories and learning-rate sensitivity
  * Newton-Schulz orthogonalization on a synthetic low-rank matrix
  * bias-correction curves

Run with a Python that has numpy + matplotlib:
  MPLCONFIGDIR=./.mpl /usr/local/bin/python3 experiment.py
"""
import json
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
os.makedirs(FIGS, exist_ok=True)

rcParams["font.family"] = ["Arial Unicode MS"]
rcParams["axes.unicode_minus"] = False
rcParams["figure.facecolor"] = "#F6F7FB"
rcParams["axes.facecolor"] = "#F6F7FB"
rcParams["savefig.facecolor"] = "#F6F7FB"

TEAL = "#0D9488"
BLUE = "#2563EB"
AMBER = "#D97706"
RED = "#DC2626"
SLATE = "#64748B"
GRID = "#E2E8F0"


def run(kind, H, start, lr, beta=0.9, beta2=0.999, eps=1e-8, iters=4000, target=1e-3):
    """Return trajectory, losses, first step where loss < target * initial loss."""
    th = np.array(start, dtype=float)
    f0 = 0.5 * th @ H @ th
    v = np.zeros(2)
    m = np.zeros(2)
    s = np.zeros(2)
    path = [th.copy()]
    losses = [f0]
    hit = None
    for t in range(1, iters + 1):
        g = H @ th
        if kind == "sgd":
            th = th - lr * g
        elif kind == "momentum":
            v = beta * v + g
            th = th - lr * v
        elif kind == "adam":
            m = beta * m + (1 - beta) * g
            s = beta2 * s + (1 - beta2) * g * g
            mh = m / (1 - beta ** t)
            sh = s / (1 - beta2 ** t)
            th = th - lr * mh / (np.sqrt(sh) + eps)
        path.append(th.copy())
        f = 0.5 * th @ H @ th
        losses.append(f)
        if hit is None and f < target * f0:
            hit = t
        if not np.isfinite(f) or f > 1e6 * f0:
            break
    return np.array(path), np.array(losses), hit


def best(kind, H, start, target=1e-6):
    best_steps, best_lr, best_path = None, None, None
    if kind == "adam":
        grid = np.geomspace(0.002, 2.0, 40)
    else:
        grid = np.geomspace(0.0005, 1.8 / np.linalg.eigvalsh(H).max(), 40)
    for lr in grid:
        path, losses, hit = run(kind, H, start, float(lr), target=target)
        if hit is not None and (best_steps is None or hit < best_steps):
            best_steps, best_lr, best_path = hit, float(lr), path
    return best_steps, best_lr, best_path


def _traj_panel():
    kappa = 100.0
    H = np.diag([1.0, kappa])
    start = (-2.6, 2.2)
    names = {"sgd": ("SGD", SLATE), "momentum": ("动量", AMBER), "adam": ("Adam", TEAL)}
    fig, ax = plt.subplots(figsize=(6.2, 4.7), dpi=200)
    xs = np.linspace(-3.2, 3.2, 400)
    ys = np.linspace(-3.2, 3.2, 400)
    X, Y = np.meshgrid(xs, ys)
    Z = 0.5 * (H[0, 0] * X ** 2 + 2 * H[0, 1] * X * Y + H[1, 1] * Y ** 2)
    levels = np.geomspace(max(Z.min(), 1e-4), Z.max() * 0.9, 14)
    ax.contour(X, Y, Z, levels=levels, colors="#CBD5E1", linewidths=0.55)
    ax.plot(0, 0, marker="*", ms=13, color=RED, zorder=6)
    results = {}
    for kind, (label, color) in names.items():
        steps, lr, path = best(kind, H, start)
        results[kind] = {"steps": steps, "lr": lr}
        if path is None:
            continue
        ax.plot(path[:, 0], path[:, 1], color=color, lw=1.25,
                alpha=(0.5 if kind == "sgd" else 0.95), label=f"{label} · {steps} 步")
        ax.plot(path[0, 0], path[0, 1], "o", ms=4, color=color)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.2, 3.2)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(alpha=0.22, color=GRID, lw=0.6)
    ax.set_xlabel("参数 1", fontsize=9, color=SLATE)
    ax.set_ylabel("参数 2（曲率 100 倍）", fontsize=9, color=SLATE)
    ax.set_title("同一初始点，各自调 lr，降到初始损失 1/10⁶", fontsize=10.5, color="#0F172A", pad=8)
    ax.legend(loc="upper right", fontsize=8.2, frameon=True, framealpha=0.92,
              edgecolor="none", borderpad=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_traj.png"), bbox_inches="tight")
    plt.close(fig)
    return results


def _lr_panel():
    kappa = 100.0
    H = np.diag([1.0, kappa])
    start = (-2.6, 2.2)
    names = {"sgd": ("SGD", SLATE), "momentum": ("动量", AMBER), "adam": ("Adam", TEAL)}
    fig, ax = plt.subplots(figsize=(6.4, 4.3), dpi=200)
    grid = np.geomspace(0.001, 3.0, 55)
    for kind, (label, color) in names.items():
        finals = []
        for lr in grid:
            _, losses, _ = run(kind, H, start, float(lr), iters=200, target=1e-12)
            finals.append(min(max(losses[-1] / losses[0], 1e-22), 10.0))
        ax.plot(grid, finals, color=color, lw=1.9, label=label)
    ax.axvspan(0.001, 0.02, color=SLATE, alpha=0.05)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-22, 30)
    ax.set_xlim(0.001, 3.0)
    ax.set_xlabel("学习率（对数刻度）", fontsize=9, color=SLATE)
    ax.set_ylabel("200 步后的相对损失", fontsize=9, color=SLATE)
    ax.set_title("固定跑 200 步：最终损失如何随 lr 变化", fontsize=10.5, color="#0F172A", pad=8)
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(GRID)
    ax.grid(alpha=0.25, color=GRID, lw=0.6)
    ax.legend(fontsize=8.2, frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_lr.png"), bbox_inches="tight")
    plt.close(fig)


def fig_descent():
    x = np.linspace(-1.0, 3.2, 400)
    f = lambda z: 0.5 * z ** 2 + 0.35 * np.sin(3 * z)
    df = lambda z: z + 1.05 * np.cos(3 * z)
    cur, lr = 2.25, 0.55
    g = df(cur)
    nxt = cur - lr * g
    fig, ax = plt.subplots(figsize=(6.3, 3.9), dpi=200)
    ax.plot(x, f(x), color="#334155", lw=2.0)
    ax.plot(cur, f(cur), "o", ms=8, color=TEAL, zorder=5)
    ax.plot(nxt, f(nxt), "o", ms=8, color=AMBER, zorder=5)
    tx = np.linspace(cur - 0.55, cur + 0.55, 20)
    ax.plot(tx, f(cur) + g * (tx - cur), ls="--", lw=1.2, color=BLUE)
    ax.annotate("", xy=(nxt, f(nxt)), xytext=(cur, f(cur)),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.8,
                                connectionstyle="arc3,rad=0.25"))
    ax.annotate("当前 θₜ", xy=(cur, f(cur)), xytext=(cur + 0.05, f(cur) + 0.35),
                fontsize=9, color=TEAL)
    ax.annotate("下一步 θₜ₊₁ = θₜ − η∇L", xy=(nxt, f(nxt)), xytext=(nxt - 0.4, f(nxt) + 0.55),
                fontsize=9, color=AMBER)
    ax.annotate("切线斜率 = 梯度 ∇L", xy=(cur + 0.35, f(cur) + g * 0.35), xytext=(cur + 0.55, f(cur) + g * 0.35 - 0.45),
                fontsize=8.5, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.set_xlabel("参数 θ", fontsize=9, color=SLATE)
    ax.set_ylabel("损失 L(θ)", fontsize=9, color=SLATE)
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(GRID)
    ax.grid(alpha=0.25, color=GRID, lw=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_descent.png"), bbox_inches="tight")
    plt.close(fig)


def fig_bias():
    t = np.arange(1, 41)
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)
    ax.plot(t, 1 - 0.9 ** t, color=BLUE, lw=2, label="一阶矩：1 − β₁^t（β₁=0.9）")
    ax.plot(t, 1 - 0.999 ** t, color=TEAL, lw=2, label="二阶矩：1 − β₂^t（β₂=0.999）")
    ax.axhline(1.0, color=GRID, lw=1, ls="--")
    ax.annotate("第 1 步：只有 0.1 / 0.001 的样本量", xy=(1, 0.1), xytext=(6.4, 0.30),
                fontsize=8.2, color=SLATE,
                arrowprops=dict(arrowstyle="-", color=SLATE, lw=0.8))
    ax.scatter([1, 1], [0.1, 0.001], color=[BLUE, TEAL], zorder=5, s=22)
    ax.set_xlim(1, 40)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("训练步数 t", fontsize=9, color=SLATE)
    ax.set_ylabel("修正系数", fontsize=9, color=SLATE)
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(GRID)
    ax.grid(alpha=0.3, color=GRID, lw=0.6)
    ax.legend(fontsize=8.2, frameon=False, loc="center right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_bias.png"), bbox_inches="tight")
    plt.close(fig)


def newton_schulz(G, steps=5):
    a, b, c = 3.4445, -4.7750, 2.0315
    X = G.astype(np.float32)
    X = X / (np.linalg.norm(X) + 1e-7)
    if X.shape[0] > X.shape[1]:
        X = X.T
    for _ in range(steps):
        A = X @ X.T
        B = b * A + c * (A @ A)
        X = a * X + B @ X
    if G.shape[0] > G.shape[1]:
        X = X.T
    return X


def fig_muon():
    rng = np.random.default_rng(7)
    n, r = 64, 32
    U, _ = np.linalg.qr(rng.normal(size=(n, n)))
    V, _ = np.linalg.qr(rng.normal(size=(r, r)))
    s = np.geomspace(1.0, 0.02, r)
    G = U[:, :r] @ np.diag(s) @ V.T
    O = newton_schulz(G)
    s_before = np.linalg.svd(G, compute_uv=False)
    s_after = np.linalg.svd(O, compute_uv=False)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.0), dpi=200,
                             gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axes[0]
    idx = np.arange(1, r + 1)
    ax.bar(idx - 0.2, s_before[:r], width=0.4, color="#94A3B8", label="正交化前：奇异值")
    ax.bar(idx + 0.2, s_after[:r], width=0.4, color=TEAL, label="Newton–Schulz 5 步后")
    ax.set_xlabel("奇异值序号", fontsize=9, color=SLATE)
    ax.set_ylabel("奇异值", fontsize=9, color=SLATE)
    ax.set_ylim(0, 1.58)
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(GRID)
    ax.grid(axis="y", alpha=0.3, color=GRID, lw=0.6)
    ax.legend(fontsize=8.2, frameon=False, loc="upper right")
    ax.set_title("谱被压平：从“几乎低秩”到接近正交", fontsize=11, color="#0F172A")

    ax = axes[1]
    a, b, c = 3.4445, -4.7750, 2.0315
    phi = lambda z: a * z + b * z ** 3 + c * z ** 5
    ax.axhspan(0.68, 1.13, color=TEAL, alpha=0.10)
    ax.axhline(1.0, color=GRID, lw=1, ls="--")
    for x0, col in [(0.02, "#94A3B8"), (0.3, BLUE), (0.7, TEAL), (0.95, AMBER)]:
        y = np.array([x0], dtype=float)
        seq = [x0]
        for _ in range(5):
            seq.append(float(phi(seq[-1])))
        ax.plot(range(6), seq, marker="o", ms=4, lw=1.6, color=col, label=f"x₀={x0}")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.4)
    ax.set_xlabel("迭代步数 k", fontsize=9, color=SLATE)
    ax.set_ylabel("归一化奇异值", fontsize=9, color=SLATE)
    ax.tick_params(colors=SLATE, labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(GRID)
    ax.grid(alpha=0.3, color=GRID, lw=0.6)
    ax.legend(fontsize=7.8, frameon=False, loc="lower right")
    ax.set_title("5 步后全部落进 [0.68, 1.13]（阴影带）", fontsize=11, color="#0F172A")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_muon.png"), bbox_inches="tight")
    plt.close(fig)
    return {"s_before": s_before[:6].round(3).tolist(),
            "s_after": s_after[:6].round(3).tolist(),
            "s_before_min": float(s_before[r - 1]), "s_after_min": float(s_after[r - 1]),
            "s_after_max": float(s_after.max())}


if __name__ == "__main__":
    res = {}
    res["landscape"] = _traj_panel()
    _lr_panel()
    fig_descent()
    fig_bias()
    res["muon"] = fig_muon()
    with open(os.path.join(HERE, "experiment-results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False, indent=2))
