# tests/test_ingest.py
import sqlite3, os, json
def test_insert():
    conn = sqlite3.connect("scanner.db")
    rows = conn.execute("SELECT COUNT(*) FROM traffic").fetchone()[0]
    assert rows > 0, "traffic table should not be empty"

def test_json_schema():
    sample = json.loads(open("captured.jsonl").readline())
    assert {"ts","host","endpoint"}.issubset(sample), "missing keys"
