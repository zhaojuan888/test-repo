# 准则原文库

> 依据陈版主（陈奕蔚）会计准则实务专家技能内置动态准则库同步，来源 docs.maoyanqing.com。
> 更新时间：2026-08-17

## 结构
- `cas/` — 企业会计准则原文（31 个）
- `casi/` — 企业会计准则解释（20 个）
- `rlc/` — 上市公司监管指引（6 个）

## 更新方式
```bash
# 在技能目录运行（需 requests/bs4/markdownify）
python fetch_standards.py --update   # 更新已缓存准则
# 再运行同步脚本复制到本目录
```
