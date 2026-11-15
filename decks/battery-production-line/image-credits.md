# 图片来源与署名（Image Credits）

本 deck 使用了两类图：**① Wikimedia Commons 开放授权的真实照片**（下表逐张署名）；**② 本 deck 依据公开工艺资料用代码绘制的示意图**（无第三方版权）。

所有照片均从 Wikimedia Commons 下载，按原授权使用；为适配版式做了裁切与缩放，未改变内容。CC BY / CC BY-SA 要求署名，CC0 / Public domain 无署名要求但一并列出以便核查。

## 一、真实照片（Wikimedia Commons）

| deck 内文件 | 原始文件 | 作者 / 来源 | 授权 | 用于页 |
|---|---|---|---|---|
| `01-cover-line.jpg`, `02-factory-floor.jpg`, `13-lab-worker.jpg`, `14-lab-detail.jpg`, `22-hero-factory.jpg`, `22-hero-formation.jpg` | Battery Manufacturing Lab (50954222986 / 23376 / 28316 / 54326312).jpg | Oak Ridge National Laboratory | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0) | 1, 4, 6, 12, 19 |
| `03-coater-real.jpg`, `22-hero-coating.jpg` | [Electrode Coater.JPG](https://commons.wikimedia.org/wiki/File:Electrode_Coater.JPG) | RudolfSimon | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) | 6, 7 |
| `05-cell-formats.jpg`, `grid-05-formats.jpg` | Lithium Ion Battery Cell - Cylindrical Cell, Prismatic Cell, Pouch Cell.png | CRBAman | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 10 |
| `08-18650-21700.jpg`, `grid-01-cylinders.jpg` | 18650 and 21700 lithium ion battery cell.jpg | Sevenethics | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) | 10 |
| `07-cylindric-open.jpg`, `grid-02-cylindric-open.jpg`, `grid-04-jellyroll.jpg` | Lithium-Ion Cell cylindric.JPG | RudolfSimon | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | 10 |
| `11-catl-lfp-cell.jpg`, `grid-03-prismatic.jpg` | CATL Lifepo4 302Ah.jpg | Aeroid | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 10 |
| `15-catl-plant.jpg` | CATL Arnstadt.jpg | Giorno2 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 备用 |
| `12-battery-pack.jpg`, `10-doe-graphic.jpg`, `grid-06-pack.jpg` | Graphic-working (50831686767).jpg | National Transportation Safety Board / US DOE | Public domain | 5, 10 |
| `04-electrode-hand.jpg` | U.S. Department of Energy - Science - 419 001 010 (9951392125).jpg | U.S. Department of Energy (Sandia) | Public domain | 8 |
| `16-doe-electrode.jpg` | U.S. Department of Energy - Science - 394 053 002 (9404534338).jpg | U.S. Department of Energy | Public domain | 备用 |
| `09-liion-schematic.jpg` | Lithium ion battery.png | Walter Davison | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 备用（未用于正式页） |
| `06-prismatic-section.jpg` | PrismaticCell.png | ArcturusNotTaurus | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 备用（未用于正式页） |

> 说明：`09-liion-schematic.jpg` 是电化学能级图，`06-prismatic-section.jpg` 是带英文标注的材料说明图；初版曾误用，现已从正式页面中移除，仅保留在 `images/` 目录作为素材存档。

## 二、示意图（本 deck 自行绘制）

以下图由 `make_diagrams.py` / `make_extra.py` / `make_liion_path.py` / `make_s03.py` 用 Pillow 绘制，依据公开工艺与原理资料，用于解释机理，**不是设备图纸或工艺参数规范**：

| 文件 | 内容 | 用于页 |
|---|---|---|
| `diagram-01-coating-drying.png` | 狭缝挤压涂布与多段干燥 | 7 |
| `diagram-02-calendering.png` | 辊压前后颗粒堆积对比 | 8 |
| `diagram-03-winding-vs-stacking.png` | 卷绕 vs 叠片剖面结构 | 9 |
| `diagram-04-cell-assembly.png` | 电芯装配六步 + 干燥间 | 13 |
| `diagram-05-formation-sei.png` | 化成 SEI 成膜与首次充电曲线 | 14 |
| `diagram-06-yield-21x9.png` / `diagram-06-yield-ramp.png` | 良率爬坡曲线 | 16 |
| `diagram-07-process-quality-chain.png` | 前中后段工序 + 检测关口 + 损失递增 | 18 |
| `diagram-08-cost-breakdown.png` | 电芯满成本构成 | 15 |
| `diagram-09-cell-formats.png` | 圆柱 / 方形 / 软包结构示意 | 11 |
| `diagram-10-liion-path-portrait.png` | 锂离子充放电路径（S03 右半屏） | 3 |

## 三、授权提示

- CC BY / CC BY-SA 素材已在本文件署名并给出授权链接；若二次分发，请保留本文件。
- CC BY-SA 的「相同方式共享」要求：若你修改并再分发这些具体照片，需沿用相同授权。本 deck 中的**示意图与排版**不受此约束。
- 原始文件页面与完整元数据见 `research-notes.md` 及 `.research/commons_meta.json`（本地工作区）。
