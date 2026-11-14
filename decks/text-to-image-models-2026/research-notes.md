# 2026-11 文生图模型深度调研与交叉验证笔记

**快照时间**：2026-11-14（CST）  
**主数据源**：Artificial Analysis（AA）Image Arena 的 `textToImage` 子榜（人类两两盲选偏好 Elo）  
**辅助数据源**：厂商模型卡 / 官方博客 / GitHub README / ModelScope / 许可文本  
**样本**：综合质量榜第 1、6、7 名 + 开源子榜第 1、3、5 名（共 6 款）

> 重要口径：AA 同一页面存在 `textToImage` 与 `imageEditing` 两套独立 Elo，不能混用。此前部分二手榜单把编辑榜当成文生图榜，导致 Seedream、MiniMax H3 等模型被高估。本笔记一律使用 `textToImage` 子榜。

---

## 1. 排名与核心数字（AA T2I 子榜）

| 模型 | 类型 | T2I Elo | 95% CI | 全榜排名 | AA 代表性价格（USD/1k 张） |
|---|---|---:|---:|---:|---:|
| GPT Image 2.6 Sunburst (max) | 闭源 | **1260.7** | 1247–1275 | #1 | $210.72 |
| Kling Image 4.0 (preview) | 闭源预览 | **1179.9** | 1167–1193 | #6 | 未公开 |
| Nano Banana 2.1 | 闭源 | **1176.1** | 1164–1188 | #7 | $33.60 |
| MiniMax H3-Image Highspeed | 开源权重 | **1071.7** | 1058–1086 | #24 | $35.29 |
| MiniMax H3-Image | 开源权重 | **1065.7** | 1052–1080 | #25 | $21.79 |
| Qwen-Image-2.1-Pro | 开源权重 | **1058.2** | 1046–1070 | #26 | $35.33 |
| FLUX 3 Image Klein | 开源权重 | **1041.3** | 1030–1052 | #29 | $9.00 |

**读数**：
- 第 1 名与第 6 名相差约 81 Elo；第 6/7 名仅差 3.9 Elo，置信区间重叠，统计上不可区分。
- 开源第一（H3-Image 家族）与闭源第一相差约 189 Elo；价格却相差 6–23 倍。
- 价格是 AA 的“代表性 API 口径”，不是厂商账单；分辨率、档位、批量折扣会显著改变实际成本。

---

## 2. 六模型深度卡片

### 2.1 GPT Image 2.6 Sunburst (max) — OpenAI

- **定位**：当前 AA T2I 总榜第 1，质量天花板。
- **质量**：1260.7 Elo（CI 1247–1275），领先第 2 名约 31 分。
- **价格/速度**：AA 代表性价格 $210.72/千张；同代 Flare 档约 55 秒、Sunburst 档约 123 秒（AA 同代实测口径）。
- **能力判断**：高价值品牌主视觉、电影感场景、复杂材质与细节；不适合大批量与成本敏感场景。
- **证据状态**：
  - AA：T2I #1 / 1260.7（主证据）。
  - OpenAI 官网与 platform 文档在本环境返回 403，未能一手核验规格。
  - 发布日期 2026-11-04 来自二手报道，标注 `*`。
  - 结论：**B 级**——质量排名可信，官方规格/发布日期待核。

### 2.2 Kling Image 4.0 (preview) — 快手可灵

- **定位**：AA T2I 第 6，影视审美挑战者。
- **质量**：1179.9 Elo（CI 1167–1193），略高于 Nano Banana 2.1（1176.1），但差距在 CI 内。
- **价格/速度**：AA 无价格、无延迟数据；官方开放平台目前主推 Image 3.0 / 3.0 Omni，未检索到 4.0 的公开规格页。
- **能力判断**：影视概念、分镜预览、镜头语言与光影；暂不适合生产锁定。
- **证据状态**：
  - AA：T2I #6 / 1179.9（唯一量化来源）。
  - 可灵官网/开放平台：Image 3.0 & 3.0 Omni 为主，4.0 文档缺失。
  - 结论：**C 级**——只能先做 2 周 POC，等价格/SLA/规格公开后再评估。

### 2.3 Nano Banana 2.1 — Google DeepMind

- **定位**：综合最均衡的生产主力。
- **质量**：AA T2I 1176.1（CI 1164–1188），全榜 #7；官方 Overall Preference 1050±14（Thinking）。
- **官方规格（Model Card，2026-10-06）**：
  - 基于 Gemini 3.6 Flash；输入最多 1M token；输出 4K 图像 + 64K 文本。
  - 分发：Gemini App、Google AI Studio、Gemini API、Search AI Mode、Google Ads、Google Flow、Google Stitch。
- **官方专项基准**：
  - Infographic Design：1048±17（NB2 为 961±12，NB Pro 912±12）。
  - Infographic Factuality：0.521（NB2 0.179，NB Pro 0.265）。
  - General Editing：1026±12；Multi-Character Consistency：1106±14。
