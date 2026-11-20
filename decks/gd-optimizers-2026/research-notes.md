# 研究笔记与来源核对

**主题**：从下山到矩阵几何：梯度下降优化器的七十年（SGD → 动量 → Adam → AdamW → Muon）
**交付**：37 页教学 PPT（PPTX + PDF + cover.png）
**整理日期**：2026-11-20
**核对原则**：论文与作者原文优先；博客、代码仓库作为工程证据；无法核验的常识性细节在正文标注，不替作者补数。

---

## 1. 一手来源总表

| ID | 文献 | 链接 | 本讲用途 |
|---|---|---|---|
| S1 | Cauchy, 1847, *Méthode générale pour la résolution des systèmes d'équations simultanées* | 历史文献（无在线原文） | 梯度下降最早的系统表述 |
| S2 | Robbins & Monro, 1951, *A Stochastic Approximation Method*, Ann. Math. Stat. 22(3) | https://doi.org/10.1214/aoms/1177729586 | 随机近似、噪声下收敛 |
| S3 | Polyak, 1964, *Some methods of speeding up the convergence of iteration methods* | https://doi.org/10.1016/0041-5553(64)90137-5 | Heavy-ball 动量 |
| S4 | Nesterov, 1983, *A method of solving a convex programming problem with convergence rate O(1/k²)* | Soviet Math. Dokl. 27 | 加速梯度 |
| S5 | Rumelhart, Hinton & Williams, 1986, *Learning representations by back-propagating errors*, Nature 323 | https://doi.org/10.1038/323533a0 | 反向传播让梯度算得动 |
| S6 | Duchi, Hazan & Singer, 2011, *Adaptive Subgradient Methods*, JMLR 12 | https://jmlr.org/papers/v12/duchi11a.html | AdaGrad |
| S7 | Hinton, 2012, Coursera *Neural Networks* lecture 6.5 | https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf | RMSProp（未正式发表） |
| S8 | Kingma & Ba, 2015, *Adam: A Method for Stochastic Optimization*, ICLR | https://arxiv.org/abs/1412.6980 | Adam 公式、默认超参、偏差修正 |
| S9 | Reddi, Kale & Kumar, 2018, *On the Convergence of Adam and Beyond*, ICLR | https://arxiv.org/abs/1904.09237 | Adam 收敛反例、AMSGrad |
| S10 | Loshchilov & Hutter, 2019, *Decoupled Weight Decay Regularization*, ICLR | https://arxiv.org/abs/1711.05101 | AdamW、15% 相对改进 |
| S11 | Wilson et al., 2017, *The Marginal Value of Adaptive Gradient Methods*, NeurIPS | https://arxiv.org/abs/1705.08292 | 自适应方法的泛化争议 |
| S12 | Jordan, 2024, *Muon: An optimizer for hidden layers in neural networks* | https://kellerjordan.github.io/posts/muon/ | Muon 定义、NS 系数、speedrun 战绩 |
| S13 | Moonshot AI, 2025, *Muon is Scalable for LLM Training* | https://arxiv.org/abs/2502.16982 | weight decay + update scale、2×、Moonlight |
| S14 | Kimi Team, 2025, *Kimi K2: Open Agentic Intelligence* | https://arxiv.org/abs/2507.20534 | MuonClip、QK-clip、15.5T tokens |
| S15 | Llama Team, 2024, *The Llama 3 Herd of Models* | https://arxiv.org/abs/2407.21783 | 405B 的 AdamW 配方 |
| S16 | Gupta et al., 2018, *Shampoo: Preconditioned Stochastic Tensor Optimization* | https://arxiv.org/abs/1802.09568 | 矩阵预条件的前史 |
| S17 | Vaswani et al., 2017, *Attention Is All You Need* | https://arxiv.org/abs/1706.03762 | 原版 Transformer 的 Adam 超参 |

补充提及但未逐页引用：Lion（arXiv:2302.06675）、Sophia（arXiv:2305.14342）、LAMB（arXiv:1904.00962）、Adafactor（arXiv:1804.04235）。

---

## 2. 逐页事实核对

### 历史线（p3、p6、p34）

