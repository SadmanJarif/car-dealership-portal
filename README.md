# Car Dealership Portal — IBM Full Stack Capstone (Course 12)
# Project: fullstack_developer_capstone

Full-stack build of the IBM Full Stack Software Developer capstone
project: Django back end + React front end + Node.js dealers/reviews
back-end services, all in this repo. Course project name:
**fullstack_developer_capstone**. **Not submitted to Coursera / Mark
yet — published to GitHub at https://github.com/SadmanJarif/car-dealership-portal.**
(See `RETAKE-ANSWERS.md` for the checklist retake sheet and `SUMMARY.md`
for verification evidence.)

## Layout
```
course12-capstone/
├── manage.py, requirements.txt, Dockerfile   # Django app (djangoproj + djangoapp)
├── frontend/          # React front end (Vite) — dealer list/detail, add-review, REGISTER page
├── services/          # Node.js dealers (:3001) + reviews (:3002) back-end services
├── .github/workflows/ci.yml   # CI definition — GitHub Actions run #17 succeeded (2026-11-06)
├── SUMMARY.md         # build + verification record
└── RETAKE-ANSWERS.md  # Coursera Modules 1–4 retake answer sheet
```

## What it is
- Static pages: About Us (`/about/`) and Contact Us (`/contact/`, form saves a `ContactMessage`)
- User management: register / login / logout with Django auth; adding a review requires login.
  Superuser exists locally (`admin`, created with `createsuperuser` — see note below).
  The React nav shows Login/Register when logged out and username/Logout when logged in.
- Back-end services: `CarMake` / `CarModel` Django models, dealer + review JSON APIs,
  and `djangoapp/restapis.py` proxy helpers (`get_request` / `post_request`,
  `get_dealers_from_cf`, `get_dealer_by_id_from_cf`, `get_dealers_by_state_from_cf`,
  `get_dealer_reviews_from_cf`, `post_review`) that proxy the Node services in
  `services/` when `DEALERS_API_URL` / `REVIEWS_API_URL` are set, and fall back to
  the local SQLite database otherwise. The dealers service also exposes the
  IBM-style `/fetchDealers`, `/fetchDealer/<id>`, `/fetchDealers/<state>` endpoints.
- Dynamic pages (React, `frontend/`): dealer list with search, dealer detail with
  reviews + stock, add-review form (JSON POST to `/api/dealers/<id>/reviews/`,
  form POST fallback), and a registration page.
- Admin: `/admin/` (superuser `admin` exists in the local dev DB only —
  `db.sqlite3` is gitignored, so recreate it on any fresh checkout with
  `python manage.py createsuperuser`).

## Run locally (full stack)
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_dealership   # demo data: 3 dealers, 3 makes, 9 models, 3 reviews
.venv/bin/python manage.py createsuperuser  # only on a fresh checkout (admin already exists locally)

# Node back-end services (dealers :3001, reviews :3002)
cd services && ./start-all.sh && cd ..

# Django, wired to the Node services (omit the env vars to use the local DB instead)
DEALERS_API_URL=http://127.0.0.1:3001/dealers REVIEWS_API_URL=http://127.0.0.1:3002/reviews \
  .venv/bin/python manage.py runserver 127.0.0.1:8000
# open http://127.0.0.1:8000/

# React front end (proxies /api, /dealer, /login, /logout, /register to Django :8000)
cd frontend && npm install && npm run dev     # http://127.0.0.1:5173
# or: npm run build && npm run preview        # http://127.0.0.1:4173
```

## Test
```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test        # 10 tests (was 6 before the integration)
cd services && ./test.sh               # live endpoint check for both Node services
cd frontend && npm run build           # production build into frontend/dist/
```

## API endpoints
- `GET /api/me/` — `{authenticated, username}` (drives the React nav)
- `GET /api/dealers/` — all dealers (JSON)
- `GET /api/dealers/<id>/` — one dealer
- `GET /api/dealers/<id>/reviews/` — reviews for a dealer
- `POST /api/dealers/<id>/reviews/` — submit a review as JSON (login + CSRF required, 201;
  also forwards to the external reviews service via `restapis.post_review` when configured)
- `GET /api/inventory/` — car models (inventory service)
- `GET /api/cars/` — car makes

## Still NOT done (see SUMMARY.md)
- Published to GitHub (https://github.com/SadmanJarif/car-dealership-portal); no Coursera/Mark submission yet; no peer review (Module 6).
- **Module 5 is still blocked:** Docker is NOT installed on this VM
  (`docker`, `podman`, `nerdctl` all absent), so no image was built and
  nothing is deployed to Kubernetes / IBM Code Engine. CI itself HAS run:
  GitHub Actions run #17 succeeded (2026-11-06) — the `Dockerfile` is
  still a file only, with no image built from it on this VM.
