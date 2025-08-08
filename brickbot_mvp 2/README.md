
# BrickBot / PropMind — MVP (UK Estate Agency AI Helper)

Minimal FastAPI backend to:
- Add/list properties
- Add/list leads
- Match leads to properties (by city + budget band)
- Track simple sales progression milestones for a lead
- Send email previews to console (local dev)

## 1) Requirements
- Python 3.10+
- `pip install -r requirements.txt`

## 2) Run (dev)
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs for Swagger UI.

## 3) Local email testing (optional)
Run a local debug SMTP server in another terminal:
```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

## 4) Notes
- DB: SQLite file `brickbot.db` in project root (auto-created).
- WhatsApp sending is stubbed (print only). For production, integrate Twilio/Meta WhatsApp Business API.
- This is an MVP; no auth. Add JWT before real usage.
- AML/IDV not included in MVP. Hook later via providers (e.g. Credas/Thirdfort/SmartSearch) in `integrations/`.
```