# Car Dealership Portal — Build Summary (IBM Course 12 Capstone)

Project: IBM Full Stack Software Developer Professional Certificate,
Course 12 — Full Stack Application Development Capstone Project
(Car Dealership Portal).
Location: `~/workspace/course12-capstone/`
Status: **Built and verified locally. NOT submitted to Coursera / Mark.
NOT published to GitHub. No scores or URLs invented.**
**Integration update 2026-11-06:** the React front end and the Node.js
dealers/reviews services (previously in the separate folders
`~/workspace/course12-capstone-react/` and
`~/workspace/course12-capstone-services/`) are now integrated into this
repo as `frontend/` and `services/`, with the missing pieces built:
React registration page, auth-aware React nav, `post_review`, by-id /
by-state fetch helpers, `/fetchDealers` endpoints, and proxy wiring in
the Django views. Full verification in "Integration update (2026-11-06)"
below and in `RETAKE-ANSWERS.md` (the Modules 2–4 retake sheet).

Built: 2026-11-06. Stack: Python 3.12, Django 4.2.16, SQLite, `requests` 2.31.0.
Virtualenv: `~/workspace/course12-capstone/.venv/` (not part of the submission).

## What was built

A Django dealership app in IBM template style (`djangoproj` project +
`djangoapp` app), with demo data seeded locally (3 dealers, 3 car makes,
9 car models, 3 reviews — demo data only, not real dealers):

- **Static pages:** About Us (`/about/`) and Contact Us (`/contact/`;
  the contact form saves a `ContactMessage` and shows a thank-you message).
- **User management:** register (`/register/`), login (`/login/`), logout,
  Django admin (`/admin/`). Adding a review requires login (anonymous
  users are redirected to login, HTTP 302 — verified).
- **Back-end services:** `CarMake` and `CarModel` Django models (CarModel
  has Sedan / SUV / Wagon types, year, dealer_id, FK to CarMake),
  `CarDealer` and `DealerReview` models, JSON APIs, and
  `djangoapp/restapis.py` proxy helpers (`get_request` / `post_request`,
  `get_dealers_from_cf`, `get_dealer_reviews_from_cf`) that proxy an
  external Node/Mongo dealers service when `DEALERS_API_URL` /
  `REVIEWS_API_URL` are set, and fall back to the local SQLite database
  otherwise (unset in local dev).
- **Dynamic pages:** home with dealer list (`/`), dealer list
  (`/dealers/`), dealer detail with reviews (`/dealer/<id>/`),
  add-review form (`/dealer/<id>/add-review/`, login required).
- **JSON APIs:** `GET /api/dealers/`, `GET /api/dealers/<id>/`,
  `GET /api/dealers/<id>/reviews/`, `GET /api/inventory/` (car models),
  `GET /api/cars/` (car makes).

## Modules 1–7 checklist coverage

Module numbering follows the Coursera course outline (7 modules).
Checklist question counts below are the counts published on the course
outline (SkillUp mirror of IBM CD0321EN): Static Pages 5 questions,
Back End 12, Dynamic Pages 6, User Management & CI/CD 8, Containerize 7,
Peer Review 1. **The Coursera checklist quizzes themselves were not
taken in this task (no Coursera access), so no quiz scores are claimed.**
Coverage below is of the hands-on lab work behind each checklist only.

