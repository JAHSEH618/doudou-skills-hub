#!/usr/bin/env python3
"""2026-10-29 daily run: arXiv window fetch + exa 4-line batch + X accounts.
Window 10-27 -> 10-29 (arXiv cutoff 10-26 to overlap previous run; ledger dedupes).
"""
import json, os, subprocess, sys, time, urllib.request, urllib.parse
from xml.etree import ElementTree as ET

BASE = "/Users/friedhelmliu/.hermes/skills/research/paper-radar"
OUT = f"{BASE}/reports/assets/2026-10-29/exa"
os.makedirs(OUT, exist_ok=True)
EXA = f"{BASE}/scripts/exa_api.py"
CUTOFF = "2026-10-26"
CATS = ["cs.AI","cs.LG","cs.CL","cs.CV","cs.SE","stat.ML","cs.CR","cs.DC",
        "cs.IR","cs.AR","cs.OS","cs.RO","cs.HC"]
NS = {"a": "http://www.w3.org/2005/Atom"}

def arxiv_cat(cat, offset=0):
    q = urllib.parse.urlencode({
        "search_query": f"cat:{cat}",
        "sortBy": "submittedDate", "sortOrder": "descending",
        "start": offset, "max_results": 400,
    })
    url = f"https://export.arxiv.org/api/query?{q}"
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "paper-radar/1.0"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return r.read()

def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("a:entry", NS):
        eid = e.findtext("a:id", "", NS)
        title = " ".join((e.findtext("a:title", "", NS) or "").split())
        pub = e.findtext("a:published", "", NS)
        summ = " ".join((e.findtext("a:summary", "", NS) or "").split())
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        out.append({"id": eid.rsplit("/", 1)[-1], "title": title,
                    "published": pub, "cats": cats, "abstract": summ,
                    "url": eid})
    return out

all_entries = {}
arxiv_errs = []
for cat in CATS:
    try:
        batch = parse(arxiv_cat(cat))
        if not batch:
            arxiv_errs.append(f"{cat}: 0 entries")
            continue
        oldest = batch[-1]["published"][:10]
        # if we still have more in-window papers, fetch one more page
        if oldest >= CUTOFF:
            try:
                batch += parse(arxiv_cat(cat, offset=400))
            except Exception as ex:
                arxiv_errs.append(f"{cat}: page2 fail {ex}")
        kept = [e for e in batch if e["published"][:10] >= CUTOFF]
        for e in kept:
            all_entries[e["id"]] = e
        print(f"arxiv {cat}: {len(batch)} fetched, {len(kept)} in-window (oldest {oldest})", flush=True)
    except Exception as ex:
        arxiv_errs.append(f"{cat}: {ex}")
        print(f"arxiv {cat}: FAIL {ex}", flush=True)
    time.sleep(3)

papers = sorted(all_entries.values(), key=lambda e: e["published"], reverse=True)
with open(f"{OUT}/arxiv_window.json", "w") as f:
    json.dump(papers, f, ensure_ascii=False, indent=1)
print(f"arxiv total in-window unique: {len(papers)}  errs={arxiv_errs or 'none'}", flush=True)

# ---------------- exa batch ----------------
PAPER_START = "2026-10-24"
X_START = "2026-10-27"
QUERIES = [
    ("hw_fp4",    "arXiv paper NVFP4 FP4 FP8 low precision training inference kernel GPU", 8, PAPER_START, "research paper"),
    ("hw_cxl",    "arXiv CXL memory pooling disaggregated memory GPU serving inference", 8, PAPER_START, "research paper"),
    ("hw_cluster","arXiv large-scale training cluster fault tolerance silent data corruption GPU observability", 8, PAPER_START, "research paper"),
    ("mo_arch",   "arXiv hybrid linear attention sparse attention MoE architecture LLM", 8, PAPER_START, "research paper"),
    ("mo_quant",  "arXiv LLM quantization compression weight sparsity int4 fp8 post-training", 8, PAPER_START, "research paper"),
    ("mo_finetune","arXiv reinforcement learning LLM fine-tuning recipe SFT post-training", 8, PAPER_START, "research paper"),
    ("ss_serving","arXiv LLM inference serving scheduler KV cache prefill decode disaggregation", 8, PAPER_START, "research paper"),
    ("ss_agent",  "arXiv LLM agent memory RAG retrieval long-context", 8, PAPER_START, "research paper"),
    ("ss_rl",     "arXiv agentic reinforcement learning rollout infrastructure environment scaling", 8, PAPER_START, "research paper"),
    ("em_eval",   "arXiv LLM evaluation benchmark reliability methodology audit", 8, PAPER_START, "research paper"),
    ("em_empir",  "arXiv empirical study LLM agent harness failure analysis negative results", 8, PAPER_START, "research paper"),
    ("x_infra",   "vLLM SGLang FlashInfer PyTorch release announcement engineering", 8, X_START, None),
    ("x_models",  "DeepSeek Qwen Kimi GLM MiniMax Hunyuan MiniCPM new model open weights release", 8, X_START, None),
]
searches = []
fails = []
for name, q, n, start, cat in QUERIES:
    cmd = [sys.executable, EXA, "search", q, "--n", str(n)]
    if start:
        cmd += ["--start-date", start]
    if cat:
        cmd += ["--content-type", cat]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=150)
    with open(f"{OUT}/{name}.jsonl", "w") as f:
        f.write(r.stdout)
    nout = len([l for l in r.stdout.splitlines() if l.strip()])
    line = {"name": name, "query": q, "n_results": nout,
            "exit": r.returncode, "err": r.stderr.strip()[:200],
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    searches.append(line)
    print(f"exa {name}: {nout} results (exit {r.returncode}) {r.stderr.strip()[:100]}", flush=True)
    if r.returncode != 0:
        fails.append(name)
    time.sleep(2)

with open(f"{OUT}/searches.jsonl", "w") as f:
    for s in searches:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")
print("FAILS:", fails if fails else "none")
print("DONE")
