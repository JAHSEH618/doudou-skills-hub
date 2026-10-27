#!/usr/bin/env python3
"""Fetch arXiv window [2026-10-22 18:00 UTC, 2026-10-27 06:00 UTC) for 13 cats,
merge with 10-25 arxiv-window.jsonl (covers up to 2610.31670)."""
import urllib.request, re, json, time, sys

CATS = ["cs.LG", "cs.CL", "cs.DC", "cs.DB", "cs.AR", "cs.OS", "cs.AI", "cs.IR",
        "cs.CR", "cs.NI", "cs.DL", "cs.SE", "cs.CE"]
LIMITS = {"cs.LG": 3200, "cs.CL": 2200, "cs.DC": 1100, "cs.DB": 1800,
          "cs.AR": 1100, "cs.OS": 1100, "cs.AI": 2200, "cs.IR": 1400,
          "cs.CR": 1100, "cs.NI": 1100, "cs.DL": 1100, "cs.SE": 1100, "cs.CE": 700}
RANGE = "202610221800+TO+202610270600"

def api(cat, limit, tries=4):
    url = ("https://export.arxiv.org/api/query?search_query=cat:%s+AND+submittedDate:[%s]"
           "&sortBy=submittedDate&sortOrder=descending&max_results=%d" % (cat, RANGE, limit))
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (paper-radar daily scan)"})
            with urllib.request.urlopen(req, timeout=240) as r:
                data = r.read().decode(errors="ignore")
                if len(data) > 2000:
                    return data
        except Exception as e:
            print(f"[{cat}] try {i} ERR {e}", file=sys.stderr)
        time.sleep(8)
    return None

entries = {}
failed = []
truncated = []
for cat in CATS:
    data = api(cat, LIMITS[cat])
    if not data:
        print(f"[{cat}] FETCH FAILED", file=sys.stderr)
        failed.append(cat)
        continue
    items = re.findall(r"<entry>(.*?)</entry>", data, re.S)
    if len(items) >= LIMITS[cat]:
        truncated.append(cat)
    n = 0
    for it in items:
        aid = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", it)
        if not aid:
            continue
        aid = aid.group(1).split("v")[0]
        pub = re.search(r"<published>(.*?)</published>", it)
        if not pub:
            continue
        pub = pub.group(1)
        if not ("2026-10-22T18:00" <= pub <= "2026-10-27T06:00"):
            continue
        if aid in entries:
            continue
        title = re.search(r"<title>(.*?)</title>", it, re.S)
        summ = re.search(r"<summary>(.*?)</summary>", it, re.S)
        entries[aid] = {
            "id": aid, "published": pub,
            "title": " ".join(title.group(1).split()) if title else "",
            "abstract": " ".join(summ.group(1).split()) if summ else "",
            "cats": cat,
        }
        n += 1
    print(f"[{cat}] {n} new entries", file=sys.stderr)
    time.sleep(4)

out = sorted(entries.values(), key=lambda e: e["id"], reverse=True)
print(f"FRESH TOTAL: {len(out)}; failed cats: {failed}; truncated cats: {truncated}")
if out:
    print("newest:", out[0]["id"], out[0]["published"], out[0]["title"][:60])
    print("oldest:", out[-1]["id"], out[-1]["published"])

base = "/Users/friedhelmliu/.hermes/skills/research/paper-radar/reports/assets"
json.dump(out, open(f"{base}/2026-10-27/arxiv-fresh.jsonl", "w"), ensure_ascii=False, indent=0)

old = json.load(open(f"{base}/2026-10-25/arxiv-window.jsonl"))
merged = {e["id"]: e for e in old}
for e in out:
    merged.setdefault(e["id"], e)
full = sorted(merged.values(), key=lambda e: e["id"], reverse=True)
json.dump(full, open(f"{base}/2026-10-27/arxiv-window.jsonl", "w"), ensure_ascii=False, indent=0)
print(f"MERGED WINDOW TOTAL: {len(full)} (10-25 window {len(old)} + fresh {len(out)}, overlap {len(old)+len(out)-len(full)})")
print("merged id range:", full[-1]["id"], "..", full[0]["id"])
