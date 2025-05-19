# tail_ingest.py
import json, sqlite3, time, pathlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DB = "scanner.db"
LOG = pathlib.Path("captured.jsonl")

class TailHandler(FileSystemEventHandler):
    def __init__(self):
        self.offset = LOG.stat().st_size if LOG.exists() else 0
        self.conn   = sqlite3.connect(DB, isolation_level=None)

    def on_modified(self, event):
        if event.src_path != str(LOG):   # ignore other files
            return
        with LOG.open("r", encoding="utf-8") as f:
            f.seek(self.offset)
            for line in f:
                try:
                    row = json.loads(line)
                    self.conn.execute(
                        "INSERT INTO traffic (ts,host,endpoint,prompt) VALUES (?,?,?,?)",
                        (row["ts"], row["host"], row["endpoint"], row.get("body","")),
                    )
                except Exception as e:
                    print("⛔ bad line:", e)
            self.offset = f.tell()

if __name__ == "__main__":
    if not LOG.exists():
        print("Waiting for", LOG); LOG.touch()
    observer = Observer()
    observer.schedule(TailHandler(), ".", recursive=False)
    observer.start()
    print("▶ live ingest running — Ctrl-C to stop")
    try:
        while True: time.sleep(1)
    finally:
        observer.stop(); observer.join()
