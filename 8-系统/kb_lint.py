# -*- coding: utf-8 -*-
"""审迹知识库 lint v3（终版）：全目录扫描，支持路径式/文件名式/附件链接"""
import os, re, collections

VAULT = r"D:\AI学习\审迹知识库"
SKIP = {".obsidian", ".git", ".smart-env", ".trash", "copilot", "Excalidraw", "7-归档"}

files = {}                                   # rel(无扩展,正斜杠) → 绝对路径
by_basename = collections.defaultdict(list)  # basename(无扩展) → [rel]

for root, dirs, fnames in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
    for fn in fnames:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, VAULT).replace("\\", "/")
        stem = rel.rsplit(".", 1)[0] if "." in fn else rel
        files[stem] = p
        by_basename[os.path.basename(stem)].append(stem)

link_re = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

def resolve(t):
    t = t.strip().lstrip("/")
    for c in (t, t.rsplit(".", 1)[0] if "." in t.split("/")[-1] else t):
        if c in files:
            return c
    base = os.path.basename(t)
    if base in by_basename:
        return by_basename[base][0]
    bs = base.rsplit(".", 1)[0] if "." in base else base
    if bs in by_basename:
        return by_basename[bs][0]
    return None

incount = collections.Counter()
dead = collections.defaultdict(list)
out_stat = {}

for rel, p in files.items():
    if not rel.endswith(".md") and ".md" not in rel:
        pass
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        if not p.endswith(".md"):
            continue
        txt = ""
    # 代码块与行内代码中的 [[...]] 是示范文本，不算链接
    # 顺序：围栏代码块 → 双反引号 → 单反引号（勿颠倒，否则双反引号被拆坏）
    txt = re.sub(r"```[\s\S]*?```", "", txt)
    txt = re.sub(r"``[^`\n]*``", "", txt)
    txt = re.sub(r"`[^`\n]*`", "", txt)
    targets = {m.group(1).strip() for m in link_re.finditer(txt)}
    ok = 0
    for t in targets:
        if not t:
            continue
        r = resolve(t)
        if r is None:
            # 4-模板/ 用 [[XX行业-...]] 等占位符是模板设计使然，不计死链
            if not rel.startswith("4-模板/"):
                dead[t].append(rel)
        else:
            ok += 1
            if r != rel:
                incount[r] += 1
    if rel.endswith(".md"):
        out_stat[rel] = ok

print("=" * 14, "真死链（按目标聚合，全目录扫描）", "=" * 14)
tot = 0
for t, srcs in sorted(dead.items(), key=lambda x: -len(x[1])):
    tot += len(srcs)
    print(f"[[{t}]]  被 {len(srcs)} 处引用")
    for s in srcs:
        print(f"      ← {s}")
print(f"\n合计死链引用次数：{tot}，不同目标：{len(dead)}")

print()
print("=" * 14, "wiki 层孤儿（2-知识库，入链<2，排除 Dataview index 覆盖目录）", "=" * 14)
DATAVIEW_COVERED = ("行业研究/行业审计要点", "行业研究/行业对照", "行业研究/审计指南", "会计准则/准则原文库", "企业财务规范")
orph = []
for rel in files:
    if not rel.startswith("2-知识库/"):
        continue
    if os.path.basename(rel) in ("index", "README"):
        continue
    if any(d in rel for d in DATAVIEW_COVERED):
        continue
    if incount[rel] < 2:
        orph.append((incount[rel], rel))
for c, rel in sorted(orph):
    print(f"  入链={c}  {rel}")
print(f"\n孤儿合计：{len(orph)}")
