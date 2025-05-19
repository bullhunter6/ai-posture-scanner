import os, requests, json
from dotenv import load_dotenv
load_dotenv()

VERIFY_PEM = r"C:\Users\saikr\.mitmproxy\mitmproxy-ca-cert.pem"
PROXIES    = {
    "http":  "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}
data = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role":"user","content":"hello"}],
  "max_tokens": 5
}

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=data,
    timeout=30,
    verify=VERIFY_PEM,
    proxies=PROXIES,          # ← tell requests to use mitmproxy
)
print(resp.json())
