# rotate_logs.py
import pathlib, datetime, shutil
RAW = pathlib.Path("captured.jsonl")
if RAW.exists() and RAW.stat().st_size:
    ts = datetime.datetime.now().strftime("%Y-%m-%d")
    dst = pathlib.Path("logs") / f"captured-{ts}.jsonl"
    dst.parent.mkdir(exist_ok=True)
    shutil.move(RAW, dst)
    RAW.touch()
    print("Rotated to", dst)
else:
    print("Nothing to rotate.")
