import json, sqlite3, pathlib, sys

DB        = "scanner.db"
LOG_FILE  = pathlib.Path("captured.jsonl")

if not LOG_FILE.exists():
    sys.exit("captured.jsonl not found – run mitmproxy first 🛑")

conn = sqlite3.connect(DB)
cur  = conn.cursor()

with LOG_FILE.open(encoding="utf‑8") as fh:
    for line in fh:
        row = json.loads(line)
        cur.execute(
            """INSERT INTO traffic (ts,host,endpoint,prompt)
                   VALUES (?,?,?,?)""",
            (row["ts"], row["host"], row["endpoint"], row.get("body"))
        )
conn.commit()
print(f"✔ inserted {cur.rowcount} rows → traffic table")