- 1847 Cauchy 梯度下降；1951 Robbins–Monro 随机近似；1964 Polyak 动量；1983 Nesterov 加速；1986 反向传播；2011 AdaGrad；2015 Adam；2017 arXiv / 2019 ICLR AdamW；2024 Muon；2025 Moonshot / Kimi K2。年份均取自原文或论文首页。
- 时间线把 AdamW 标在 2017（arXiv 首版），正文与来源页标 ICLR 2019；两种写法都成立，正文没有把 2017 说成“正式发表”。

### 成本与动机（p4）

- 1.35×、约 2×、3.3→2.6 A100-seconds 均为原文数字（S12、S13）。
- “10% 效率差 = 数百万美元”是**示意性算术**，不是某篇论文的引用数字；页面用“算一笔粗账”明确标注为估算。前沿模型预训练成本以千万美元计是行业公开量级，但本页没有把它写成精确账单。

### SGD、病态曲率与学习率（p7–p9）

- 噪声方差与 batch size 成反比、曲率比 κ 决定收敛条件，是标准结论，未逐条引文。
- p8/p9 的步数、学习率区间来自本讲 Toy 实验（见第 3 节），不是文献数字。
- p9 的“稳定区间”是在 `0.001–3.0`、55 个对数网格点上、固定跑 200 步读出的；SGD 写 `0.001–0.019`、动量写“到 0.037”、Adam 写 `0.001–3.0`，都限定在这张网格内，没有外推。

### Adam（p13–p15）

- 默认 `β₁=0.9, β₂=0.999, ε=1e-8, lr=0.001`：S8。
- 偏差修正 `m̂=m/(1−β₁ᵗ)`、`v̂=v/(1−β₂ᵗ)`：S8 §3。
- “坐标尺度不变 / 步长有界 / 稀疏友好”是对 Adam 更新式的性质整理，不是论文原话；p15 的页脚标“本讲整理”。
- 首步 `m₁/(√v₁)=3.16·sign(g)` 是把 `β₁=0.9, β₂=0.999` 代入后的算术结果（`0.1/√0.001≈3.16`），属于本讲推导。

### 两次危机（p16–p17）

- Wilson et al. 2017：在若干视觉任务上，充分调参后 SGD+momentum 不输自适应方法；论文的核心论点之一是自适应方法找到的解泛化更差。p16 明确写“论文结论的转述，非原文引用”，没有伪造引号内容。
- Reddi et al. 2018：给出 Adam 在凸问题上的不收敛反例；AMSGrad 用 `v̂_t=max(v̂_{t−1},v_t)` 修复。p17 的“代价：更保守”是工程解读，不是论文原句。
- p16 “2019 年 AdamW … 追平 SGD+momentum”对应 S10 的 “compete with SGD with momentum”；原文更谨慎（CIFAR-10 缩小大部分差距、ImageNet32x32 可比），本讲用“追平”是教学化压缩，来源页保留原文措辞。

### AdamW（p18–p21）

- “L2 与 weight decay 对 SGD 等价、对 Adam 不等价”：S10 摘要第一句。
- “15% relative improvement in test error”：S10 §1（引言）与 §5（实验）；原文明确是**默认 lr=0.001** 下、CIFAR-10 与 ImageNet32x32 **两者都**达到 15% 相对改进，对比对象是 Adam+L2。
- 注意：15% **不在摘要里**。早期版本的本讲页脚曾写 “Table 1 / Abstract”，已改为 “§1 与 §5（15% 在引言与实验部分）”。
- “15% 是相对改进，不是绝对准确率 +15 点”：这是对 “relative improvement in test error” 的中文澄清，正确。
- Llama 3 405B：峰值 lr `8e-5`、8000 步 linear warmup、cosine 衰减到 `8e-7`、总 `1.2M` steps、weight decay `0.1`：S15 §3.3.1 / Table 3。**论文正文没有给出 β₁/β₂**，所以 p21 表格写“β 值正文未给出”，没有编造。

### Muon（p22–p29）

