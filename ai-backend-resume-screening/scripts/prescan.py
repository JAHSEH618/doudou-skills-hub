#!/usr/bin/env python3
"""简历目录预扫（筛选流程第 0 步的确定化实现）。

只做机械活：枚举文件、提取文本、把「批注」与「正文」分开、跑关键词普查、
抽身份键、查 checked.md 去重。**不做任何判定**——档位、分数、淘汰与否
一律由模型按 references/screening-criteria.md 读原文得出。

用法:
    python3 prescan.py <简历目录> [--checked <checked.md 路径>] [--out <输出文件>]

默认 checked.md 位置：<简历目录>/../checked.md，找不到则试 <简历目录>/checked.md。
提取到 0 字符的文件会在「⚠️ 提取失败」区块单独列出——不要静默跳过它们。
"""

import argparse
import os
import re
import subprocess
import sys

# ---------- 关键词普查分组（命中即摘录原句上下文，供模型回原文核对） ----------
KEYWORD_GROUPS = [
    ("门槛①工具", r"Cursor|Claude\s?Code|Codex|Copilot|Windsurf|Trae|CodeBuddy|Qoder|Comet|Augment|Cline|Aider|通义灵码|豆包|Kimi|文心一言|ChatGPT"),
    ("门槛②规格/测试", r"SDD|TDD|测试驱动|规格驱动|测试先行|先写测试|OpenSpec|spec-?kit|Superpower|Kiro|验收标准|红绿重构"),
    ("AI占比", r"占比|百分之|\d{2,3}\s?%\s?(的)?(代码|编码|开发)|代码.{0,4}\d{2,3}\s?%"),
    ("Agent落地", r"Agent|智能体|LangChain|LangGraph|Dify|Coze|AutoGen|CrewAI|MCP|Function\s?Calling|RAG|多智能体"),
    ("C档危险信号", r"半成品|没有完全|不完全|了解过|尝试过|用得不多|还停留|系统设计文档|详细设计文档|开发完.{0,6}测试|补.{0,2}单测|先做.{0,4}原型"),
    ("硬门槛线索", r"年龄[:：]\s*\d+|\d+\s*年工作经验|专科|大专|专升本|本科|硕士|跨境|海关|多币种|保税"),
]

SUPP_EXT = {".xlsx", ".xls", ".docx", ".csv", ".md", ".txt"}
PHONE = re.compile(r"1[3-9]\d{9}")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


# ---------------------------- 文本提取 ----------------------------

