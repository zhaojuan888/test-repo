# Activity Log

## [2026-08-02 13:30] migrate | wiki → 2-知识库，清理旧目录
- 迁移 4 篇准则笔记 → 2-知识库/会计准则/
- 迁移 3 篇审计程序 → 2-知识库/审计程序/
- 迁移 4 篇案例 → 2-知识库/处罚案例/
- 迁移旧模板 → 4-模板/（准则笔记、审计发现、客户笔记）
- 删除旧目录：wiki/ raw/ templates/
- 移动 2026年度审计.md → 1-项目/

## [2026-08-02 13:22] upgrade | 知识库升级至 PARA+Zettelkasten 体系
- Created: 8-系统/CLAUDE.md
- Created: Home.md（Dataview 仪表盘）
- Created: 3-知识地图/（6个 MOC）
- Created: 4-模板/（6个模板）
- Created: 2-知识库/处罚案例/2025-利安达-江平生物-存货审计失败.md

## [2026-08-01 22:16] create | 初始概念页
- Created: CAS 14、CAS 1141


## [2026-08-02 21:13] restructure | Karpathy 三层管线改造
- 新增 9-产出/（outputs 层）+ index.md
- 2-知识库 下 6 个子领域各新增 index.md（AI学习/会计准则/处罚案例/审计程序/税法/行业研究）
- 删除空的 5-参考资料/（原始资料统一走 0-收件箱）
- Home.md：加入产出中心入口 + 工作流说明
- 8-系统/每日使用指南.md：加入四步知识流（收集→消化→连接→产出）
- 8-系统/CLAUDE.md：架构树 + 工作流同步更新

## [2026-08-02 21:18] commit | 7c72652 feat: Karpathy三层管线改造，固化规则到CLAUDE.md
- git 提交结构改造 + Karpathy 规则固化（11 files, +238/-4）
- CLAUDE.md 新增「Karpathy 规则（最高优先级）」：三层管线/数据流/强制清单/Lint
- 未提交：.obsidian 插件配置 + 3 个笔记的 LF→CRLF 行尾符差异（无实质内容变化）

## [2026-08-02 21:39] plugins | 安装 8 个 Obsidian 插件（审计师场景定制）
- 第一梯队：obsidian-pdf-plus / quickadd / omnisearch / various-complements
- 第二梯队：obsidian-spaced-repetition / smart-connections / obsidian-tasks-plugin
- 附加：table-editor-obsidian（Advanced Tables）
- 来源：GitHub release（various-complements 官方仓库含 -plugin 后缀，初装 404 已修正）
- 隐私红线：smart-connections 本地嵌入不出机器；Copilot 未装（客户资料敏感性）

## [2026-08-02 21:51] plugins | 安装 Copilot for Obsidian v3.3.3（AI 对话）
- 目的：用户要求与知识库 AI 对话（Vault QA）
- 后端：默认 SiliconFlow DeepSeek（SILICONFLOW_API_KEY）+ 备用 Kimi（MOONSHOT_API_KEY）
- Key 已存在于用户级环境变量，未写入 vault（避免明文入 git）
- 嵌入模型：SiliconFlow Qwen3-Embedding-0.6B（本地索引）
- 待用户手动配置：Settings → Copilot → Basic 填入两个 Key + 添加 Kimi 自定义模型

## [2026-08-02 21:53] privacy | Copilot 隐私隔离配置
- 预写 data.json：siliconflowApiKey + qaExclusions="copilot, 1-项目"
- 默认模型 DeepSeek-V4-Flash|siliconflow，嵌入 Qwen3-Embedding-0.6B|siliconflow
- data.json 加入 .gitignore（防 Key 入库）
- 待办：重启 Obsidian 验证加载；Kimi 走 UI 添加自定义 provider

## [2026-08-23 20:50] staging | 补完 staging_convert.py + 标签规范（0-收件箱自动转 md）
- 重写 `8-系统/staging_convert.py`：新增链接类（.url/.webloc/纯URL文本）→ `情报` 型待抓取笔记（tags: staging/web/capture/平台 + platform 字段）；截图类（png/jpg）→ 占位笔记 + 入 _needs_ocr.txt，tags 加 MinerU/capture/截图；修 .md 源文件双后缀命名；加 --dry-run。
- 建 managed venv（注意 Windows 用 Scripts\ 非 bin\）装 pypdf/python-docx/openpyxl/watchdog，沙箱+真实 0-收件箱均验证通过。
- 固化 `4-模板/标签规范.md`：status 受控词表补 `待归类`；来源维度加 `capture`/`截图` + 平台标签；新增「六、捕获与补采工作流（视频号/B站盲区）」。
- 新建 `8-系统/ima_rag_integration.md`（IMA RAG 接入方案：本会话 ima-mcp disconnected，需重连；敏感不出域红线；3 个 IMA 库 ID 检索约定）。
- 新建 `8-系统/skill_naming_governance.md`（77 技能命名治理：受控词表+全量分类+漂移表+重命名提案；软链共享高风险，只出方案不自动改名）。

## [2026-08-23 20:50] skills | 命名漂移治理（仅出方案）
- 77 技能中漂移点：gridman(语义不明)/企查查…(超长中文)/存货计价…(中英混排)/kimi-data-tools-v2(版本后缀)/related-party·regulatory-penalty(缺前缀)/extract 家族不一致。
- 非 skill 文件混在 skills 目录：`skills_catalog.md`、`_bm_skillid_migration.json` → 建议隔离至 8-系统/。
- 处置：待用户确认后执行隔离 + 低/中风险改名；平台类不改。