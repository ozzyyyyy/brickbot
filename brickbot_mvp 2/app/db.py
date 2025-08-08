
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "brickbot.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        price INTEGER NOT NULL,
        bedrooms INTEGER NOT NULL,
        description TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        budget_min INTEGER NOT NULL,
        budget_max INTEGER NOT NULL,
        preferred_city TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progression (
        lead_id INTEGER PRIMARY KEY,
        status TEXT NOT NULL,
        last_update TEXT NOT NULL,
        FOREIGN KEY(lead_id) REFERENCES leads(id)
    )
    """)
    _ensure_indexes(cur)
    conn.commit()
    conn.close()


def _ensure_indexes(cur):
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone)")
    except Exception:
        pass

# Inject index creation in init_db()
