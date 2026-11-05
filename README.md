# Car Dealership Portal — IBM Full Stack Capstone (Course 12)

Local-only Django build of the IBM Full Stack Software Developer capstone
project. **Not submitted to Coursera / Mark. Not published to GitHub.**

## What it is
A Django dealership app (template/fork style: `djangoproj` + `djangoapp`):
- Static pages: About Us (`/about/`) and Contact Us (`/contact/`, form saves a `ContactMessage`)
- User management: register / login / logout with Django auth; adding a review requires login
- Back-end services: `CarMake` / `CarModel` Django models, dealer + review JSON APIs,
  and `djangoapp/restapis.py` proxy helpers (`get_request` / `post_request`,
  `get_dealers_from_cf`, `get_dealer_reviews_from_cf`) that proxy an external
  Node/Mongo dealers service when `DEALERS_API_URL` / `REVIEWS_API_URL` are set,
  and fall back to the local SQLite database otherwise
- Dynamic pages: dealer list (`/dealers/`), dealer detail with reviews
  (`/dealer/<id>/`), add-review (`/dealer/<id>/add-review/`)
- Admin: `/admin/` (create a superuser with `python manage.py createsuperuser`)

## Run locally
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_dealership   # demo data: 3 dealers, 3 makes, 9 models
.venv/bin/python manage.py runserver 127.0.0.1:8000
# open http://127.0.0.1:8000/  — About: /about/  Contact: /contact/
```

## Test
```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

## API endpoints
- `GET /api/dealers/` — all dealers (JSON)
- `GET /api/dealers/<id>/` — one dealer
- `GET /api/dealers/<id>/reviews/` — reviews for a dealer
- `GET /api/inventory/` — car models (inventory service)
- `GET /api/cars/` — car makes

## Still NOT done (see SUMMARY.md)
- No GitHub repo / public URLs; no Coursera/Mark submission; no peer review
- No React front end, no Node/Mongo back-end service, no Docker/Kubernetes
  deployment, no IBM Code Engine deployment, no live CI run — a `Dockerfile`
  and `.github/workflows/ci.yml` are present as files only, and Docker is not
  installed in this VM.
