import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/prices.db")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            platform  TEXT,
            url       TEXT,
            title     TEXT,
            price     REAL,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_price(record: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO price_history (platform, url, title, price, fetched_at) VALUES (?,?,?,?,?)",
        (record["platform"], record["url"], record["title"],
         record["price"], datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def get_history(url: str, limit: int = 30) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT platform, price, fetched_at FROM price_history WHERE url=? ORDER BY fetched_at DESC LIMIT ?",
        (url, limit)
    ).fetchall()
    conn.close()
    return [{"platform": r[0], "price": r[1], "fetched_at": r[2]} for r in rows]
