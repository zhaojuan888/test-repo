---
type: index
created: 2026-08-02
updated: 2026-08-02
---

# 审迹知识库

> 天健审计师 · 审计 | 税务 | 尽调 | IPO
> 基于 PARA+Zettelkasten 混合体系，Dataview 自动聚合

---

##  快速入口

-  [[3-知识地图/审计程序库|审计程序库]] — 审计程序 + 方法论
-  [[3-知识地图/准则条文库|准则条文库]] — CAS 会计准则
-  [[3-知识地图/税务专题库|税务专题库]] — 税种 + 金税四期
-  [[3-知识地图/处罚案例库|处罚案例库]] — 监管处罚案例
-  [[3-知识地图/行业知识库|行业知识库]] — 行业审计风险
-  📖 [[3-知识地图/学习仪表盘|学习仪表盘]] — 每日进步 + 复习队列
-  📚 [[8-系统/学习资源索引|学习资源]] — 政策法规库 + 公众号

---

## 当前活跃项目

```dataview
TABLE status AS "状态", deadline AS "截止日期", tags AS "标签"
FROM "1-项目"
WHERE type = "project" AND status != "archived"
SORT deadline ASC
```

---

## 最近更新的知识笔记

```dataview
TABLE type AS "类型", category AS "分类", file.mtime AS "最后更新"
FROM "2-知识库"
SORT file.mtime DESC
LIMIT 10
```

---

## 待处理收件箱

```dataview
LIST
FROM "0-收件箱"
SORT file.ctime DESC
LIMIT 5
```

---

## 需要复习

```dataview
LIST
FROM "2-知识库"
WHERE status = "review-needed"
SORT file.mtime ASC
LIMIT 7
```