def extract_pdf(path):
    """返回 (正文, [批注原文], 提取方式)。批注与正文必须分开——证据来源字段靠它。"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        out = subprocess.run(["pdftotext", "-layout", path, "-"],
                             capture_output=True).stdout.decode("utf-8", "ignore")
        return out, [], "pdftotext(无 PyMuPDF，批注无法单独分离)"

    doc = fitz.open(path)
    body = "".join(p.get_text() for p in doc)
    annots = []
    for page in doc:
        for a in (page.annots() or []):
            content = (a.info.get("content") or "").strip()
            if content:
                annots.append(content)
    return body, annots, "PyMuPDF"


def extract_supp(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".xlsx", ".xls"):
            import openpyxl
            wb = openpyxl.load_workbook(path, data_only=True)
            cells = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    vals = [str(c).strip() for c in row if c is not None and str(c).strip()]
                    if vals:
                        cells.append(" | ".join(vals))
            return "\n".join(cells)
        if ext == ".docx":
            import zipfile
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "ignore")
            xml = re.sub(r"</w:p>", "\n", xml)
            return re.sub(r"<[^>]+>", "", xml)
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:  # 读不出就说读不出，别装作空文件
        return f"__EXTRACT_ERROR__: {type(e).__name__}: {e}"


# ---------------------------- 字段抽取 ----------------------------

def identity_key(text):
    """身份键：手机后 4 位优先，缺则邮箱前缀。两者皆缺返回 None。"""
    m = PHONE.search(text)
    if m:
        return m.group()[-4:], f"手机…{m.group()[-4:]}"
    m = EMAIL.search(text)
    if m:
        prefix = m.group().split("@")[0]
        return prefix, f"邮箱 {prefix}@…"
    return None, "缺失"


def guess_name(filename, body):
    """姓名：正文开头的中文串优先，回落到文件名。两个都给，由模型定夺。"""
    # 噪声词按「包含」匹配：文件名里的「年应届生」「工作经验」都会被滤掉
    noise = ("开发", "长沙", "南京", "深圳", "北京", "上海", "杭州", "广州", "武汉",
             "郑州", "成都", "应届", "经验", "后端", "前端", "工程师", "简历",
             "个人", "求职", "应聘", "信息", "补充", "你好", "基本", "年限", "岗位")

    def clean(c):
        return c and not any(w in c for w in noise)

    stem = os.path.splitext(os.path.basename(filename))[0]
    stem = re.sub(r"【[^】]*】", "", stem)
    from_file = next((c for c in reversed(re.findall(r"[一-龥]{2,4}", stem)) if clean(c)), None)

    # 文件名解析出的姓名若在正文出现，即互证；否则退回正文开头第一个非噪声中文串
    from_body = None
    if from_file and from_file in body:
        from_body = from_file
    else:
        for m in re.finditer(r"([一-龥]{2,4})(?![一-龥])", body[:120]):
            if clean(m.group(1)):
                from_body = m.group(1)
                break
    return from_body, from_file


def keyword_census(text, label):
    """命中即摘录原句上下文，方便模型直接回原文核对，不必再翻一遍。"""
    rows = []
    for name, pat in KEYWORD_GROUPS:
        hits = list(re.finditer(pat, text, re.I))
        if not hits:
            rows.append((name, 0, []))
            continue
        # 同一句话里的多次命中只摘一次：命中点相距 <60 字视为同一处
        snippets, taken = [], []
        for h in hits:
            if any(abs(h.start() - t) < 60 for t in taken):
                continue
            taken.append(h.start())
            snippets.append(text[max(0, h.start() - 28): h.end() + 44].replace("\n", "·").strip())
            if len(snippets) >= 5:
                break
        rows.append((name, len(hits), snippets))
    return rows


# ---------------------------- checked.md 查重 ----------------------------

def load_checked(path):
    if not path or not os.path.exists(path):
        return None, []
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|") or line.startswith("|---") or "筛选日期" in line:
                continue
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) < 7:
                continue
            blob = line
            tier = None
            mt = re.search(r"\[G2:([ABC])\]", blob)
            if mt:
                tier = mt.group(1)
            mid = re.search(r"\[ID:([\w.+-]+)\]", blob)
            rows.append({
                "date": cols[0], "file": cols[1], "name": cols[2], "city": cols[3],
                "score": cols[4], "grade": cols[5], "verdict": cols[6],
                "tier": tier, "id": mid.group(1) if mid else None,
            })
    return path, rows


def dedup_lookup(rows, basename, relpath, name_body, name_file, idkey):
    """返回 (状态, 全部相关历史行)。

    关键：文件名精确命中**不得**提前返回。同一个人在别的批次以别的文件名投过、
    且判定不同，正是跨批次一致性协议要抓的场景——短路就永远看不见。
    """
    if not rows:
        return "新筛（无 checked.md 记录）", []

    exact = [r for r in rows if basename in r["file"] or relpath in r["file"]]
    names = {n for n in (name_body, name_file) if n}
    by_name = [r for r in rows if r["name"] in names] if names else []
    by_id = [r for r in rows if idkey and r["id"] == idkey]

    hits = list({id(r): r for r in exact + by_name + by_id}.values())
    hits.sort(key=lambda r: r["date"])

    if not hits:
        return "新筛", []
    extra = len(hits) - len(exact)
    if exact:
        status = "已筛过（来源文件精确命中）→ 跳过"
        if extra:
            status += f"；另有 {extra} 条同人历史记录，须一并对账"
        return status, hits
    if by_id:
        return "身份键命中同一人 → 按跨批次一致性协议处理", hits
    return "姓名命中，身份键未确认 → 须核对是否同一人", hits


# ---------------------------- 主流程 ----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory")
    ap.add_argument("--checked", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.directory)
    if not os.path.isdir(root):
        sys.exit(f"不是目录: {root}")

    checked_path = args.checked
    if not checked_path:
        for cand in (os.path.join(os.path.dirname(root), "checked.md"),
                     os.path.join(root, "checked.md")):
            if os.path.exists(cand):
                checked_path = cand
                break
    checked_path, checked_rows = load_checked(checked_path)

    pdfs, supps, others = [], [], []
    for dirpath, _, filenames in os.walk(root):
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            full = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext == ".pdf":
                pdfs.append(full)
            elif ext in SUPP_EXT:
                supps.append(full)
            else:
                others.append(full)

    L = []
    w = L.append
    w(f"# 预扫报告 · {root}")
    w("")
    w(f"PDF {len(pdfs)} 份 · 补充材料 {len(supps)} 份 · 其他 {len(others)} 份 · "
      f"checked.md: {checked_path or '未找到（全部按新筛处理）'}"
      + (f"（{len(checked_rows)} 条记录）" if checked_rows else ""))
    w("")
    w("> 本报告只做提取与查重，**不含任何判定**。档位 / 分数 / 淘汰一律回读原文按 criteria 判。")
    w("")

    supp_texts = {s: extract_supp(s) for s in supps}

    if supps:
        w("## 目录级补充材料（门槛②定档的主要依据，务必读完）")
        w("")
        for s in supps:
            w(f"### {os.path.relpath(s, root)}")
            text = supp_texts[s]
            if text.startswith("__EXTRACT_ERROR__"):
                w(f"⚠️ {text}")
            elif not text.strip():
                w("⚠️ 提取到 0 字符——请手工打开确认，不要当作「无补充材料」")
            else:
                w("```")
                w(text.strip()[:6000])
                w("```")
            w("")

    if others:
        w("## 其他文件（未提取，自行确认是否含证据）")
        w("")
        for o in others:
            w(f"- {os.path.relpath(o, root)}")
        w("")

    failures = []
    w("## 逐份简历")
    w("")
    for p in pdfs:
        rel = os.path.relpath(p, root)
        base = os.path.basename(p)
        try:
            body, annots, how = extract_pdf(p)
        except Exception as e:
            failures.append((rel, f"{type(e).__name__}: {e}"))
            continue
        if not body.strip() and not annots:
            failures.append((rel, "提取到 0 字符"))
            continue

        ann_text = "\n".join(annots)
        idkey, id_disp = identity_key(body + "\n" + ann_text)
        name_body, name_file = guess_name(p, body)

        # 证据来源：门槛①② 的证据落在哪一层
        gate_pat = KEYWORD_GROUPS[0][1] + "|" + KEYWORD_GROUPS[1][1]
        src = []
        if re.search(gate_pat, body, re.I):
            src.append("正文")
        if re.search(gate_pat, ann_text, re.I):
            src.append("批注")
        if any(re.search(gate_pat, t, re.I) for t in supp_texts.values()):
            src.append("补充表(目录级)")
        src_disp = " + ".join(src) if src else "无"

        status, hits = dedup_lookup(checked_rows, base, rel, name_body, name_file, idkey)

        w(f"### {rel}")
        w("")
        w(f"- 姓名：正文『{name_body or '—'}』 / 文件名『{name_file or '—'}』")
        w(f"- 身份键：{id_disp}" + ("　⚠️ 无手机无邮箱，须人工确认是否同一人" if not idkey else ""))
        w(f"- 提取：{how} · 正文 {len(body)} 字 · 批注 {len(annots)} 条")
        w(f"- **证据来源：{src_disp}**" + ("　⚠️ 门槛①②零证据来源" if src_disp == "无" else ""))
        w(f"- **查重：{status}**")
        for h in hits:
            tier = f"[G2:{h['tier']}]" if h["tier"] else "档位未标"
            # token 已单独成列，从结论正文里去掉免得重复
            verdict = re.sub(r"\[(G2|ID):[^\]]*\]\s*", "", h["verdict"])
            w(f"    - {h['date']} · {h['score']} 分 · {h['grade']} · {tier} · {verdict[:110]}")
        if len(hits) > 1:
            tiers = {h["tier"] for h in hits if h["tier"]}
            scores = {h["score"] for h in hits}
            if len(tiers) > 1 or len(scores) > 1:
                w("    - ⚠️ **历史判定不一致** → 按跨批次一致性协议：缺失继承 / 冲突取最低")
        w("")

        if annots:
            w("**批注原文（候选人手写补充，门槛②定档主要依据）**")
            w("")
            for a in annots:
                w("```")
                w(a.strip()[:2500])
                w("```")
            w("")

        w("**关键词命中**")
        w("")
        for group, n, snips in keyword_census(body + "\n" + ann_text, rel):
            if n == 0:
                w(f"- {group}：0")
            else:
                w(f"- {group}：{n}")
                for s in snips:
                    w(f"    - …{s}…")
        w("")

    if failures:
        w("## ⚠️ 提取失败（不得当作「无证据」，必须手工打开）")
        w("")
        for rel, why in failures:
            w(f"- **{rel}** — {why}")
        w("")

    report = "\n".join(L)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"已写入 {args.out}（{len(report)} 字符）")
        if failures:
            print(f"⚠️ {len(failures)} 份提取失败，见报告末尾")
    else:
        print(report)


if __name__ == "__main__":
    main()