- 定义：只用于 2D hidden 参数；先 Nesterov 动量，再做 Newton–Schulz 正交化：S12。
- NS 系数 `(3.4445, −4.7750, 2.0315)`、5 步、bf16：S12。
- 目标是把奇异值压到 1 附近；作者说 `ε≈0.3` 的偏差不伤 loss，调参目标是让极限落在 `[0.7, 1.3]`：S12。本讲 p26 写 `[0.68, 1.13]` 是**本讲 Toy 实验**的实测区间，页脚同时标了“Jordan 2024；本讲 Toy 实验”，没有把实测值冒充论文值。
- 3.3→2.6 A100-seconds（CIFAR-10 94%）、NanoGPT 1.35×、1.5B 用 10 个 8×H100-hours（AdamW 13.3）、FLOP 开销 0.7%（NanoGPT）/0.5%（Llama 405B）、12 次记录由 7 位研究者保持：S12。
- “Muon 2024-10 发布”：博客记录了 2024-10-15 的 speedrun 改进；仓库/博客是 2024 年 10–12 月间公开。正文用“2024”年份，不写具体日。
- Moonshot：两个关键技术是加 weight decay、按参数调整 update scale；更新式 `W←W−η(0.2·O·√max(A,B)+λW)`；把 update RMS 对齐 AdamW 的 0.2–0.4；compute-optimal 下约 2×；Moonlight 3B/16B MoE、5.7T tokens、wd=0.1、峰值 lr=4.2e-4：S13。
- Kimi K2：1T 总参 / 32B 激活、15.5T tokens、零 loss spike；MuonClip = Muon + QK-clip；QK-clip 在 per-head max logit 超过阈值 `τ=100` 时把 `Wq←γ^α Wq`、`Wk←γ^(1−α) Wk`（逐 head），稳定后关闭：S14。
- 工程边界：embedding / 最终 classifier / 标量向量仍用 AdamW；Q/K/V 分开优化更好；只支持 2D（4D 卷积可 flatten）；尚未证明 fine-tune / RL 同样有效；分布式 NS 通信是难点：S12（作者“open questions”与实现说明）。

### 对比与选型（p30–p32）

- 三者对比表是**本讲综合**，不是某篇论文的表格；每一行的依据分散在 S8–S14。
- 选型决策树、六个坑是工程经验总结，依据是 S12–S15 的边界条件与常见失败模式，属于“本讲整理”，不是引用结论。
- p31 的“先问三个问题”（参数是不是 2D 矩阵、是否预训练、能否承担重调成本）是教学框架。

---

## 3. Toy 实验：参数、结果与可复现性

脚本：`experiment.py`（numpy + matplotlib，无 GPU）。
输出：`figs/fig_traj.png`、`figs/fig_lr.png`、`figs/fig_bias.png`、`figs/fig_muon.png`、`figs/fig_descent.png`、`experiment-results.json`。

### 3.1 病态二次函数

```
f(θ) = ½ θᵀHθ,  H = diag(1, 100),  κ = 100
初始点 θ₀ = (−2.6, 2.2)
目标：f(θ) < 1e-6 · f(θ₀)
最多 4000 步；发散判据 f > 1e6·f(θ₀) 或非有限
```

每种优化器独立做 40 点对数学习率网格：

- SGD / 动量：`geomspace(0.0005, 1.8/λmax, 40)`；
- Adam：`geomspace(0.002, 2.0, 40)`；
- 动量 `β=0.9`；Adam `β₁=0.9, β₂=0.999, ε=1e-8`。

结果：

| 优化器 | 最快步数 | 对应 lr |
|---|---|---|
| SGD | 263 | 0.0180 |
| 动量 | 90 | 0.00344 |
| Adam | 83 | 0.5789 |

> 读数：在这个**轴对齐**的二次函数上，Adam 的逐坐标归一化几乎抹平了 κ=100 的条件数；动量靠方向记忆；SGD 被最大曲率卡住步长。三个数字不能直接外推到真实网络。

### 3.2 学习率敏感性

固定 200 步，`geomspace(0.001, 3.0, 55)`，画 200 步后的相对损失：

- SGD 稳定到约 `0.019`，超过 `0.02` 发散；
- 动量稳定到约 `0.037`，之后出现“悬崖”；
- Adam 在 `0.001–3.0` 全区间都能把损失压下去，最优区间很宽。

这组数字只说明“对 lr 的容忍度”，不说明收敛速度或泛化。

### 3.3 偏差修正

`t=1` 时 `m₁=0.1g`、`v₁=0.001g²`，所以

```
m₁/√v₁ = 0.1g / (0.0316|g|) ≈ 3.16·sign(g)
```

除以 `(1−β₁ᵗ)`、`(1−β₂ᵗ)` 后回到 `1·sign(g)`。这是算术，不是实验拟合。

### 3.4 Muon 奇异值谱

