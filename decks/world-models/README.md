# 世界模型：从想象中学习

![cover](cover.png)

81 页世界模型技术全景：从 Ha & Schmidhuber 2018 到 Genie 3 / Dreamer 4，覆盖 16 篇论文、19 张论文原图、每页演讲备注。

方法上借用 [skJack/kelip-paper-reading](https://github.com/skJack/kelip-paper-reading) 的精读框架：动机 → 架构 → 训练 → 数据 → 信息流 → 例子。

## 文件

| 版本 | 页数 | PPTX | PDF |
|---|---|---|---|
| 世界模型（图文版） | 81 | [世界模型-从想象中学习.pptx](世界模型-从想象中学习.pptx) | [.pdf](世界模型-从想象中学习.pdf) |

## 结构

| 部分 | 页码 | 内容 |
|---|---|---|
| 导读 | 1–6 | 六站法、定义、时机、谱系、四个误解 |
| P1 三块积木 | 7–9 | 表示、动力学、条件；评估三维 |
| P2 RL 时代 | 10–18 | World Models、Dreamer、MuZero、DreamerV3 |
| P3 生成式转向 | 19–40 | GAIA-1、UniSim、Genie、GameNGen、Cosmos、GAIA-2、iVideoGPT |
| P4 另一条路 | 41–52 | V-JEPA、V-JEPA 2、Dreamer 4、WorldVLA、π0.7 |
| P5 训练与评估 | 53–61 | 一条样本、四种目标、数据、漂移、WorldScore |
| P6 应用 | 62–66 | 机器人、自动驾驶、游戏、科学 |
| P7 局限 | 67–72 | 物理幻觉、可控性、评测、版权、Scaling 争论 |
| P8 判断 | 73–81 | 三种定义、选型、上手、未来、总结、术语、来源 |

## 论文原图清单

| 页 | 图 | 来源 |
|---|---|---|
| 12 | V-M-C 架构 | World Models, arXiv:1803.10122, Fig. 3 |
| 13 | 信息流 | World Models, arXiv:1803.10122, Fig. 8 |
| 16 | 规划/行动/训练 | MuZero, arXiv:1911.08265, Fig. 1 |
| 22 | 多模态生成 | GAIA-1, arXiv:2309.17080, Fig. 1 |
| 24 | 训练与推理 | UniSim, arXiv:2310.06114, Fig. 2 |
| 25 | 长时推演 | UniSim, arXiv:2310.06114, Fig. 4 |
| 27 | 可玩环境 | Genie, arXiv:2402.15391, Fig. 1 |
| 28 | 训练管线 | Genie, arXiv:2402.15391, Fig. 2 |
| 29 | ST-Transformer | Genie, arXiv:2402.15391, Fig. 3 |
| 32 | 实时 DOOM | GameNGen, arXiv:2408.14837, Fig. 1 |
| 33 | 自回归漂移 | GameNGen, arXiv:2408.14837, Fig. 4 |
| 36 | 多视角架构 | GAIA-2, arXiv:2503.20523, Fig. 2 |
| 38 | 交互式 VideoGPT | iVideoGPT, arXiv:2405.15223, Fig. 3 |
| 43 | 特征预测训练 | V-JEPA, arXiv:2404.08471, Fig. 7 |
| 45 | 理解/预测/规划 | V-JEPA 2, arXiv:2506.09985, Fig. 1 |
| 46 | 规划 | V-JEPA 2, arXiv:2506.09985, Fig. 7 |
| 48 | 想象训练 | Dreamer 4, arXiv:2509.24527, Fig. 1 |
| 50 | 动作 + 世界模型 | WorldVLA, arXiv:2506.21539, Fig. 2 |
| 61 | 基准设计 | WorldScore, arXiv:2504.00983, Fig. 2 |

## 来源

- 论文：World Models (1803.10122)、Dreamer (1912.01603)、MuZero (1911.08265)、DreamerV3 (2301.04104)、GAIA-1 (2309.17080)、UniSim (2310.06114)、Genie (2402.15391)、V-JEPA (2404.08471)、iVideoGPT (2405.15223)、GameNGen (2408.14837)、Cosmos (2501.03575)、GAIA-2 (2503.20523)、WorldScore (2504.00983)、V-JEPA 2 (2506.09985)、WorldVLA (2506.21539)、Dreamer 4 (2509.24527)
- 博客：Genie 2（2024.12）、Genie 3（2025.08）、Sora（2024.02）
- 方法参考：skJack/kelip-paper-reading（六站精读法）

## 口径说明

- 论文原图按 arXiv HTML 下载，最长边 2400px、JPEG q=90；版权归原作者。
- 标注“官方博客口径”的数字（Genie 2/3 的分辨率、帧率）未逐条核对论文。
- Cosmos 的数据规模与算力为论文口径的近似值，标注“约”。
