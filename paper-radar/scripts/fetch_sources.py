#!/usr/bin/env python3
"""paper-radar 非论文信源抓取。只用 Python 标准库 + 系统 curl，输出 JSON。

两个子命令：

  scan    周扫 / 定向开始时跑一次，拉 AIHot 热点 + AIHot 关键词与账号 + HN 高分帖，
          产出资讯 / 快讯 / 实践的候选池。
          python3 fetch_sources.py scan --since 2026-09-01 --out reports/assets/2026-09-10/candidates.json
          可选：--topic "agent 记忆"（定向模式，追加到关键词）、--hn-min 100、--accounts <清单路径>

  lookup  给一篇论文 / 博客找解说：HN 讨论串 + AIHot 收录。
          python3 fetch_sources.py lookup "Post-Training Science for Supervised Fine-Tuning"
          可选：--days 90

  x       核一条 X 原帖：走公开的 oEmbed 端点拿作者与正文（exa 抓不到 x.com，这条能）。
          python3 fetch_sources.py x https://x.com/dair_ai/status/2097555607389896732 [更多链接...]

信源说明见 references/sources.md。AIHot 只有 24h / 7d 两个窗口，--since 早于 7 天时
AIHot 只盖后 7 天，输出里的 notes 会写明，报告开头要照抄声明。
HTTP 走 curl 而不是 urllib：这台机器的 python.org Python 没带 CA 证书，urllib 打 https 会挂。
"""

import argparse
import json
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

AIHOT = "https://aihot.news/api/v1"
AIHOT_UA = "aihot-skill/1.6.0 (+https://aihot.news/aihot-skill/)"
HN = "https://hn.algolia.com/api/v1/search"

# 每期固定查的关键词。AIHot 用 mode=all（selected 池几乎没有基础设施内容），HN 用同一组。
KEYWORDS = [
    "vLLM", "SGLang", "LLM inference", "LLM serving", "KV cache",
    "GPU cluster", "Blackwell", "quantization", "FP4", "CXL",
    "agent memory", "RAG", "RL training", "post-training", "LLM evaluation",
]
DEFAULT_ACCOUNTS = Path(__file__).resolve().parent.parent / "references" / "x-accounts.txt"


def curl(url, ua=None, timeout=25):
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", "Accept: application/json"]
    if ua:
        cmd += ["-A", ua]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed ({r.returncode}): {r.stderr.strip()[:200]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"non-JSON response from {url[:80]}: {r.stdout[:120]!r}")


# ---------------------------------------------------------------- AIHot

def aihot_items(q=None, mode="all", window="7d", limit=20, category=None):
    params = {"mode": mode, "window": window, "limit": limit}
    if q:
        params["q"] = q
    if category:
        params["category"] = category
    d = curl(f"{AIHOT}/items?{urlencode(params)}", ua=AIHOT_UA)
    out = []
    for it in d.get("items", []):
        out.append({
            "title": it.get("title"),
            "original_title": it.get("originalTitle"),
            "summary": it.get("summary"),
            "source": it["source"]["name"],
            "category": it.get("category"),
            "published_at": it.get("publishedAt"),
            "discovered_at": it.get("discoveredAt"),
            "url": it["links"]["original"],
            "aihot_url": it["links"]["aihot"],
            "reason": it.get("reason"),
        })
    return out


def aihot_hot_topics():
    d = curl(f"{AIHOT}/hot-topics", ua=AIHOT_UA)
    out = []
    for it in d.get("items", []):
        out.append({
            "rank": it.get("rank"),
            "title": it.get("title"),
            "source_count": it.get("sourceCount"),
            "source_names": it.get("sourceNames"),
            "latest_at": it.get("latestAt"),
            "story_url": (it.get("links") or {}).get("story"),
        })
    return out


# ---------------------------------------------------------------- HN

def hn_search(query, since_ts, hits=10):
    params = {"query": query, "tags": "story",
              "numericFilters": f"created_at_i>{since_ts}", "hitsPerPage": hits}
    d = curl(f"{HN}?{urlencode(params)}")
    out = []
    for h in d.get("hits", []):
        out.append({
            "title": h.get("title"),
            "url": h.get("url"),
            "points": h.get("points") or 0,
            "comments": h.get("num_comments") or 0,
            "created_at": h.get("created_at"),
            "hn_url": f"https://news.ycombinator.com/item?id={h['objectID']}",
        })
    return out


