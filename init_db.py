import sqlite3
SCHEMA = """
CREATE TABLE IF NOT EXISTS traffic (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ts       REAL   NOT NULL,
  host     TEXT   NOT NULL,
  endpoint TEXT   NOT NULL,
  prompt   TEXT
);
"""
conn = sqlite3.connect("scanner.db")
conn.executescript(SCHEMA)
conn.close()
print("✔ scanner.db initialised → table `traffic` ready")