- 64×32 随机矩阵，做 5 步 NS 迭代；
- 迭代前最小奇异值 `0.020`；
- 迭代后最小 `0.682`、最大 `1.132`；
- 结论：NS 把谱压到 1 附近，但不是精确 SVD；5 步足够用于教学演示。

### 3.5 已知局限

- 二次函数是凸的、轴对齐的，没有噪声、没有 mini-batch、没有权重衰减；它只演示“曲率 + 尺度”这一件事。
- 学习率网格的上界与“发散”判据会改变步数读数；本讲的数字只在这套判据内有效。
- Muon 的谱实验是单个随机矩阵，不是训练中的真实权重；不能据此推断收敛速度。

---

## 4. 未核验、争议与边界

1. **Transformer 原论文的 Adam 超参**（`β₂=0.98, ε=1e-9, warmup 4000`）是领域常识，本讲正文未逐字引用 S17；引用时请以原文 §5.3 为准。
2. **“AdamW 追平 SGD+momentum”** 是教学化压缩；原文是 “compete with”，且在 CIFAR-10 上是“缩小大部分差距”，ImageNet32x32 上是“可比”。严格表述见 S10。
3. **Wilson et al. 2017 的结论有适用范围**：它不是说“所有自适应方法在所有任务上都更差”，而是说在若干视觉任务、充分调参后，自适应方法的泛化优势不成立。本讲 p16 已写明是转述。
4. **Reddi 反例是凸问题上的构造**，不等于“Adam 在深度网络里一定不收敛”；工程上的 warmup / clip 也不是 AMSGrad 的等价替代，只是经验兜底。
5. **Muon 的“12 次记录 / 7 位研究者”** 是博客在写作时的统计，会随时间变化；本讲用它说明社区复现，不把它当作永久事实。
6. **Muon 的适用边界**：作者明确只覆盖预训练、2D hidden 参数；fine-tune、RL、embedding、输出层仍用 AdamW。Kimi K2 的 MuonClip 是工程改造（QK-clip），不是原版 Muon 的数学结论。
7. **Llama 3 的 β 值缺失**：论文没有给，p21 如实标注，没有用“常见默认值”冒充实测配置。
8. **成本页的“数百万美元”** 是量级估算，不是报价单；不同芯片、云价、利用率会改变结果。

---

## 5. 图表与版式

| 图 | 内容 | 生成方式 |
|---|---|---|
| `fig_traj.png` | κ=100 峡谷中 SGD / 动量 / Adam 的轨迹与步数 | `experiment.py::_traj_panel` |
| `fig_lr.png` | 固定 200 步，最终相对损失 vs 学习率 | `_lr_panel` |
| `fig_bias.png` | 偏差修正前后首步有效步长 | `_bias_panel` |
| `fig_muon.png` | NS 迭代前后的奇异值谱 + φ⁵ 收敛 | `_muon_panel` |
| `fig_descent.png` | 一维下山示意（切线、步长） | `fig_descent` |

版式：python-pptx，16:9（13.333×7.5 in），浅底卡片 + 顶部色条；中文 `Arial Unicode MS`，公式 `Times New Roman`，代码 `Menlo`；每页有演讲者备注。机检脚本 `workbench/pptx_lint.py` 对最终版输出 0 error / 0 warning。

---

## 6. 重新导出 PDF

本机没有 LibreOffice，使用 Microsoft PowerPoint（16.109.2）AppleScript 导出：

```bash
osascript <<'EOF'
tell application "Microsoft PowerPoint"
    activate
    open POSIX file "/Users/jiduobin/Downloads/workdir/gd-optimizers-2026/out/从下山到矩阵几何：梯度下降优化器七十年.pptx"
    delay 3
    set theDoc to active presentation
    save theDoc in POSIX file "/Users/jiduobin/Downloads/workdir/gd-optimizers-2026/out/从下山到矩阵几何：梯度下降优化器七十年.pdf" as save as PDF
    delay 2
    close theDoc saving no
end tell
EOF
```

封面：

```bash
pdftoppm -r 150 -png -f 1 -l 1 "out/从下山到矩阵几何：梯度下降优化器七十年.pdf" out/cover
sips -z 900 1600 out/cover-01.png --out out/cover.png
```

---

*本笔记只服务于这份教学 deck 的可核查性；所有引用以原始论文/作者博客为准，数字的适用条件见上文。*
