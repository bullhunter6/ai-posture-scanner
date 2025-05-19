import argparse, sqlite3, textwrap, pandas as pd, rich.console, rich.table

DB = "scanner.db"

parser = argparse.ArgumentParser(
    description="Query AI‑traffic database",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("""
      examples:
        python cli.py top-hosts 5
        python cli.py last-prompts 3
    """))
sub = parser.add_subparsers(dest="cmd", required=True)

sub_top = sub.add_parser("top-hosts", help="Show most frequent hosts")
sub_top.add_argument("n", type=int, nargs="?", default=10)

sub_last = sub.add_parser("last-prompts", help="Show last N prompts")
sub_last.add_argument("n", type=int, nargs="?", default=5)

args = parser.parse_args()
con  = sqlite3.connect(DB)
console = rich.console.Console()

def show(df):
    table = rich.table.Table(show_header=True, header_style="bold magenta")
    for col in df.columns:
        table.add_column(col)
    for _, row in df.iterrows():
        table.add_row(*map(str, row))
    console.print(table)

if args.cmd == "top-hosts":
    df = pd.read_sql(f"""SELECT host, COUNT(*) AS hits
                         FROM traffic GROUP BY host
                         ORDER BY hits DESC LIMIT {args.n}""", con)
    show(df)
elif args.cmd == "last-prompts":
    df = pd.read_sql(f"""SELECT datetime(ts,'unixepoch','localtime') AS time, host, substr(prompt,1,120) AS prompt
                         FROM traffic ORDER BY ts DESC LIMIT {args.n}""", con)
    show(df)