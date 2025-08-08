
# Deploy BrickBot to Render (one-time setup, ~10 minutes)

## Option A — Blueprint (recommended)
1) Push your `brickbot_mvp` folder to a new GitHub repo named `brickbot`.
2) Go to https://render.com -> New + -> **Blueprint**.
3) Connect your GitHub account and choose the `brickbot` repo.
4) Confirm and click **Apply**.
5) Wait ~2–5 minutes for provisioning and build.
6) You’ll get a URL like `https://brickbot.onrender.com`.
7) Update the **CONTACT_EMAIL** env var in the Render dashboard to your real email.

## Option B — Web Service (manual, also easy)
1) Render -> New + -> **Web Service** -> Connect your repo.
2) Build: `pip install -r requirements.txt`
3) Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4) Add env var CONTACT_EMAIL = your@email

> Demo uses SQLite with a small disk (configured in render.yaml). For production, add Render PostgreSQL and move persistence there.
