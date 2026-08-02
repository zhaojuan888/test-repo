---
type: procedure
category: [学习, AI工具]
tags: [AI审计, OpenCode, Skill, 效率工具, 数据驾驶舱, 课程提炼]
status: evergreen
created: 2026-08-02
updated: 2026-08-02
---

# 狗哥 AI 审计实战课 — 核心提炼

> 来源：course.auditdog.cn《一个人+AI=财务审计团队》，共 53 节课。
> 核心理念：按审计工作流走，不先学概念，直接动手。

---

## 一、上手三件套（第1-6课）

### 工具链
- **OpenCode Desktop** — AI Agent 主战场，免费模型（MIMO 2.5、DeepSeek V4 Flash Free）即可
- Plan 模式（先想清楚再动手）vs Build 模式（直接干）
- 几分钟做出第一个 Excel 合并工具 → 直接打包成 exe

### Skill 体系
- Skill = 给 AI 用的"程序表"，把操作流程固化为可复用模块
- `find-skills` — 一句话搜索 4 个社区（SkillHub、LobeHub、skills.sh、腾讯SkillHub）
- `Skill Creator` — Anthropic 官方出品，把任何流程自动化为 Skill

---

## 二、文档处理（第7-8课）

| 能力 | 工具 |
|------|------|
| PDF 解析 | MinerU Skill（66K Stars），Flash 模式 vs 精准模式 |
| 发票识别 | 批量识别 → 导出 Excel |
| 合同提取 | 关键字段提取 + AI 风险审查 |

---

## 三、知识积累与记忆（第14-17课）

### 蒸馏任何人
- 女娲 Skill：把陈版主/田大的审计思维蒸馏成可复用 Skill
- 两个 Skill 整合：先查历史问答 → 再查准则 → 综合判断

### AI 记忆系统
- `CLAUDE.md` / `AGENTS.md` — 三级加载体系
- 写好记忆文件的 5 个原则
- IMA 知识库 MCP 连接 — 直接调用你的 IMA 资料

---

## 四、提问方法论（第19课）

### 提问四要素
1. 背景：我在做什么
2. 目标：我想要什么结果
3. 约束：有什么限制条件
4. 格式：输出成什么形式

### 准确率黄金法则
- AI"越跑越不准" → 上下文太长 → `/compact` 压缩
- 长对话超过 20 轮 → 开新会话

---

## 五、审计实战技能（第31-35、38-42课）

### 核心 Skill 清单

| Skill | 功能 |
|-------|------|
| 法规查询 Skill | 双数据源兜底，抓包固化为脚本 |
| 工商信息查询 Skill | 登录用浏览器 + 查询用代码，cookie 复用 |
| 关联方识别 Skill | 八个核查维度，真实案例循环验证 |
| 审计报告复核 Skill | 三层架构：AI 做语义 + 代码做算术 → Excel+Markdown 报告 |
| 审计底稿生成 Skill | 一条指令生成全套底稿，需原子化拆分 |
| 审计底稿复核 Skill | 四步框架：通用检查 + 类型专属检查 |

### Office 自动化

| 场景 | 方案 |
|------|------|
| Excel | Pandas+OpenPyXL（数据处理）/ Xlwings（格式保留）/ Win32com（完全控制） |
| Word | python-docx（内容编辑）/ XML工具链（批量操作）/ win32com |
| PPT | HTML 路线（演示炸裂）/ PPT 路线（能交差能改） |
| 流程图 | Flow Chart Generator Skill → draw.io 替代 Visio |

---

## 六、数据驾驶舱（第26-28课）

### 六步核心心法
1. 先搭钢架再装修（MVP）
2. 微内核 + 插件式架构
3. 验收 MVP → 版本管理 → 逐步迭代
4. 给 AI 配眼睛（接入数据源）
5. 权限基建
6. 部署上线：SSH 交给 AI → Docker → 域名+HTTPS

---

## 七、备考与学习（第29课）

### Pass All Exams 六步法
1. 建档（知识结构）→ 2. 拆解（知识颗粒）→ 3. 讲授（费曼学习法）
4. 出题（AI 生成题目）→ 5. 错题（针对性复习）→ 6. 间隔复习（艾宾浩斯）

---

## 八、数据安全（第53课）

三条私有化路线：纯本地 → 本地模型+云端API → 纯云端
五维度评分：数据敏感度/模型能力/使用频率/技术能力/预算
底线：客户数据不出境，审计底稿不上传公开 API

---

## 关联
- [[8-系统/学习资源索引]] — 茶瓜子 CPAHelper 插件
- [[8-系统/_system-prompt]] — CLAUDE.md 记忆体系
