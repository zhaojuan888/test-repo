# Skill 体系命名治理（受控词表 / 命名漂移治理）

> 目的：消除 77 个 Skill 的命名漂移（camelCase / 中文长名 / 语义不明 / 版本后缀 / 前缀不一），
> 建立受控词表，让技能可按前缀稳定聚合、调用、检索。
> 创建：2026-08-23 ｜ 扫描路径：`~/.workbuddy/skills`（= `~/.config/opencode/skills` 软链，77 项）

## ⚠️ 执行红线（最高优先级）

1. **Skills 是 WorkBuddy ↔ OpenCode 软链共享**——改名同时影响两端，且其他工具/脚本可能按名调用。
2. **本文件只出方案，未经你明确确认，绝不自动执行改名/移动。**
3. 平台/通用类（`docx`/`xlsx`/`pptx`/`find-skills`/`python` 等）属工具自带，**不建议改**。
4. 仅「非 skill 文件混在 skills 目录」可安全隔离（移入 `8-系统/`）。

## 一、受控词表（目标命名规范）

**格式**：`{domain}-{action}`，全小写 kebab-case，ASCII；动词或名词结尾；无版本后缀；无裸名词。
**专家视角**：`{name}-perspective`（如 `chen-yiwei-perspective`）。

**前缀分类（受控）**
| 前缀 | 领域 | 例 |
|---|---|---|
| `audit-` | 审计程序/底稿/核查 | audit-report-checker, audit-tb-workpaper-review |
| `tax-` | 税务 | tax-audit-toolkit |
| `fdd-` | 财务尽调 | fdd-process-guide |
| `ipo-` | IPO | ipo-inquiry-analyst |
| `fin-` | 通用财务分析 | financial-analysis |
| `extract-` | OCR/单据提取 | extract-invoice（提案） |
| `doc-` / `office-` | 文档处理 | docx, pdf-to-markdown |
| `kg-` / `kb-` | 知识库管理 | shenji-kb-manager, llm-wiki |
| `skill-` | 技能元管理 | skill-creator, skill-inventory-manager |
| `expert-` / `*-perspective` | 专家视角 | chen-yiwei-perspective |
| `web-` / `search-` | 检索 | kimi-web-bridge（提案）, find-skills |
| `viz-` | 可视化 | seaborn-visualization |
| `sec-` / `cninfo-` | 证券/公告 | cninfo-announcement-downloader |

## 二、全量 77 项分类（节选关键）

**A. 审计/财务/税务/尽调（用户技能，治理重点）**
audit-cutoff-testing, audit-data-analytics, audit-financial-analysis-tool, audit-income-detail-test,
audit-problem-classifier, audit-report-checker, audit-sampling-calculator, audit-tb-workpaper-review,
audit-workpaper-review, bank-flow-reconciliation, china-accounting-skills, china-law-search,
cicpa-company-query, cninfo-announcement-downloader, construction-inprogress-anomaly, cost-calculation,
fraud-investigation, fdd-process-guide, industry-benchmarking, it-audit-toolkit, ipo-inquiry-analyst,
legal-risk-analyzer, management-suggestion-letter, payable-nature-tagging, rd-expense-diagnosis,
regulatory-penalty-evaluator, related-party, shenji-kb-manager, tax-audit-toolkit,
tianchuan-audit-perspective, chen-yiwei-perspective, gridman★, kimi-data-tools-v2★, kimi-webbridge★,
darwin-skill, ponytail, ponytail-audit, ponytail-debt, ponytail-review, voucher-pdf-split, topic-splitter,
safe-recycle-delete, single-subject-note-link-replace, note-link-batch-replace, docx-version-diff,
企查查企业信息全量提取与高管对外投资明细★, 存货计价测试-加权平均法★

**B. 平台/通用（不建议改）**
docx, xlsx, pptx, wps-excel, wps-office, wps-ppt, wps-word, pdf-to-markdown, md-to-pdf,
find-skills, skill-creator, skill-inventory-manager, python, simplify, casting, local-rag, llm-wiki,
ima-skill, mineru-document-extractor, seaborn-visualization, data-analyst, financial-analysis,
claude-financial-services, invoice-recognition-and-extract, purchase-order-recognition-and-extract,
adp-document-extract

**C. 非 skill 文件（需隔离）**
`skills_catalog.md`, `_bm_skillid_migration.json`

## 三、漂移发现

| # | 现状名 | 漂移类型 | 提案名 | 风险 |
|---|---|---|---|---|
| 1 | `gridman` | 语义不明（无领域/视角标识） | `gridman-audit-perspective` | 中（对齐 *-perspective 家族） |
| 2 | `企查查企业信息全量提取与高管对外投资明细` | 超长中文名、无前缀 | `qcc-company-full-extract` | 中（拼音缩写对齐 cicpa-company-query） |
| 3 | `存货计价测试-加权平均法` | 中英混排+短横不一致 | `inv-valuation-weighted-avg` 或 `存货计价-加权平均法` | 低（保留中文亦可，需统一分隔） |
| 4 | `kimi-data-tools-v2` | 版本后缀（暗示有 v1 残留） | `kimi-data-tools` | 中（先确认无 v1 冲突再改） |
| 5 | `kimi-webbridge` | 复合词未拆（webbridge） | `kimi-web-bridge` | 低 |
| 6 | `related-party` | 缺领域前缀 | `audit-related-party` | 低（或 `fdd-related-party`） |
| 7 | `regulatory-penalty-evaluator` | 缺领域前缀 | `fdd-penalty-evaluator` / `reg-penalty-evaluator` | 低 |
| 8 | `mineru-document-extractor` vs `pdf-to-markdown` | 功能重叠（PDF→md） | 保留，补 scope 说明（MinerU=大模型解析/含扫描；pdf-to-markdown=轻量） | 低（不强制改） |
| 9 | `invoice-recognition-and-extract` / `purchase-order-recognition-and-extract` / `adp-document-extract` | `-and-extract` vs `-extract` 不一致 | `extract-invoice` / `extract-po` / `extract-adp`（动词前置） | 中（疑平台技能，需谨慎） |
| 10 | `note-link-batch-replace` / `single-subject-note-link-replace` | 缺 `audit-` 前缀（实为审计附注链接） | `audit-note-link-batch-replace` / `audit-note-link-single` | 低-中 |
| 11 | `gridman`/`企查查…`/`存货…` | 中文/英文混用 | 统一 kebab ASCII 或统一中文短横 | 见上 |

## 四、非 skill 文件隔离（可安全执行）

- `skills_catalog.md` → 移入 `8-系统/skills_catalog.md`（或 `3-知识地图/`）
- `_bm_skillid_migration.json` → 移入 `8-系统/`（迁移元数据，非技能）

## 五、治理动作建议（待确认后执行）

1. **先隔离非 skill 文件**（安全，立即可做）。
2. **低/中风险重命名**（#3/5/6/7/10）按提案改名，改后同步更新 `SKILL.md` 内 `name` 字段与该技能被引用处。
3. **中风险改名**（#1/2/4/9）需你确认，因涉及专家视角家族、拼音缩写、版本清理、平台技能。
4. **功能重叠**（#8）先补 scope 说明、观察使用频率，再决定是否合并。
5. 改名后全局 `grep` 旧名引用（含 OpenCode 侧），确保无断链。

> 下一步：你确认"执行隔离 + 低/中风险改名"后，我再动手；平台类（B 组）默认不改。