- **已知限制（官方）**：1K 小字易糊、长段落/整页文字弱；角色一致性不完美；空间左右定位偶有混淆；知识截止 2026-03。
- **证据状态**：**A 级**——官方模型卡 + AA 方向一致；实际账单按 token/分辨率计费，需另核。

### 2.4 MiniMax H3-Image — MiniMax

- **定位**：开源质量第一梯队，4K 速度型选手。
- **质量**：AA T2I base 1065.7（#25）；Highspeed 1071.7（#24）。
- **官方规格（2026-11-11 博客 + GitHub README）**：
  - 33.1B DiT、50 层、hidden 5376、56 heads、FFN 14336；BF16 DiT 68.65GB。
  - 单流 Transformer；Qwen3-VL 文本编码器；16× VAE 下采样、24 latent channels。
  - 4K（4096×4096，约 16MP）<10 秒；6 步采样；最多 16 张参考图；prompt 最多 32K 字符。
  - 支持 text-to-image 与 image editing；1–10 张/请求；输出 PNG/JPEG/WebP。
  - 暂不支持：mask inpainting、透明背景、用户指定 seed、预览图。
- **部署**：SGLang / vLLM-Omni / Diffusers / ComfyUI；含文本编码器约 135GB；官方称可从 B300 到 12GB 显卡的 recipes。
- **许可**：MiniMax-H3-Image Community License；商用需按 Section IV 提交书面授权申请。
- **证据状态**：**A- 级**——规格/许可一手，AA Elo 单源；独立第三方横向评测仍少。

### 2.5 Qwen-Image-2.1-Pro — 阿里 Qwen

- **定位**：中文、透明素材、统一编辑的开源性价比方案。
- **质量**：AA T2I Pro 1058.2（#26）；Turbo 1024.7（#39）。
- **官方规格（2026-09-20 开源；Pro/Turbo API 2026-10-09）**：
  - 7B 视觉生成组件、32 层 Single-Stream DiT；混合粒度 attention + prefix KV cache。
  - 统一文生图 + 编辑；原生 RGBA 透明图生成/编辑；最多 10 张参考图。
  - 支持圈选、涂鸦、mask 局部编辑；Turbo 8 步；base 40 步。
- **许可**：Qwen Research License Agreement（不是 Apache/MIT）。
- **生态**：Day-0 Diffusers / ComfyUI / vLLM-Omni / SGLang / LightX2V / OpenVINO。
- **证据状态**：**B+ 级**——能力/许可一手，AA Elo 单源；Pro 托管版与开源权重的质量差异待核。

### 2.6 FLUX 3 Image Klein — Black Forest Labs

- **定位**：成本杀手 / 本地部署首选。
- **质量**：AA T2I 1041.3（#29），开源子榜第 4。
- **官方规格（2026-10-15）**：
  - 5.6B 参数；text-to-image + image editing + 最多 10 张参考图。
  - 原生 4K；bbox 定位；像素级编辑；base + step-distilled 两个版本。
  - BF16 11.2GB / FP8 5.6GB / INT8 8GB 显存；1MP 约 4 秒（RTX 5090，16 步）、<9 秒（RTX 4070，ComfyUI）。
  - API $0.009/1K 图；ComfyUI / Diffusers / TensorRT-LLM / SGLang / vLLM-Omni / LoRA。
- **许可**：FLUX Kommunity License；个人及年收入 <$5M 的企业可免费商用，超过需自托管授权或 API。
- **证据状态**：**A- 级**——规格/许可一手；但 BFL 内部评测称“开源第一”，AA 大众偏好仅 #29，两者方向冲突，需以业务盲测为准。

---

## 3. 交叉验证矩阵

| 模型 | 质量（AA） | 官方规格 | 许可 | 价格 | 主要分歧/缺口 | 等级 |
|---|---|---|---|---|---|---|
| GPT Image 2.6 | #1 / 1260.7 | 官网 403 | 专有 | $210.7 | 发布日期/规格为二手 | B |
| Kling 4.0 preview | #6 / 1179.9 | 官方 4.0 文档缺失 | 专有 | 未公开 | 价格/SLA/规格未知 | C |
| Nano Banana 2.1 | #7 / 1176.1 | Model Card 完整 | 专有 | $33.6 | 账单口径需按 token 核 | A |
| H3-Image | #25 / 1065.7 | 博客+README 完整 | Community | $21.8 | 独立评测少；135GB 部署 | A- |
| Qwen 2.1 Pro | #26 / 1058.2 | README/ModelScope | Research | $35.3 | Pro 与开源权重差异 | B+ |
| FLUX 3 Klein | #29 / 1041.3 | 官方博客完整 | Kommunity | $9.0 | 厂商自称第一 vs AA #29 | A- |

