# dashboard.py
import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path("scanner.db")

@st.cache_data(ttl=5)   # refresh every 5 s
def load_data():
    if not DB_PATH.exists():
        return pd.DataFrame()
    con = sqlite3.connect(DB_PATH)
    return pd.read_sql(
        """
        SELECT
          datetime(ts, 'unixepoch', 'localtime') AS time,
          host,
          endpoint,
          prompt
        FROM traffic
        ORDER BY ts DESC
        LIMIT 500
        """,
        con,
    )

st.title("AI Posture Scanner – Live Flows")

data = load_data()
if data.empty:
    st.info("No data yet – run mitmproxy and ingest.py first.")
    st.stop()

# Host histogram
st.subheader("Top Hosts (last 500 flows)")
host_counts = data["host"].value_counts().reset_index()
host_counts.columns = ["Host", "Hits"]
st.bar_chart(host_counts, x="Host", y="Hits")

# Latest prompts table
st.subheader("Latest Prompts")
st.dataframe(data[["time", "host", "prompt"]], use_container_width=True)