| Module | Checklist | Local status |
|---|---|---|
| 1 — Application: Static Pages | Static Pages (5 Q) | **Done.** About Us + Contact Us pages render HTTP 200; contact form POST saves and shows thank-you (covered by test). |
| 2 — User Management and CI/CD | User Management & CI/CD (8 Q) | **Done (locally, 2026-11-06 integration).** Register/login/logout + login-gated add-review work and are tested. Superuser `admin` exists in the local DB. React nav now shows Login/Register vs username/Logout via `GET /api/me/`; React registration page added (`frontend/src/components/Register.jsx`, verified end to end). CI has run: GitHub Actions run #17 succeeded (2026-11-06). |
| 3 — Back End Services | Back End (12 Q) | **Done locally (2026-11-06 integration).** CarMake/CarModel models built, migrations applied, proxy services in `restapis.py` (now incl. `post_review`, `get_dealer_by_id_from_cf`, `get_dealers_by_state_from_cf`), dealer/review/inventory JSON APIs all return HTTP 200 with real seeded data. The external Node back-end service is now built (`services/`, Express, in-memory demo data, no MongoDB) and the Django views actually render its data when `DEALERS_API_URL`/`REVIEWS_API_URL` are set (verified live). New: `POST /api/dealers/<id>/reviews/` (JSON, 201, forwards via `post_review`). |
| 4 — Dynamic Pages | Dynamic Pages (6 Q) | **Done in Django AND React (2026-11-06 integration).** Dealer list, dealer detail + reviews, and add-review pages exist as server-rendered Django pages AND as React components in `frontend/` (DealerList, DealerDetail, ReviewForm, Register). React build passes; preview serves live data through the proxy. |
| 5 — Containerize & Deploy to Kubernetes | Containerize (7 Q) | **Not done beyond a file.** `Dockerfile` exists. Docker is not installed in this VM (`docker`/`podman`/`nerdctl` all absent, checked 2026-11-06), so no image was built, and nothing was deployed to Kubernetes or IBM Code Engine. |
| 6 — Share Your Project | Peer Review: Submit Your Work & Grade Your Peers (1 Q) | **Not done.** Requires a public GitHub repo + Mark submission + peer grading. None of that was done (see "What Mark needs next"). |
| 7 — Enhancement of Car Dealership Portal (optional) | Optional enhancement labs | **Partly done.** Car-inventory back-end service exists (`/api/inventory/`, 9 models). The React front-end enhancement is now built (`frontend/`). No optional lab was claimed or submitted. |

## File list

```
~/workspace/course12-capstone/
├── README.md                              # run / test / API docs (updated 2026-11-06)
├── SUMMARY.md                             # this file
├── RETAKE-ANSWERS.md                      # Coursera Modules 2–4 retake sheet (2026-11-06)
├── requirements.txt                       # Django==4.2.16, requests==2.31.0
├── manage.py
├── Dockerfile                             # file only — never built (no Docker in VM)
├── .github/workflows/ci.yml               # CI — GitHub Actions run #17 succeeded (2026-11-06)
├── .gitignore
├── db.sqlite3                             # local dev DB, seeded (3 dealers / 3 makes / 9 models / 3 reviews)
├── frontend/                              # React front end (integrated 2026-11-06)
│   ├── package.json / vite.config.js / index.html
│   └── src/ (App.jsx, api.js, components: DealerList, DealerDetail, ReviewForm, Register)
├── services/                              # Node dealers (:3001) + reviews (:3002) (integrated 2026-11-06)
│   ├── dealers-service/ (server.js, data.js)   # incl. /fetchDealers, /fetchDealer/:id, /fetchDealers/:state
│   ├── reviews-service/ (server.js, data.js)   # incl. POST /reviews
│   └── start-all.sh / stop-all.sh / test.sh
├── djangoproj/
│   ├── settings.py                        # SQLite, djangoapp installed, DEALERS/REVIEWS_API_URL env hooks
│   ├── urls.py                            # admin + djangoapp urls
│   ├── wsgi.py / asgi.py
├── djangoapp/
│   ├── models.py                          # CarMake, CarModel, CarDealer, DealerReview, ContactMessage
│   ├── views.py                           # static, auth, dealer, review, JSON API views
│   ├── urls.py                            # 15 routes (pages + auth + APIs)
│   ├── forms.py                           # RegistrationForm, ReviewForm, ContactForm
│   ├── restapis.py                        # get/post_request + dealers/reviews proxy helpers
│   ├── admin.py                           # all 5 models in Django admin
│   ├── tests.py                           # 6 tests
│   ├── migrations/0001_initial.py         # generated, applied
│   ├── management/commands/seed_dealership.py
│   ├── static/djangoapp/style.css
│   └── templates/djangoapp/
│       ├── base.html, index.html, about.html, contact.html
│       ├── dealers.html, dealer_detail.html, add_review.html
│       └── login.html, register.html
└── .venv/                                 # local virtualenv (not submitted)
```