def hn_relevant(kw, hit):
    """Algolia 的 query 是全文模糊匹配，会把「GPU cluster」匹配到毫不相干的帖子。
    这里要求关键词的每个词都出现在标题或链接里。"""
    hay = f"{hit.get('title') or ''} {hit.get('url') or ''}".lower()
    words = [w for w in kw.lower().split() if len(w) > 1]
    return all(w in hay for w in words)


# ---------------------------------------------------------------- 账号清单

def load_accounts(path):
    """返回 [(group, must, [handles])]。`## 组名` 起一组，组名末尾 ! 表示每期必搜；
    `# ...` 是注释；`@handle` 归当前组。"""
    groups, cur = [], None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("##"):
            name = line[2:].strip()
            cur = (name.rstrip("!").strip(), name.endswith("!"), [])
            groups.append(cur)
        elif line.startswith("@") and cur is not None:
            cur[2].append(line[1:])
    return groups


# ---------------------------------------------------------------- scan

def cmd_scan(args):
    since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    since_ts = int(since.timestamp())
    now = datetime.now(timezone.utc)
    notes = []
    if (now - since).days > 7:
        notes.append(f"AIHot 只有 7 天窗口：{args.since} → {now:%Y-%m-%d} 共 {(now - since).days} 天，"
                     f"AIHot 只盖后 7 天，更早的资讯 / 快讯靠 HN 与 exa。报告开头要声明。")

    result = {"since": args.since, "generated_at": now.isoformat(timespec="seconds"),
              "notes": notes, "aihot_hot_topics": [], "aihot_items": [],
              "x_by_account": {}, "hn": [], "errors": []}

    def guard(label, fn, *a, **kw):
        try:
            return fn(*a, **kw)
        except RuntimeError as e:
            result["errors"].append(f"{label}: {e}")
            return None

    # 1) AIHot 热点榜
    hot = guard("aihot hot-topics", aihot_hot_topics)
    result["aihot_hot_topics"] = hot or []

    # 2) AIHot 关键词（mode=all）
    keywords = list(KEYWORDS) + ([args.topic] if args.topic else [])
    seen = {}
    for kw in keywords:
        items = guard(f"aihot q={kw}", aihot_items, q=kw)
        time.sleep(0.3)
        for it in items or []:
            key = it["url"]
            if key in seen:
                seen[key]["matched_by"].append(kw)
            else:
                it["matched_by"] = [kw]
                seen[key] = it
    result["aihot_items"] = sorted(seen.values(), key=lambda x: x.get("published_at") or "", reverse=True)

    # 3) 必搜账号：AIHot q=<handle>，只认来源名里带 @handle 的（本人发的），其余算提及
    groups = load_accounts(args.accounts)
    for gname, must, handles in groups:
        if not must:
            continue
        for h in handles:
            items = guard(f"aihot @{h}", aihot_items, q=h, limit=15)
            time.sleep(0.3)
            own = [it for it in (items or []) if f"@{h}".lower() in it["source"].lower()]
            mentions = [it for it in (items or []) if it not in own]
            result["x_by_account"][h] = {
                "group": gname, "own_posts": own, "mention_count": len(mentions),
                "tracked_by_aihot": bool(own),
            }

    # 4) HN 高分帖
    hn_seen = {}
    for kw in keywords:
        hits = guard(f"hn {kw}", hn_search, kw, since_ts, hits=15)
        time.sleep(0.2)
        for h in hits or []:
            if h["points"] < args.hn_min or not hn_relevant(kw, h):
                continue
            key = h["hn_url"]
            if key in hn_seen:
                hn_seen[key]["matched_by"].append(kw)
            else:
                h["matched_by"] = [kw]
                hn_seen[key] = h
    result["hn"] = sorted(hn_seen.values(), key=lambda x: x["points"], reverse=True)

    out = Path(args.out) if args.out else None
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # 人读摘要
    print(f"scan since {args.since}" + (f"  topic={args.topic}" if args.topic else ""))
    for n in notes:
        print(f"  ! {n}")
    for e in result["errors"]:
        print(f"  x {e}")
    print(f"AIHot 热点 {len(result['aihot_hot_topics'])} 条：")
    for t in result["aihot_hot_topics"]:
        print(f"  #{t['rank']} {t['title']}  [{t['source_count']} 源]")
    by_kw = {}
    for it in result["aihot_items"]:
        for kw in it["matched_by"]:
            by_kw[kw] = by_kw.get(kw, 0) + 1
    print(f"AIHot 关键词命中 {len(result['aihot_items'])} 条（去重后）：" +
          ", ".join(f"{k} {v}" for k, v in sorted(by_kw.items(), key=lambda x: -x[1])))
    untracked = [h for h, v in result["x_by_account"].items() if not v["tracked_by_aihot"]]
    tracked = {h: len(v["own_posts"]) for h, v in result["x_by_account"].items() if v["tracked_by_aihot"]}
    print(f"必搜账号：AIHot 有收录 {len(tracked)} 个 {tracked}")
    print(f"           AIHot 未收录 {len(untracked)} 个，需 exa 按账号名补：{untracked}")
    print(f"HN ≥{args.hn_min} 分 {len(result['hn'])} 条：")
    for h in result["hn"][:15]:
        print(f"  {h['points']:>4} 分 {h['comments']:>4} 评  {h['title'][:70]}  {h['hn_url']}")
    if out:
        print(f"→ {out}")


