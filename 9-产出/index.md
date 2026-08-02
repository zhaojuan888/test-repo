---
type: index
created: 2026-08-02
updated: 2026-08-02
---

# 9-产出

> 消化层的输出制品：研究报告、审计备忘录、正式文章、PPT、给客户的交付物。
> 对应 Karpathy 方法论中的 `outputs/` — 知识经消化后形成的公开/交付制品。

---

## 产出流程

`0-收件箱`（收集）→ `2-知识库`（消化）→ `9-产出`（输出）

## 已有产出

```dataview
TABLE type AS "类型", status AS "状态", file.mtime AS "最后更新"
FROM "9-产出"
WHERE file.name != "index"
SORT file.mtime DESC
```

## 写作规范

- 产出来自知识库中的 [[2-知识库/index|知识库]]，不凭空输出
- 每篇产出标注引用来源 `[[来源笔记]]`
- 完成后归档：仍需要的移入 `7-归档`，发布件可移出 Vault