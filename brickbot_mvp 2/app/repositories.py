
from .db import get_conn

# Property CRUD
def add_property(p):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO properties (id, address, city, price, bedrooms, description) VALUES (?, ?, ?, ?, ?, ?)",
        (p.id, p.address, p.city, p.price, p.bedrooms, p.description),
    )
    conn.commit()
    conn.close()

def list_properties(city: str | None = None):
    conn = get_conn()
    cur = conn.cursor()
    if city:
        cur.execute("SELECT * FROM properties WHERE city = ?", (city,))
    else:
        cur.execute("SELECT * FROM properties")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

# Lead CRUD
def add_lead(l):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO leads (id, name, email, budget_min, budget_max, preferred_city) VALUES (?, ?, ?, ?, ?, ?)",
        (l.id, l.name, l.email, l.budget_min, l.budget_max, l.preferred_city),
    )
    conn.commit()
    conn.close()

def list_leads():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM leads")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_lead(lead_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# Progression
def upsert_progression(lead_id: int, status: str, last_update: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO progression (lead_id, status, last_update) VALUES (?, ?, ?)",
        (lead_id, status, last_update),
    )
    conn.commit()
    conn.close()

def get_progression(lead_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM progression WHERE lead_id = ?", (lead_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def find_lead_by_email_phone(email: str | None, phone: str | None):
    conn = get_conn()
    cur = conn.cursor()
    if email and phone:
        cur.execute("SELECT * FROM leads WHERE email = ? OR phone = ?", (email, phone))
    elif email:
        cur.execute("SELECT * FROM leads WHERE email = ?", (email,))
    elif phone:
        cur.execute("SELECT * FROM leads WHERE phone = ?", (phone,))
    else:
        conn.close()
        return None
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_lead_fields(lead_id: int, fields: dict):
    if not fields:
        return
    allowed = {"name","email","phone","budget_min","budget_max","preferred_city","source","raw"}
    sets = []
    vals = []
    for k,v in fields.items():
        if k in allowed:
            sets.append(f"{k} = ?")
            vals.append(v)
    if not sets:
        return
    vals.append(lead_id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE leads SET {', '.join(sets)} WHERE id = ?", vals)
    conn.commit()
    conn.close()