# ---------------------------------------------------------------- lookup

def cmd_lookup(args):
    since_ts = int((datetime.now(timezone.utc) - timedelta(days=args.days)).timestamp())
    q = args.query
    print(f"lookup: {q}")
    try:
        hits = hn_search(q, since_ts, hits=10)
        # 标题查询用宽松版相关性：一半以上的实词要出现在标题或链接里
        words = [w for w in q.lower().split() if len(w) > 3]
        def loose(h):
            hay = f"{h.get('title') or ''} {h.get('url') or ''}".lower()
            return sum(w in hay for w in words) * 2 >= len(words)
        hits = [h for h in hits if loose(h)]
        print(f"HN（{args.days} 天内）{len(hits)} 条：")
        for h in hits:
            print(f"  {h['points']:>4} 分 {h['comments']:>4} 评  {h['title'][:70]}  {h['hn_url']}")
    except RuntimeError as e:
        print(f"  x HN 失败：{e}")
    try:
        items = aihot_items(q=q, limit=8)
        print(f"AIHot（7 天内，mode=all）{len(items)} 条：")
        for it in items:
            print(f"  [{it['source']}] {it['title'][:70]}  {it['url']}")
    except RuntimeError as e:
        print(f"  x AIHot 失败：{e}")


def cmd_x(args):
    import html as _html
    import re as _re
    for url in args.urls:
        try:
            d = curl("https://publish.twitter.com/oembed?omit_script=1&" + urlencode({"url": url}))
            text = _re.sub(r"\s+", " ", _html.unescape(_re.sub(r"<[^>]+>", " ", d.get("html", "")))).strip()
            print(f"{d.get('author_name')} (@{(d.get('author_url') or '').rstrip('/').split('/')[-1]}) | {text}")
        except RuntimeError as e:
            print(f"x 失败 {url}: {e}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("--since", required=True, help="窗口起点 YYYY-MM-DD")
    s.add_argument("--out", help="候选 JSON 输出路径")
    s.add_argument("--topic", help="定向模式主题，追加到关键词")
    s.add_argument("--hn-min", type=int, default=100)
    s.add_argument("--accounts", default=str(DEFAULT_ACCOUNTS))
    s.set_defaults(fn=cmd_scan)
    l = sub.add_parser("lookup")
    l.add_argument("query")
    l.add_argument("--days", type=int, default=90)
    l.set_defaults(fn=cmd_lookup)
    x = sub.add_parser("x")
    x.add_argument("urls", nargs="+")
    x.set_defaults(fn=cmd_x)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