## How to run

```bash
cd ~/workspace/course12-capstone
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_dealership   # demo data (idempotent)
.venv/bin/python manage.py runserver 127.0.0.1:8000
# open http://127.0.0.1:8000/  — About: /about/  Contact: /contact/
# optional: .venv/bin/python manage.py createsuperuser  (for /admin/)
```

## Test command and result

Commands run 2026-11-06 in `~/workspace/course12-capstone/`:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

- `manage.py check` — **passed, no issues.** (First run failed with
  `ModuleNotFoundError: No module named 'requests'` because `requests`
  was not yet installed in the venv; fixed by
  `.venv/bin/pip install -r requirements.txt`, then check was clean.
  An intermediate run also showed one staticfiles warning W004, fixed
  by creating `djangoapp/static/`.)
- `manage.py test` — **passed: Ran 6 tests in 7.494s — OK.** Tests cover
  About page, Contact GET + POST, index/dealers list, dealer detail +
  APIs, register/login + login-gated add-review, and the models.
- `manage.py migrate` — applied all migrations (auth, admin,
  contenttypes, sessions, `djangoapp.0001_initial`) — OK.
- `manage.py seed_dealership` — "Seeded 3 dealers, 3 makes, 9 car models,
  3 reviews."

### Runserver smoke test (curl, 2026-11-06)

Server started with `runserver 127.0.0.1:8000`, then stopped after the test.

| URL | Result |
|---|---|
| `GET /` | HTTP 200, 1633 bytes, contains "Best Cars Dealership" |
| `GET /about/` | HTTP 200, contains "About Us" |
| `GET /contact/` | HTTP 200 |
| `GET /dealers/` | HTTP 200 |
| `GET /dealer/1/` | HTTP 200 |
| `GET /api/dealers/` | HTTP 200, JSON array of 3 dealers |
| `GET /api/inventory/` | HTTP 200, 9 car models |
| `GET /login/` | HTTP 200 |
| `GET /register/` | HTTP 200 |
| `GET /dealer/1/add-review/` (anonymous) | HTTP 302 (redirect to login, as designed) |
| `GET /admin/` | HTTP 302 (redirect to admin login, as designed) |

## Exactly what Mark needs next

Nothing has been submitted. For the Course 12 final peer-review
assignment in Mark, Jarif (or a follow-up task with his go-ahead) still
needs to:

1. **Publish to GitHub (not done, do not invent URLs):** push this
   project to a public GitHub repository under his account. No repo was
   created and no GitHub URLs exist yet. Note the repo will need a
   decision on what to include: this build is Django-only; the full
   original capstone also expects a React front end, a Node/Mongo
   dealers + reviews back-end service, and Kubernetes/Code Engine
   deployment, none of which exist here.
2. **Complete the Coursera checklist quizzes** (Static Pages, Back End,
   Dynamic Pages, User Management & CI/CD, Containerize) — not taken
   in this task.
3. **Submit in Mark:** paste the public GitHub repo URL (and any
   deployed app URL, if deployment is done) into the Mark peer-review
   assignment and submit; then grade peers as required.
4. **Optional, for a fuller submission:** build the React front end,
   the Node/Mongo back-end services, and the Docker/Kubernetes
   deployment (Modules 4, 5, 7 as originally specified), or confirm
   with the course requirements that this Django-only build is
   acceptable as the submitted project.
   **Update 2026-11-06:** the React front end and the Node back-end
   services are now built and integrated (`frontend/`, `services/`) —
   only the Docker/Kubernetes deployment (Module 5) is still missing,
   because Docker is not installed on this VM. See "Integration update
   (2026-11-06)" below and `RETAKE-ANSWERS.md` for the retake sheet.

## Integration update (2026-11-06) — missing pieces built, retakes prepared

