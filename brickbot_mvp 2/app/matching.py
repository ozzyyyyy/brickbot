
from .db import get_conn

def match_for_lead(lead_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    lead = cur.fetchone()
    if not lead:
        conn.close()
        return []
    city = lead["preferred_city"]
    bmin = lead["budget_min"]
    bmax = lead["budget_max"]
    cur.execute(
        "SELECT id FROM properties WHERE city = ? AND price BETWEEN ? AND ? ORDER BY price ASC",
        (city, bmin, bmax),
    )
    ids = [r["id"] for r in cur.fetchall()]
    conn.close()
    return ids
