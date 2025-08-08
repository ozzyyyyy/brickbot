
from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Optional, List
from .db import init_db
from .models import PropertyIn, Property, LeadIn, Lead, MatchResult, ProgressionUpdate
from .repositories import add_property, list_properties, add_lead, list_leads, get_lead, upsert_progression, get_progression, find_lead_by_email_phone, update_lead_fields
from .matching import match_for_lead
from .messaging import send_email_console

app = FastAPI(title="BrickBot / PropMind — MVP", version="0.1.0")


@app.on_event("startup")
def on_start():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "name": "BrickBot/PropMind MVP", "version": "0.1.0"}

# ---- Properties ----
@app.post("/properties/", response_model=Property)
def create_property(p: PropertyIn):
    add_property(p)
    return p

@app.get("/properties/", response_model=List[Property])
def get_properties(city: Optional[str] = Query(None, description="Filter by city")):
    rows = list_properties(city=city)
    return rows

# ---- Leads ----
@app.post("/leads/", response_model=Lead)
def create_lead(l: LeadIn):
    add_lead(l)
    # initial progression row
    upsert_progression(l.id, status="new", last_update=datetime.now(timezone.utc).isoformat())
    return l

@app.get("/leads/", response_model=List[Lead])
def get_all_leads():
    return list_leads()

# ---- Matching ----
@app.get("/match/{lead_id}", response_model=MatchResult)
def match_for(lead_id: int):
    ids = match_for_lead(lead_id)
    if ids is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"lead_id": lead_id, "matched_property_ids": ids}

# ---- Email sending ----
@app.post("/send_match/{lead_id}")
def send_match_email(lead_id: int, bg: BackgroundTasks):
    lead = get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    ids = match_for_lead(lead_id)
    subject = f"Your property matches in {lead['preferred_city']}"
    body = "\n".join([
        f"Hi {lead['name']},",
        "",
        f"We found {len(ids)} matches within your budget (£{lead['budget_min']}–£{lead['budget_max']}).",
        f"City: {lead['preferred_city']}",
        "IDs: " + (", ".join(map(str, ids)) if ids else "No matches yet"),
        "",
        "Thanks, BrickBot"
    ])
    bg.add_task(send_email_console, lead["email"], subject, body)
    # update progression
    upsert_progression(lead_id, status="matches_sent", last_update=datetime.now().isoformat())
    return {"queued": True}

# ---- Sales progression ----
@app.get("/progression/{lead_id}")
def get_progress(lead_id: int):
    row = get_progression(lead_id)
    if not row:
        raise HTTPException(status_code=404, detail="No progression record for lead")
    return row

@app.post("/progression/{lead_id}")
def update_progress(lead_id: int, payload: ProgressionUpdate):
    upsert_progression(lead_id, status=payload.status, last_update=datetime.now(timezone.utc).isoformat())
    return {"ok": True, "lead_id": lead_id, "status": payload.status}


# ---- Marketing Site (public) ----
from .config import PRODUCT_NAME, TAGLINE, PRIMARY_COLOR, CTA_WHATSAPP, CTA_TRIAL_URL
from datetime import datetime
@app.get('/', response_class=HTMLResponse)
def marketing_home(request: Request):
    ctx = {"request": request, "title": PRODUCT_NAME, "product_name": PRODUCT_NAME, "tagline": TAGLINE, "primary_color": PRIMARY_COLOR, "whatsapp_cta": CTA_WHATSAPP, "trial_url": CTA_TRIAL_URL, "year": datetime.now().year}
    return TEMPLATES.TemplateResponse('home.html', ctx)

@app.get('/features', response_class=HTMLResponse)
def marketing_features(request: Request):
    ctx = {"request": request, "title": f"Features · {PRODUCT_NAME}", "product_name": PRODUCT_NAME, "primary_color": PRIMARY_COLOR, "year": datetime.now().year, "trial_url": CTA_TRIAL_URL}
    return TEMPLATES.TemplateResponse('features.html', ctx)

@app.get('/pricing', response_class=HTMLResponse)
def marketing_pricing(request: Request):
    ctx = {"request": request, "title": f"Pricing · {PRODUCT_NAME}", "product_name": PRODUCT_NAME, "primary_color": PRIMARY_COLOR, "year": datetime.now().year, "trial_url": CTA_TRIAL_URL}
    return TEMPLATES.TemplateResponse('pricing.html', ctx)

@app.get('/privacy', response_class=HTMLResponse)
def marketing_privacy(request: Request):
    ctx = {"request": request, "title": f"Privacy · {PRODUCT_NAME}", "product_name": PRODUCT_NAME, "primary_color": PRIMARY_COLOR, "year": datetime.now().year}
    return TEMPLATES.TemplateResponse('privacy.html', ctx)

@app.get('/terms', response_class=HTMLResponse)
def marketing_terms(request: Request):
    ctx = {"request": request, "title": f"Terms · {PRODUCT_NAME}", "product_name": PRODUCT_NAME, "primary_color": PRIMARY_COLOR, "year": datetime.now().year}
    return TEMPLATES.TemplateResponse('terms.html', ctx)
