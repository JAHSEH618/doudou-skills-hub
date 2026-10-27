#!/usr/bin/env python3
"""Batch exa search for 4 lines + X accounts. Results -> exa/<name>.jsonl"""
import subprocess, sys, os, time

BASE = "/Users/friedhelmliu/.hermes/skills/research/paper-radar"
EXA = f"{BASE}/scripts/exa_api.py"
OUT = f"{BASE}/reports/assets/2026-10-27/exa"
os.makedirs(OUT, exist_ok=True)

PAPER_START = "2026-10-15"   # wider than window; ledger dedupe catches old
X_START = "2026-10-23"

QUERIES = [
    # (name, query, n, start, category)
    ("hw_fp4",    "arXiv paper NVFP4 FP4 quantization LLM inference kernel Blackwell", 8, PAPER_START, "research paper"),
    ("hw_cxl",    "arXiv CXL memory pooling GPU inference LLM KV cache", 8, PAPER_START, "research paper"),
    ("hw_sdc",    "arXiv GPU cluster silent data corruption observability fault tolerance serving", 8, PAPER_START, "research paper"),
    ("mo_linear", "arXiv hybrid linear attention MoE sparse attention architecture LLM", 8, PAPER_START, "research paper"),
    ("mo_finetune","arXiv LoRA SFT reinforcement learning fine-tuning LLM post-training", 8, PAPER_START, "research paper"),
    ("mo_quant",  "arXiv LLM quantization compression weight-only int4 fp8", 8, PAPER_START, "research paper"),
    ("ss_serving","arXiv LLM inference serving scheduler KV cache prefill decode disaggregation", 8, PAPER_START, "research paper"),
    ("ss_agent",  "arXiv LLM agent memory RAG retrieval vector database", 8, PAPER_START, "research paper"),
    ("ss_rl",     "arXiv RL post-training infrastructure rollout agentic reinforcement learning system", 8, PAPER_START, "research paper"),
    ("em_eval",   "arXiv LLM evaluation benchmark reliability methodology audit", 8, PAPER_START, "research paper"),
    ("em_bench",  "arXiv empirical study LLM agent harness negative results", 8, PAPER_START, "research paper"),
    ("em_judge",  "arXiv LLM-as-a-judge reliability calibration judge", 8, PAPER_START, "research paper"),
    ("x_infra",   "vLLM SGLang FlashInfer PyTorch release announcement engineering", 8, X_START, None),
    ("x_models",  "DeepSeek Qwen Kimi GLM MiniMax Hunyuan new model open weights release", 8, X_START, None),
]

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
    with open(f"{OUT}/{name}.err", "w") as f:
        f.write(r.stderr)
    nout = len([l for l in r.stdout.splitlines() if l.strip()])
    print(f"{name}: {nout} results (exit {r.returncode}) {r.stderr.strip()[:80]}", flush=True)
    if r.returncode != 0:
        fails.append(name)
    time.sleep(2)

print("FAILS:", fails if fails else "none")
