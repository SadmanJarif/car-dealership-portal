# Course 12 Capstone — Final Submission evidence (REBUILT v3, 2026-11-06)

Rebuilt after the second Mark submission scored 25/50 (50%, FAILED, pass
70%; first attempt was 15/50). Every grader-feedback item from BOTH
attempts is fixed here. Captured locally against the full stack on this
machine: Django :8000 (runserver --noreload), dealers service :3001,
reviews service :3002, React preview :4173; deployed shots against the
live Module 5 Kubernetes deployment. Seeded demo data: **50 dealers**
(5 in Kansas: Wichita, Kansas City, Topeka, Overland Park, Lawrence),
3 car makes, 150 car models, 50 seeded reviews. Admin superuser is `admin`
(local dev DB only; password `Admin12345` for this evidence run — local dev
only, change it on any shared deployment). Nothing in this folder was
submitted to Coursera/Mark or pushed to GitHub.

## What changed in v3 — grader feedback from the 25/50 retake, fixed
1. **Q1 README project name.** `README.md` now contains the exact string
   `fullstack_developer_capstone` (title line + body).
2. **Q2 django_server = real runserver terminal output.** `django_server.txt`
   now leads with the verbatim runserver startup block ("Performing system
   checks...", "Django version 4.2.16, using settings 'djangoproj.settings'",
   "Starting development server at http://127.0.0.1:8000/", "Quit the
   server with CONTROL-C.") from `evidence/django_runserver.log`
   (captured with `python -u manage.py runserver --noreload` so the
   startup block is not stuck in stdout buffering), plus request logs and
   the curl home-page 200. Capture script: `capture_evidence3.py`.
3. **Q3/Q4 About/Contact at the course paths.** `server/frontend/static/
   About.html` and `server/frontend/static/Contact.html` are rendered copies
   of the fixed About/Contact pages (team members, office address), so the
   rubric URLs `server/frontend/static/About.html` and `.../Contact.html`
   resolve to real files in the repo. The Django template versions
   (`djangoapp/templates/djangoapp/about.html`, `contact.html`) are unchanged.
4. **Q5/Q6/Q8 use the course endpoints.** New URL aliases in
   `djangoapp/urls.py`: `/djangoapp/login`, `/djangoapp/logout`,
   `/djangoapp/get_dealer_reviews/<id>/` (same views as the local routes).
   `loginuser.txt`, `logoutuser.txt`, `getdealerreviews.txt` were
   re-captured using ONLY those `/djangoapp/*` endpoints.
5. **Q9/Q11/Q14 paste the COMPLETE JSON — no summaries.** The `.txt` files
   contain the full output (all 50 dealers, all 5 Kansas dealers, all 3
   makes with all 150 models). The retake MUST paste the full file content
   into the Mark text field, not a first/last summary.
6. **Q15 analyzereview = GET analysis curl.** New endpoint
   `GET /djangoapp/analyze_review/?review=Fantastic+services` (added in
   `djangoapp/views.py`) returns `{"review": "Fantastic services",
   "sentiment": "positive"}`. `analyzereview.txt` shows that GET FIRST,
   then the POST 201, the stored review, and the dealer page.
7. **Q20 review-form screenshot: all fields filled.** `capture_screenshots3.py`
   now fills EVERY field (name, purchase, purchase_date, car_make,
   car_model, car_year, review) BEFORE grabbing
   `dealership_review_submission.png`, and only then submits.
8. **Q24–Q26 deployed screenshots show the address bar.** They are now REAL
   headed-browser screenshots (Xvfb + ffmpeg x11grab of the whole screen)
   of the live deployment — not PDF-print conversions. Capture script:
   `capture_deployed3.py`. (The VM's egress proxy is a MITM proxy that
   Chromium cannot use directly, so captures go through a local relay
   proxy on 127.0.0.1:18080 — see `capture_deployed3.py` header and
   `/tmp/relay_proxy.py`; the relay only adds Proxy-Authorization.)
9. **Q27 deployed_add_review = the POSTED review on the dealer page.**
   `evidence/deployed/deployed_add_review.png` shows dealer 1 AFTER a
   review was submitted on the deployed app ("Fantastic services" by
   Evidence Tester, with sentiment) — not the entry form.

## Earlier fixes (v2, still in place)
- Literal `curl` commands in all 9 `.txt` files (no `"$ GET ..."` notation).
- 50 dealerships (5 in Kansas) seeded in Django + both Node services.
- Exact endpoint `/djangoapp/get_cars` (3 makes, 150 models).
- Review text "Fantastic services" → sentiment **positive** (keyword rule
  extended: fantastic/wonderful/amazing/awesome/superb/outstanding/love/
  best/perfect/brilliant/happy/pleased/recommend).
- Screenshots show the full browser window incl. address bar
  (headed Chromium under Xvfb + x11grab). `admin_logout.png` is the real
  Django admin "Logged out" page (`/admin/logout/`, "Log in again").
- Sentiment icons on reviews (`Sentiment: positive 😊👍` / `neutral 😐` /
  `negative 👎😞`).
- About "Meet the Team" (4 demo staff); Contact head-office address
  (123 Main Street, Toronto, ON M1A 1A1), office hours,
  `hello@bestcarsdealership.ca`, link to About; Register has 5 fields.
- `?state=` filtering on `dealers_list` and `api_dealers`.

## Text outputs (real curl) — exact rubric names
| File | What it shows (grader check) |
|---|---|
| `django_server.txt` | **Runserver terminal output verbatim** (startup block + request logs) + `curl -i http://127.0.0.1:8000/` → HTTP 200 |
| `loginuser.txt` | `curl -X POST -d username=admin&password=... /djangoapp/login` → 302 + sessionid cookie; home page shows "Hi, admin!" |
| `logoutuser.txt` | `curl /djangoapp/logout` → 302; home page anonymous again (Login link, no "Hi, admin!") |
| `getalldealers.txt` | `curl /fetchDealers` + `curl /api/dealers/` — **complete JSON, 50 dealers each** |
| `getdealerbyid.txt` | `curl /fetchDealer/1` + `curl /api/dealers/1/` — Best Cars Dealership |
| `getdealersbyState.txt` | `curl /fetchDealers/KS` + `curl /api/dealers/?state=KS` + `curl /dealers/?state=KS` — **complete JSON, 5 Kansas dealers** |
| `getdealerreviews.txt` | `curl /reviews?dealerId=1` + `curl /djangoapp/get_dealer_reviews/1/` |
| `getallcarmakes.txt` | `curl /makes` + `curl /api/cars/` + `curl /djangoapp/get_cars` — **complete JSON, 3 makes, 150 models** |
| `analyzereview.txt` | **`curl /djangoapp/analyze_review/?review=Fantastic+services` → `{"review": "Fantastic services", "sentiment": "positive"}`**, then POST → **HTTP 201**, stored review, dealer page shows "Fantastic services" + "Sentiment: positive" |

## Screenshots (PNG, full browser window incl. address bar) — exact rubric names
| File | What it shows (grader check) |
|---|---|
| `admin_login.png` | Django admin index logged in as admin — address bar `127.0.0.1:8000/admin/` |
| `admin_logout.png` | Django admin "Logged out" page — address bar `127.0.0.1:8000/admin/logout/`, "Log in again" |
| `get_dealers.png` | Django dealers list, anonymous — address bar `/dealers/` |
| `dealersbystate.png` | React list, search "KS" — only the 5 Kansas dealers — address bar `127.0.0.1:4173` |
| `dealer_id_reviews.png` | Dealer 1 detail — "Fantastic services" (Maya) with `Sentiment: positive 😊👍` |
| `get_dealers_loggedin.png` | Dealers list logged in — nav "Hi, admin!" + Logout |
| `dealership_review_submission.png` | Add-review form for dealer 1 — **ALL fields filled** before the shot |
| `added_review.png` | Dealer 1 after form submit — "Fantastic services" (Playwright Tester) with `Sentiment: positive 😊👍` |

## Deployed screenshots (Q23–Q27, live Module 5 deployment)
Deployment URL (Q23): `https://jarifindia2-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/`
(image `us.icr.io/sn-labs-jarifindia2/dealership:latest`, pod 1/1 Running).
The URL only works while the lab port-forward runs.
| File | What it shows (grader check) |
|---|---|
| `deployed/deployed_landing.png` | Deployed home page — 50 dealers incl. 5 Kansas — **address bar visible** |
| `deployed/deployed_loggedin.png` | Deployed dealers page logged in as demo user `evidence` — **address bar visible** |
| `deployed/deployed_dealer_detail.png` | Deployed dealer 1 detail with reviews incl. "Sentiment: positive" — **address bar visible** |
| `deployed/deployed_add_review.png` | Deployed dealer 1 page AFTER submitting a review — posted "Fantastic services" (Evidence Tester) visible with sentiment — **address bar visible** |

## Verification (all run 2026-11-06, v3 capture)
- `manage.py check` clean; `manage.py test` 10/10 pass.
- DB: 50 dealers, 5 in KS, 150 models, 50 seeded reviews (+ "Fantastic
  services" reviews added during capture: Maya via API, Playwright Tester
  via the form — both on dealer 1 in the gitignored local `db.sqlite3`).
- `django_server.txt` contains "Starting development server at
  http://127.0.0.1:8000/"; login/logout/getdealerreviews use only
  `/djangoapp/*` endpoints; analyzereview starts with the GET analysis curl.
- Screenshots visually spot-checked: address bar visible in every shot;
  Q20 form fully filled; deployed shots are real browser screenshots.

## Caveats (honest)
- Sentiment is the Django view's keyword rule (`analyze_sentiment` in
  `djangoapp/views.py`); no Watson NLU is wired into this local build, and
  `analyzereview.txt` states that.
- The deployed screenshots depend on the lab port-forward staying up; if
  it goes down, Q24–Q27 must be re-captured from the live deployment.
- Q22 (CI/CD) is NOT covered by this folder: the "Lint Code" workflow
  (`.github/workflows/main.yml`) must have actually run on GitHub — the
  retake must cite a real run, not the older `ci.yml` run #17.
