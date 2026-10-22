#!/usr/bin/env python3
"""exa REST API 封装：search + contents（等价 paper-radar 硬规则 3 的 web_search_exa / web_fetch_exa）。

key 从 ~/.hermes/credentials/exa-api-key 读取（chmod 600），不硬编码、不进仓库。
只依赖标准库 + 系统 curl。

用法：
  python3 exa_api.py search "query 文本" [--n 5] [--content-type auto|webpage|news|research paper]
  python3 exa_api.py contents <result_id> [result_id ...]

输出：每行一个 JSON 对象（jsonl），方便脚本/agent 解析。
  search 行:  {"id","url","title","text"(截断 2000 字),"publishedDate"}
  contents 行: {"id","url","title","text"(全文)}
失败时 exit 非 0，错误写 stderr。
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

KEY_FILE = Path.home() / ".hermes" / "credentials" / "exa-api-key"
API = "https://api.exa.ai"


def api(path, payload):
    if not KEY_FILE.exists():
        raise RuntimeError(f"exa key 文件不存在: {KEY_FILE}")
    key = KEY_FILE.read_text().strip()
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "90", "-X", "POST", f"{API}/{path}",
         "-H", f"x-api-key: {key}", "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"curl failed ({r.returncode}): {r.stderr.strip()[:200]}")
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"non-JSON response: {r.stdout[:200]!r}")
    if isinstance(d, dict) and d.get("error") and "results" not in d and "contents" not in d:
        raise RuntimeError(f"exa API error: {str(d['error'])[:300]}")
    return d


def cmd_search(args):
    payload = {"query": args.query, "numResults": args.n, "type": "auto"}
    if args.content_type:
        # exa 的 type 是搜索类型（auto/neural/keyword…），内容类别走 category
        if args.content_type in ("webpage", "news", "research paper"):
            payload["category"] = args.content_type
        else:
            payload["type"] = args.content_type
    if args.start_date:
        payload["startPublishedDate"] = args.start_date
    if args.end_date:
        payload["endPublishedDate"] = args.end_date
    d = api("search", payload)
    for r in d.get("results", []):
        print(json.dumps({
            "id": r.get("id"),
            "url": r.get("url"),
            "title": r.get("title"),
            "text": (r.get("text") or "")[:2000],
            "publishedDate": r.get("publishedDate"),
        }, ensure_ascii=False))
    if not d.get("results"):
        print("NO_RESULTS", file=sys.stderr)


def cmd_contents(args):
    d = api("contents", {"ids": args.ids, "text": {"maxCharacters": 120000}})
    for r in d.get("contents", []):
        print(json.dumps({
            "id": r.get("id"),
            "url": r.get("url"),
            "title": r.get("title"),
            "text": r.get("text") or "",
        }, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--n", type=int, default=5)
    s.add_argument("--content-type", default=None)
    s.add_argument("--start-date", default=None, help="startPublishedDate, YYYY-MM-DD")
    s.add_argument("--end-date", default=None, help="endPublishedDate, YYYY-MM-DD")
    s.set_defaults(fn=cmd_search)
    c = sub.add_parser("contents")
    c.add_argument("ids", nargs="+")
    c.set_defaults(fn=cmd_contents)
    args = ap.parse_args()
    try:
        args.fn(args)
    except RuntimeError as e:
        print(f"exa_api: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
