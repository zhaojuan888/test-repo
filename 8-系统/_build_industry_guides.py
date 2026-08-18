# -*- coding: utf-8 -*-
"""
批量把「行业审计指南XX.pdf」入库为 Obsidian 笔记。
- 复制 PDF -> 5-参考资料/行业审计指南/
- 全文提取 -> 5-参考资料/行业审计指南/XX.md（可搜索语料）
- 生成导航索引 -> 2-知识库/行业研究/审计指南/XX.md（章节标题 + [[PDF#page=N]] 跳转）
仅处理带文本层的 PDF（公开行业指南，非客户数据）。
"""
import os, re, shutil, datetime

VAULT = "D:/AI学习/审迹知识库"
SRC = "D:/学习/0-行业审计学习参考"
REF_DIR = os.path.join(VAULT, "5-参考资料", "行业审计指南")
IDX_DIR = os.path.join(VAULT, "2-知识库", "行业研究", "审计指南")

# 章节标题识别（中文审计指南常见层级）
HEAD_PATTERNS = [
    r'^第[一二三四五六七八九十百千零\d]+\s*[章节目节篇]',      # 第一章 / 第一节
    r'^[一二三四五六七八九十百千]+\s*[、.]',                  # 一、 一.
    r'^（[一二三四五六七八九十]+\）',                          # （一）
    r'^\d+[.、]',                                             # 1. 1、 1.1
]
HEAD_RE = [re.compile(p) for p in HEAD_PATTERNS]

def _cjk(s):
    return sum(1 for c in s if '\u4e00' <= c <= '\u9fff')

def _digit_ratio(s):
    if not s:
        return 0
    return sum(1 for c in s if c.isdigit()) / len(s)

def is_heading(line):
    s = line.strip()
    if not s or len(s) > 40:
        return False
    if s[-1] in '。，、；：,.;:）)':
        return False
    if re.match(r'^\d{4}\s', s):          # 拒绝「2014 年」类年份开头正文
        return False
    if _digit_ratio(s) > 0.35:            # 拒绝数据行
        return False
    for r in HEAD_RE:
        m = r.match(s)
        if m:
            rest = s[m.end():]
            return _cjk(rest) >= 2         # 前缀后须有 ≥2 汉字，排除「4 月份」类
    return False

def clean_text(t):
    # 轻量化：去分页符、折叠多余空行
    t = t.replace('\x0c', '\n')
    lines = [ln.rstrip() for ln in t.split('\n')]
    out, blank = [], False
    for ln in lines:
        if ln == '':
            if not blank:
                out.append('')
                blank = True
        else:
            out.append(ln)
            blank = False
    return '\n'.join(out).strip() + '\n'

def process_one(pdf_path):
    from pypdf import PdfReader
    fn = os.path.basename(pdf_path)
    stem = fn[:-4]
    reader = PdfReader(pdf_path)
    n_pages = len(reader.pages)

    # 复制 PDF 到参考资料
    os.makedirs(REF_DIR, exist_ok=True)
    shutil.copy2(pdf_path, os.path.join(REF_DIR, fn))

    # 全文 + 章节
    full_parts = []
    toc = []  # (level_hint, text, page)
    for i, page in enumerate(reader.pages, 1):
        txt = page.extract_text() or ''
        full_parts.append(f"\n\n<!-- 第 {i} 页 -->\n\n" + txt)
        for ln in txt.split('\n'):
            ln = ln.strip()
            if is_heading(ln):
                # 估算层级：章>节>一、>（一）>数字
                lvl = 3
                if re.match(r'^第.+[章篇]', ln): lvl = 0
                elif re.match(r'^第.+[节目节]', ln): lvl = 1
                elif re.match(r'^[一二三四五六七八九十]+[、.]', ln): lvl = 1
                elif re.match(r'^（[一二三四五六七八九十]+）', ln): lvl = 2
                toc.append((lvl, ln, i))

    # 写全文语料
    today = datetime.date.today().isoformat()
    ref_md = f"""---
type: 参考资料
tags:
  - 行业审计指南
  - 审计程序
  - 参考资料
source: "{fn}"
pages: {n_pages}
created: {today}
status: 全文入库
converted_by: pypdf（文本层直提）
---

# {stem}

> 来源文件：`{fn}`（共 {n_pages} 页）。本文件为全文提取，供 Obsidian 全文检索与精读。
> 章节导航见：`[[2-知识库/行业研究/审计指南/{stem}]]`

"""
    ref_md += clean_text('\n'.join(full_parts))
    with open(os.path.join(REF_DIR, stem + '.md'), 'w', encoding='utf-8') as f:
        f.write(ref_md)

    # 写导航索引
    os.makedirs(IDX_DIR, exist_ok=True)
    lines = []
    lines.append(f"---\ntype: 行业审计指南\ntags:\n  - 行业审计指南\n  - 审计程序\nsource: \"{fn}\"\npages: {n_pages}\ncreated: {today}\nstatus: 导航索引\n---\n")
    lines.append(f"# {stem}（审计指南导航）\n")
    lines.append(f"> 来源 PDF：`[[5-参考资料/行业审计指南/{fn}]]`（共 {n_pages} 页）\n")
    lines.append(f"> 全文语料：`[[5-参考资料/行业审计指南/{stem}]]`\n")
    lines.append("\n## 章节导航\n")
    # 去重连续重复标题
    seen = set()
    last = None
    for lvl, text, pg in toc:
        if text == last:
            continue
        last = text
        indent = '  ' * lvl
        link = f"[[5-参考资料/行业审计指南/{fn}#page={pg}|{text}]]"
        lines.append(f"{indent}- {link}  ")
    idx_md = '\n'.join(lines) + '\n'
    with open(os.path.join(IDX_DIR, stem + '.md'), 'w', encoding='utf-8') as f:
        f.write(idx_md)

    return stem, n_pages, len(toc)

if __name__ == '__main__':
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.pdf') and '行业审计指南' in f)
    # 跳过重复的 09 传媒发行业（保留 传媒出版业）
    files = [f for f in files if not ('09出版发行业（传媒发行业）' in f)]
    print(f"待处理：{len(files)} 份")
    ok, fail = 0, 0
    for f in files:
        try:
            stem, n, t = process_one(os.path.join(SRC, f))
            print(f"  [OK] {stem}  页={n} 章节={t}")
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {f}: {e}")
            fail += 1
    print(f"完成：成功 {ok}，失败 {fail}")
