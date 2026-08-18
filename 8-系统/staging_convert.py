#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
staging_convert.py —— 审迹知识库「0-收件箱」自动转换脚本（本地优先 / 敏感不出域）

功能：
  监控 0-收件箱（或任意源目录），把丢进去的 Word/Excel/CSV/PDF/图片/Markdown
  自动转成 Obsidian 可用的 .md 半成品，前端 frontmatter 对齐本库约定，
  你只需做归类与质量把关。

设计原则（极简）：
  - 全程本地，绝不上传任何文件到公网（审计资料红线）。
  - 带文本层 PDF / docx / xlsx / csv / txt / md 直接本地转。
  - 扫描件 / 图片标记为「需本地 OCR」，写入 _needs_ocr.txt，由你用本地
    MinerU 技能处理，脚本不代发云端。
  - 文件名含敏感关键词（底稿/客户/函证…）强制标注 sensitive，提醒勿出域。

用法：
  python staging_convert.py --once          # 扫一次
  python staging_convert.py --watch         # 持续监听（Ctrl+C 退出）
  python staging_convert.py --src D:/inbox --out D:/out
依赖：pypdf python-docx openpyxl watchdog（已装于 managed venv）
"""
import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import date

# ---------- 配置 ----------
VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 知识库根
STAGING = os.path.join(VAULT, "0-收件箱")
MANIFEST = os.path.join(STAGING, "_manifest.json")
OCR_QUEUE = os.path.join(STAGING, "_needs_ocr.txt")
SENSITIVE_KW = ["底稿", "客户", "函证", "回函", "被审计", "机密",
                "confidential", "涉密", "敏感"]
TEXT_EXT = {".md", ".txt"}
DOCX_EXT = {".docx"}
XLSX_EXT = {".xlsx", ".xls"}
CSV_EXT = {".csv"}
PDF_EXT = {".pdf"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
SKIP_FILES = {"_manifest.json", "_needs_ocr.txt"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_sensitive(name):
    low = name.lower()
    return any(k.lower() in low for k in SENSITIVE_KW)


def frontmatter(meta):
    import json
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def docx_to_md(path):
    from docx import Document
    from docx.document import Document as _Doc
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    doc = Document(path)
    out = []

    def iter_blocks(parent):
        elm = parent.element.body if isinstance(parent, _Doc) else parent.element
        for child in elm.iterchildren():
            if isinstance(child, CT_P):
                yield ("p", Paragraph(child, doc))
            elif isinstance(child, CT_Tbl):
                yield ("t", Table(child, doc))

    def style_level(p):
        # 近似映射：Heading 1..3 -> #..###；其余正文
        sid = (p.style.style_id if p.style else "") or ""
        low = sid.lower()
        for i in range(1, 4):
            if f"heading {i}" in low or f"heading{i}" in low:
                return i
        return 0

    for kind, blk in iter_blocks(doc):
        if kind == "p":
            txt = blk.text.strip()
            if not txt:
                continue
            lvl = style_level(blk)
            out.append(("#" * lvl + " " + txt) if lvl else txt)
        else:
            rows = [[c.text.strip() for c in r.cells] for r in blk.rows]
            if rows:
                out.append(table_to_md(rows))
    return "\n\n".join(out)


def table_to_md(rows, cap=60):
    head, *body = rows
    body = body[:cap]
    md = ["| " + " | ".join(head) + " |",
          "| " + " | ".join(["---"] * len(head)) + " |"]
    for r in body:
        md.append("| " + " | ".join(r) + " |")
    if len(rows) - 1 > cap:
        md.append(f"\n> ⚠️ 表格过大，仅截取前 {cap} 行，完整内容见原文件。")
    return "\n".join(md)


def xlsx_to_md(path, cap=200):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f"## 工作表：{ws.title}")
        rows = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= cap:
                break
            rows.append(["" if c is None else str(c) for c in row])
        if rows:
            out.append(table_to_md(rows, cap=cap))
    return "\n\n".join(out)


def csv_to_md(path, cap=200):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        rows = list(csv.reader(f))[:cap]
    if rows:
        return table_to_md(rows, cap=cap)
    return ""


def pdf_to_md(path):
    from pypdf import PdfReader
    reader = PdfReader(path)
    # 判断是否带文本层
    sample = ""
    for p in reader.pages[:3]:
        sample += (p.extract_text() or "")
    if len(sample.strip()) < 50:
        return None  # 扫描件，需 OCR
    out = [f"> 共 {len(reader.pages)} 页，带文本层自动提取。\n"]
    # 书签目录
    try:
        outlines = reader.outline
        if outlines:
            out.append("## 目录（书签）")
            out.append(outline_to_md(outlines))
            out.append("")
    except Exception:
        pass
    out.append("## 正文")
    for i, p in enumerate(reader.pages, 1):
        txt = p.extract_text() or ""
        if txt.strip():
            out.append(f"\n<!-- page {i} -->\n\n" + txt.strip())
    return "\n".join(out)


def outline_to_md(items, depth=0):
    lines = []
    for it in items:
        if isinstance(it, list):
            lines.append(outline_to_md(it, depth + 1))
        else:
            title = getattr(it, "title", "") or ""
            lines.append(f'{"  " * depth}- {title}')
    return "\n".join(lines)


def convert(path, out_dir):
    """返回 (md_text, needs_ocr:bool) 或 None 表示跳过"""
    ext = os.path.splitext(path)[1].lower()
    name = os.path.splitext(os.path.basename(path))[0]
    sensitive = is_sensitive(os.path.basename(path))
    base_meta = {
        "type": "资料-待分类",
        "tags": ["staging", "待归类"],
        "source": os.path.relpath(path, VAULT),
        "created": str(date.today()),
        "converter": "staging_convert.py",
        "status": "待归类",
    }
    if sensitive:
        base_meta["sensitive"] = "true  ⚠️敏感文件，禁止上传公网/云端OCR，仅本地处理"

    if ext in TEXT_EXT:
        # md/txt：生成嵌入引用笔记，保留原文件
        body = f"> 原始文件：{os.path.basename(path)}\n\n![[{os.path.basename(path)}]]\n"
        md = frontmatter(base_meta) + body
        return md, False

    if ext in DOCX_EXT:
        md = frontmatter(base_meta) + "# " + name + "\n\n" + docx_to_md(path)
        return md, False

    if ext in XLSX_EXT:
        md = frontmatter(base_meta) + "# " + name + "\n\n" + xlsx_to_md(path)
        return md, False

    if ext in CSV_EXT:
        md = frontmatter(base_meta) + "# " + name + "\n\n" + csv_to_md(path)
        return md, False

    if ext in PDF_EXT:
        res = pdf_to_md(path)
        if res is None:
            return None, True  # 需 OCR
        md = frontmatter(base_meta) + "# " + name + "\n\n" + res
        return md, False

    if ext in IMG_EXT:
        return None, True  # 图片需 OCR

    return None, False  # 不支持的类型，跳过


def load_manifest():
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_manifest(m):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)


def scan_once():
    manifest = load_manifest()
    ocr_queue = set()
    processed = 0
    out_dir = os.path.join(STAGING, "_out")
    os.makedirs(out_dir, exist_ok=True)
    for fn in sorted(os.listdir(STAGING)):
        fp = os.path.join(STAGING, fn)
        if not os.path.isfile(fp) or fn in SKIP_FILES:
            continue
        ext = os.path.splitext(fn)[1].lower()
        if ext not in (TEXT_EXT | DOCX_EXT | XLSX_EXT | CSV_EXT | PDF_EXT | IMG_EXT):
            continue
        digest = sha256(fp)
        rec = manifest.get(fn)
        if rec and rec.get("sha256") == digest and os.path.exists(
                os.path.join(STAGING, rec.get("out", ""))):
            continue  # 已处理且未变化
        md, needs_ocr = convert(fp, out_dir)
        if needs_ocr:
            ocr_queue.add(fn)
            manifest[fn] = {"sha256": digest, "out": "", "status": "needs_ocr"}
            print(f"  [OCR] {fn} → 需本地 OCR，已入队")
            processed += 1
            continue
        if md is None:
            print(f"  [SKIP] {fn} 类型不支持")
            continue
        # 输出进 _out 子目录，按 stem.源扩展名.md 命名，避免同名覆盖与自处理
        stem, srcext = os.path.splitext(fn)
        out_fn = f"{stem}.{srcext.lstrip('.')}.md"
        with open(os.path.join(out_dir, out_fn), "w", encoding="utf-8") as f:
            f.write(md)
        manifest[fn] = {"sha256": digest, "out": os.path.join("_out", out_fn),
                        "status": "converted"}
        print(f"  [OK] {fn} → _out/{out_fn}")
        processed += 1
    # 写 OCR 队列
    with open(OCR_QUEUE, "w", encoding="utf-8") as f:
        f.write("# 需本地 OCR 的文件（请用本地 MinerU 技能处理，禁止上传公网）\n")
        for fn in sorted(ocr_queue):
            f.write(f"- {fn}\n")
    save_manifest(manifest)
    print(f"扫描完成，本次处理 {processed} 个文件。")


def watch_loop():
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class H(FileSystemEventHandler):
        def on_created(self, e):
            if not e.is_directory:
                print(f"检测到新文件：{os.path.basename(e.src_path)}，稍后扫描…")
                # 简单防抖：等 1s 让写入完成
                import time
                time.sleep(1)
                scan_once()

    obs = Observer()
    obs.schedule(H(), STAGING, recursive=False)
    obs.start()
    print(f"正在监听：{STAGING} （Ctrl+C 退出）")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()


def main():
    global STAGING, VAULT, MANIFEST, OCR_QUEUE
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="扫描一次后退出")
    ap.add_argument("--watch", action="store_true", help="持续监听目录")
    ap.add_argument("--src", default=STAGING, help="源目录（默认 0-收件箱）")
    args = ap.parse_args()
    STAGING = os.path.abspath(args.src)
    VAULT = os.path.dirname(os.path.dirname(STAGING)) if os.path.basename(
        os.path.dirname(STAGING)) == "0-收件箱" else os.path.dirname(STAGING)
    MANIFEST = os.path.join(STAGING, "_manifest.json")
    OCR_QUEUE = os.path.join(STAGING, "_needs_ocr.txt")
    if not os.path.isdir(STAGING):
        print(f"源目录不存在：{STAGING}")
        sys.exit(1)
    if args.watch:
        watch_loop()
    else:
        scan_once()


if __name__ == "__main__":
    main()