Context: Coursera Modules 1–4 were submitted Nov 5, 2:01–2:04 PM PST.
M1 PASSED 80%; M2 FAILED 50% (3/6), M3 FAILED 66.66% (8/12), M4 FAILED
33.33% (2/6). Each failed module has 2 attempts left, retry every 8
hours (earliest ≈ 10:04 PM PST Nov 5 / ≈ 12:04 PM Dhaka Nov 6).
**No checklist was submitted in this task — only prepared.** The full
per-question retake sheet is `RETAKE-ANSWERS.md`.

What was added (files listed in the tree above; originals in
`~/workspace/course12-capstone-react/` and
`~/workspace/course12-capstone-services/` left untouched):
- `frontend/src/components/Register.jsx` (new) + auth-aware nav and a
  `register` route in `src/App.jsx`; `getMe()` / `postReviewJson()` /
  `registerUser()` in `src/api.js`; `/register` + `/logout` in the Vite proxy.
- `services/dealers-service/server.js`: `/fetchDealers`,
  `/fetchDealer/:id`, `/fetchDealers/:state`, `?state=` on `/dealers`.
- `djangoapp/restapis.py`: `post_review()`, `get_dealer_by_id_from_cf()`,
  `get_dealers_by_state_from_cf()`, `get_dealer_by_id()`, `get_dealers_by_state()`.
- `djangoapp/views.py`: `dealers_list` / `dealer_detail` now render proxied
  data when configured; `add_review` forwards via `post_review`; new
  `api_me` and JSON `POST /api/dealers/<id>/reviews/` (201).
- `djangoapp/urls.py`: `api/me/`. `djangoapp/tests.py`: 4 new tests (10 total).

Verification (all run 2026-11-06, real output, no fabrication):
- `manage.py check` — no issues. `manage.py test` — **Ran 10 tests in 3.213s — OK.**
- `services/test.sh` — all endpoints 200 (3 dealers, 9 models, 3 makes,
  3 reviews, `POST /reviews` 201). New aliases curled separately:
  `/fetchDealers` 200, `/fetchDealer/1` 200, `/fetchDealers/ON` 200,
  `/dealers?state=ON` 200, `/fetchDealer/99` 404.
- Full-stack E2E (services :3001/:3002 + Django :8000 with
  `DEALERS_API_URL`/`REVIEWS_API_URL` set): `/dealers/` and `/dealer/1/`
  rendered the proxied dealer; admin login 302; `/api/me/` anon `false`,
  logged-in `admin`; JSON review POST → 201 and forwarded to the reviews
  service (dealer 1 reviews 1→2 there and in the DB); React registration
  flow created + logged in user `reacttester` (302, `/api/me/` confirmed).
  Test review + test user deleted afterwards; DB back to 3 seeded reviews.
- `frontend`: `npm run build` passed (36 modules, 1.32s, JS 155.51 kB);
  `vite preview` :4173 served index 200, `/api/me/` and `/api/dealers/`
  through the proxy returned live Django JSON, `/register/` 200.
- Docker for Module 5: `docker`, `podman`, `nerdctl` all absent from this
  VM (checked 2026-11-06) — **no image built, M5 stays honestly No**.
- All test servers stopped afterwards; ports 3001/3002/4173/8000 free.

Retake outlook (per `RETAKE-ANSWERS.md`): M2 → Yes × 6 (expected 6/6),
M3 → Yes × 12 (expected 12/12), M4 → Yes × 6 (expected 6/6), provided
`frontend/` + `services/` + the Django changes are pushed to the GitHub
repo first. M5 stays No; M6 needs the Mark submission; M7 optional, not attempted.

## What is ready / still missing

- **Ready:** Django app builds, migrates, passes `check` with no
  issues, passes all 10 tests, serves every page and API endpoint above
  over local HTTP, with seeded demo data. React front end builds and
  serves live data (incl. registration page + auth nav); Node dealers +
  reviews services pass all endpoint checks incl. `/fetchDealers`
  aliases; Django proxy wiring and `post_review` verified end to end.
- **Still missing:** GitHub publication of the integrated repo, Mark
  submission, peer review, Coursera checklist retakes (M2–M4 prepared in
  `RETAKE-ANSWERS.md`, M5 still blocked), Docker image / Kubernetes /
  Code Engine deployment.
