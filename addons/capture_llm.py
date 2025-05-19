# addons/capture_llm.py
import json
from pathlib import Path
from mitmproxy import http

LLM_HOSTS = {
    "api.openai.com",
    "api.anthropic.com",
    "oai.azure.com",
    "huggingface.co",
}

OUTFILE = Path("captured.jsonl")

def request(flow: http.HTTPFlow):
    if flow.request.host in LLM_HOSTS:
        entry = {
            "ts": flow.request.timestamp_start,
            "host": flow.request.host,
            "endpoint": flow.request.path,
            "method": flow.request.method,
            # Request body may be bytes → decode best-effort
            "body": flow.request.get_text(strict=False)[:2000],  # truncate huge payloads
        }
        with OUTFILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
