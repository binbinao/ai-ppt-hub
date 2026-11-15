# 调研与口径笔记

**调研快照**：2026-11-15（CST）  
**用途**：新能源电池生产线科普 deck；不构成投资建议。

## 关键事实与来源

### 1. 需求规模

- 2025 年全球电动车电池部署量约 **1.2 TWh**，同比增长接近 **30%**，是 2020 年的 **7 倍以上**。
- 来源：IEA, *Global EV Outlook 2026 — Electric vehicle batteries*  
  https://www.iea.org/reports/global-ev-outlook-2026/electric-vehicle-batteries

### 2. 电池包价格

- 2025 年全球锂电池包均价 **108 美元/kWh**，同比下降 **8%**，创历史新低。
- BEV 电池包均价 **99 美元/kWh**；LFP 电池包均价 **81 美元/kWh**；NMC 电池包均价 **128 美元/kWh**。
- 来源：BloombergNEF, *Lithium-Ion Battery Pack Prices Fall to $108 Per Kilowatt-Hour*（2025-12-09）  
  https://about.bnef.com/insights/clean-transport/lithium-ion-battery-pack-prices-fall-to-108-per-kilowatt-hour-despite-rising-metal-prices-bloombergnef/

### 3. 生产速度与精度

- 一座大型 38 GWh/年工厂每天约生产 **600 万颗圆柱电芯**，约 **70 颗/秒**。
- 现代电池制造需要控制到 **几微米级** 的几何公差，同时避免微米级颗粒污染。
- 来源：Attia et al., *Challenges and opportunities for high-quality battery production at scale*, Nature Communications 16, 611 (2025).  
  https://pmc.ncbi.nlm.nih.gov/articles/PMC11725600/  
  DOI: 10.1038/s41467-025-55861-7

### 4. 工艺流程

- 前段：制浆、涂布、干燥、辊压、分切、制片/模切。
- 中段：卷绕或叠片、入壳、焊接、注液、封口。
- 后段：化成、分容、老化、检测、分档。
- 来源：
  - 安永《锂电池制程 10 大技术趋势》  
    https://www.ey.com/content/dam/ey-unified-site/ey-com/zh-cn/insights/strategy/documents/ey-10-technical-trends-of-lithium-ion-battery-industry-zh.pdf
  - RWTH PEM, *Lithium-Ion Battery Cell Production Process*  
    https://www.pem.rwth-aachen.de/global/show_document.asp?id=aaaaaaaaabdqbtk

### 5. 成本结构

以 4680 NMC811 电芯的公开满成本模型为例（不含材料回收）：

| 项目 | 占比 |
|---|---:|
| 材料 | 82.9% |
| 折旧 | 7.4% |
| 管理 / 其他 | 5.9% |
| 能源 | 2.3% |
| 人工 | 1.5% |

- 来源：Duffner et al., *Cost modeling for the GWh-scale production of modern lithium-ion battery cells*, Communications Engineering 3, 155 (2024).  
  https://www.nature.com/articles/s44172-024-00306-0  
  DOI: 10.1038/s44172-024-00306-0
- 口径提醒：该模型是特定产能、特定化学体系与特定假设下的满成本，不等于当前市场报价；不同地区、材料价格、良率和产能利用率会显著改变结果。

### 6. 良率与报废率

- 新线爬坡阶段报废率可能约 **30%**；成熟产线可降到 **5%–10%**。
- 来源：Roland Berger / RWTH PEM, *Battery Monitor 2022: Battery production and Product performance*（2023-03-16）  
  https://www.rolandberger.com/en/Insights/Publications/Battery-Monitor-2022-Battery-production-and-Product-performance.html
- 口径提醒：这是行业观察区间，不是某一家企业的公开良率。

## 写作边界

- 本 deck 面向科普受众，重点解释“为什么难”和“关键控制点”，不展开具体设备型号、工艺窗口和商业报价。
- 所有数字均在页面或 README 标注来源；无法确认的内容不写成确定事实。
- 不构成投资建议。

---

## 补充：图片来源（图文增强版新增）

本 deck 的配图分两类，逐张署名与授权链接见 [image-credits.md](image-credits.md)：

1. **真实照片**：全部来自 Wikimedia Commons 开放授权作品。主要包括 Oak Ridge National Laboratory 的 Battery Manufacturing Lab 产线照片（CC BY 2.0）、RudolfSimon 的电极涂布机（CC BY 3.0）与圆柱电芯拆解（CC BY-SA 3.0）、US DOE / Sandia / NTSB 的电极与电池包层级图（Public domain）、以及圆柱/方形电芯照片（CC0 / CC BY-SA 4.0）。
2. **工艺示意图**：由本 deck 用代码依据公开工艺资料绘制（涂布与干燥、辊压、卷绕 vs 叠片、装配六步、化成 SEI、良率爬坡、质量链、成本拆解、三种电芯形态、锂离子路径）。用于解释机理，不是设备图纸。

**勘误**：初版曾把 `Lithium ion battery.png`（电化学能级图）误当作充放电路径图、把 `PrismaticCell.png`（带英文标注的材料说明图）误当作方形电芯剖面图。图文增强版已把两者从正式页面移除，改用自行绘制的准确示意图与真实电芯照片。

**关于 AI 生图**：本机 `openai-image-gen` 技能存在，但 `OPENAI_API_KEY` 未配置、media-desk image 配置为空、OpenAI 端点不可达，因此**没有使用付费 AI 生图**。对技术科普而言，开放授权的真实照片 + 精确绘制的机理图，比「看起来像但可能画错」的生成图更可靠、可核查。