---

## 4. 关键交叉验证发现

1. **AA T2I 与 AA Image Editing 是两套分**  
   - GPT Image 2.6：T2I 1260.7 / Editing 1210.4  
   - Nano Banana 2.1：T2I 1176.1 / Editing 1152.4  
   - H3-Image：T2I 1065.7 / Editing 1136.8  
   - Seedream 5.5：T2I 1133.9 / Editing 1159.8  
   结论：引用时必须写清子榜，否则排名会失真。

2. **厂商内部第一 ≠ 大众偏好第一**  
   - BFL 官方称 FLUX 3 Klein 在内部评测中“开源第一”，但 AA T2I 仅 #29（1041.3），低于 H3-Image 与 Qwen 2.1 Pro。  
   - 解释：内部评测的 prompt 分布、评分者、对比模型不同；上线前必须用业务 prompt 盲测。

3. **Kling 4.0 是“榜上有名、官方无声”**  
   - AA 给出 #6 / 1179.9，但可灵开放平台仍以 Image 3.0 / 3.0 Omni 为主，4.0 无公开规格、价格、SLA。  
   - 结论：只能作为 POC 备选，不能进入生产选型 shortlist 的“已确认”栏。

4. **开源不是“免费”**  
   - FLUX Klein：8GB 显存可跑，但年收入 >$5M 需授权。  
   - Qwen 2.1：7B 可单卡试，但 Qwen Research License 商用需法务确认。  
   - H3-Image：约 135GB 推理资源，社区许可商用需书面授权。  
   - 自托管 TCO = GPU 折旧 + 电费 + 运维 + 模型更新 + 合规，不只是“权重免费”。

---

## 5. 选型建议

| 场景 | 首选 | 备选 | 关键理由 |
|---|---|---|---|
| 品牌主视觉 / 高价值商稿 | GPT Image 2.6 Sunburst | Nano Banana 2.1 | 质量天花板；控制张数 |
| 信息图 / 多语种海报 | Nano Banana 2.1 | GPT Image 2.6 | Infographic Elo 1048；事实性 0.521 |
| 中文海报 / 电商 / 透明素材 | Qwen-Image-2.1-Pro | Seedream 5.5 | 中文文字、原生 RGBA、局部编辑 |
| 4K 私有化 / 数据不出域 | H3-Image | FLUX 3 Image Klein | 4K<10s、开放权重、参考图编辑 |
| 大批量 / 成本敏感 | FLUX 3 Image Klein | H3-Image | $9/千张；INT8 8GB 显存 |
| 多轮编辑 / 一致性 | Nano Banana 2.1 | Qwen-Image-2.1-Pro | General Editing 1026；多角色 1106 |
| 影视概念 / 快速 POC | Kling 4.0 preview | Nano Banana 2.1 | 影视审美突出；但 preview |
| 默认主力 | Nano Banana 2.1 | — | 质量/价格/渠道最平衡 |

---

## 6. 来源清单

1. Artificial Analysis — Image Arena / Text to Image：<https://artificialanalysis.ai/text-to-image>（2026-11-14 抓取；T2I 子榜 Elo、CI、价格）
2. Google DeepMind — Nano Banana 2.1 Model Card（2026-10-06）：<https://deepmind.google/models/model-cards/nano-banana-2-1/>
3. MiniMax — H3-Image 官方博客（2026-11-11）：<https://www.minimax.io/blog/minimax-h3-image>
4. MiniMax — GitHub README：<https://github.com/MiniMax-AI/MiniMax-H3-Image>
5. Qwen — Qwen-Image-2.1 README：<https://github.com/QwenLM/Qwen-Image-2.1>
6. Qwen — ModelScope：<https://modelscope.cn/models/Qwen/Qwen-Image-2.1>
7. Black Forest Labs — FLUX 3 Image Klein（2026-10-15）：<https://bfl.ai/blog/flux-3-image-klein>
8. Kling 开放平台 / 可灵官网：<https://app.klingai.com/global/dev/document-api>
9. OpenAI 官方页：本环境 403，未能一手核验 GPT Image 2.6 规格。

---

## 7. 待核清单

- [ ] GPT Image 2.6 的官方发布日期、分辨率、价格档位、最大输入/输出规格（OpenAI 官网 403）。
- [ ] Kling Image 4.0 的价格、限流、SLA、正式 GA 时间、官方能力表。
- [ ] Qwen-Image-2.1-Pro 托管版与开源 7B 权重的能力差异、商用授权边界。
- [ ] FLUX 3 Klein 在真实业务 prompt 上的质量；厂商内部第一与 AA #29 的差异来源。
- [ ] H3-Image 在 12GB 显卡上的实际可用性/延迟（官方 recipes 声称支持，但需实测）。
- [ ] 所有模型的“有效成本”：重试率、人工审核、存储、合规、数据驻留。
