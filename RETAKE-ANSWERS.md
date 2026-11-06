# Course 12 Capstone — Coursera Checklist Retake Answer Sheet

**Status: PREPARED ONLY. Nothing in this file has been submitted to
Coursera or Mark.**
Repo: https://github.com/SadmanJarif/car-dealership-portal — public, 18 commits,
verified live 2026-11-06: the integrated `frontend/` and `services/` folders
are in the repo. No push needed before the retakes.

**First submission:** Modules 1–4 submitted Nov 5, 2:01–2:04 PM PST.
**Retakes:** each failed module shows "2 attempts remaining", retry every
8 hours — earliest retake ≈ 10:04 PM PST Nov 5 (≈ 12:04 PM Dhaka Nov 6).
Check Coursera's own countdown before submitting; the time above is
computed from the submission time, not read from Coursera.

**How this sheet was made:** the exact Coursera question wordings were
not available locally, so items below are identified by the topic the
browser report gave for each lost point, in the order the answers were
submitted. Do not reword an answer on the day — match each topic to the
question that asks it, and if a question's wording does not match any
topic here, answer it truthfully from the code, not from this sheet.

## Module 1 — Static Pages: PASSED 80% (4/5) — no retake needed
Submitted answers: No / Yes / Yes / Yes / Yes. Only point lost was Q1
(app built locally, not forked from the IBM template) — honestly No, and
unchanged. Nothing new to do.

## Module 2 — User Management: FAILED 50% (3/6) → retake answers below
Submitted answers: No / No / Yes / Yes / No / Yes.
Lost points: superuser, nav-bar login/logout/signup, React registration page.

| # | Topic (lost point) | Was | Now | Evidence (all verified locally 2026-11-06) |
|---|---|---|---|---|
| 1 | Superuser created | No | **Yes** | `admin` superuser exists in the local DB (`is_superuser=True`, verified in the Django shell; admin login returns 302 to `/` and `/api/me/` returns `{"authenticated": true, "username": "admin"}`). **Caveat:** `db.sqlite3` is gitignored, so the superuser is NOT in the GitHub repo — on any fresh checkout run `python manage.py createsuperuser` first. |
| 2 | Nav bar has login / logout / signup links | No | **Yes** | Django `base.html` already had Login/Register (logged out) and Logout + "Hi, username" (logged in). The React nav now does the same: `frontend/src/App.jsx` reads `GET /api/me/` and shows Login + Register when anonymous, username + Logout when logged in. Verified via `/api/me/` (anon → `authenticated: false`; logged in → `admin`) and the built bundle. |
| 3 | (was Yes) | Yes | Yes | Unchanged. |
| 4 | (was Yes) | Yes | Yes | Unchanged. |
| 5 | Registration page in React | No | **Yes** | New `frontend/src/components/Register.jsx`: username/email/password form posting to Django `POST /register/` (CSRF token from the form page, same pattern as the review form). Verified end to end with curl: new user `reacttester` created, 302 to `/`, `/api/me/` returned `{"authenticated": true, "username": "reacttester"}` (test user deleted afterwards). |
| 6 | (was Yes) | Yes | Yes | Unchanged. |

**Module 2 retake answers: Yes / Yes / Yes / Yes / Yes / Yes → expected 6/6 (100%).**

## Module 3 — Back End Services: FAILED 66.66% (8/12) → retake answers below
Submitted answers: No / No / No / Yes / Yes / Yes / Yes / Yes / No / Yes / Yes / Yes.
Lost points (in submitted order Q1, Q2, Q3, Q9): three Express/Mongo
fetchDealers endpoints, and post_review.

| # | Topic (lost point) | Was | Now | Evidence (all verified locally 2026-11-06) |
|---|---|---|---|---|
| Q1 | fetchDealers endpoint (all dealers) | No | **Yes** | `services/dealers-service/server.js` now serves `GET /fetchDealers` (plus the existing `GET /dealers`): curl → 200, 3 dealers. Django `restapis.get_dealers_from_cf()` calls it, and `dealers_list` now actually renders the proxied list (was fetched and discarded). Live check: `GET /dealers/` with `DEALERS_API_URL` set returned "Best Cars Dealership". |
| Q2 | fetchDealer by id endpoint | No | **Yes** | `GET /fetchDealer/<id>` → 200 for id 1, 404 for id 99 (verified). Django `restapis.get_dealer_by_id_from_cf()` + `get_dealer_by_id()` added; `dealer_detail` now uses the proxied dealer when configured. Unit-tested with a mocked `get_request`. |
| Q3 | fetchDealers by state endpoint | No | **Yes** | `GET /fetchDealers/<state>` → 200, returns the 1 dealer in ON (verified); `GET /dealers?state=ON` → 200 likewise. Django `restapis.get_dealers_by_state_from_cf()` + `get_dealers_by_state()` added (unit-tested). |
| Q4–Q8 | (were Yes) | Yes | Yes | Unchanged (models, JSON APIs, proxy helpers). |
| Q9 | post_review | No | **Yes** | `restapis.post_review(url, json_payload)` added — POSTs to the reviews service. `POST /api/dealers/<id>/reviews/` added (login + CSRF, 201). Verified end to end: JSON review POST → 201 `{"id": 5, ...}`, saved in Django DB (dealer 1 reviews 1→2) AND forwarded to the reviews service (dealer 1 reviews there 1→2, incl. "E2E Tester"). The Django form `add_review` view also calls `post_review` when `REVIEWS_API_URL` is set. Form-POST fallback still works. Test review deleted afterwards; DB back to 3 reviews. |
| Q10–Q12 | (were Yes) | Yes | Yes | Unchanged. |

**Module 3 retake answers: Yes × 12 → expected 12/12 (100%).**

## Module 4 — Dynamic Pages: FAILED 33.33% (2/6) → retake answers below
Submitted answers: No / No / No / No / Yes / Yes.
Lost points: all four React-component questions. The two Yes points were
the Django add-review submission page and the review updating after posting.

| # | Topic (lost point) | Was | Now | Evidence (all verified locally 2026-11-06) |
|---|---|---|---|---|
| Q1 | Dealer list page in React | No | **Yes** | `frontend/src/components/DealerList.jsx` — cards + search + car-makes strip, calls `GET /api/dealers/`. It existed before but lived outside the capstone repo, so it was honestly No at submission. It is now integrated at `course12-capstone/frontend/` (see "What changed" below). |
| Q2 | Dealer detail page in React | No | **Yes** | `frontend/src/components/DealerDetail.jsx` — detail + reviews + stock, calls `GET /api/dealers/<id>/`, `.../reviews/`, `/api/inventory/`. Same integration note as Q1. |
| Q3 | Add-review page in React | No | **Yes** | `frontend/src/components/ReviewForm.jsx` — now posts JSON to `POST /api/dealers/<id>/reviews/` (201 verified live) with the form-POST fallback. Same integration note as Q1. |
| Q4 | React front end wired to the back end (dynamic pages render live data) | No | **Yes** | `npm run build` in `frontend/` → 36 modules, built in 1.32s; `vite preview` on :4173 served index (200), `/api/me/` and `/api/dealers/` through the proxy returned live Django JSON, `/register/` through the proxy returned 200. Bundle contains the Register page ("Create an account"). |
| Q5–Q6 | (were Yes) | Yes | Yes | Unchanged (Django add-review page; review shows after posting — re-verified live in the Module 3 test above). |

**Module 4 retake answers: Yes × 6 → expected 6/6 (100%).**

## What changed in the repo (integration, 2026-11-06)
- `frontend/` — the React app from `~/workspace/course12-capstone-react/`
  (copied, `node_modules`/`dist` excluded), plus new `src/components/Register.jsx`,
  auth-aware nav + register route in `src/App.jsx`, `getMe()` / `postReviewJson()` /
  `registerUser()` in `src/api.js`, and `/register` + `/logout` added to the Vite proxy.
- `services/` — the Node services from `~/workspace/course12-capstone-services/`
  (copied, `node_modules`/logs excluded), plus `/fetchDealers`,
  `/fetchDealer/:id`, `/fetchDealers/:state` and `?state=` on the dealers service.
- `djangoapp/restapis.py` — added `post_review()`, `get_dealer_by_id_from_cf()`,
  `get_dealers_by_state_from_cf()`, and `get_dealer_by_id()` / `get_dealers_by_state()` wrappers.
- `djangoapp/views.py` — `dealers_list` / `dealer_detail` now render the proxied
  data when configured (previously fetched and discarded); `add_review` forwards to
  `post_review`; new `api_me` (`GET /api/me/`) and JSON review POST in `api_dealer_reviews`.
- `djangoapp/urls.py` — added `api/me/`.
- `djangoapp/tests.py` — 4 new tests (api_me, JSON review POST incl. anon 403,
  post_review helper, proxy by-id/by-state). **10/10 tests pass** (`manage.py test`, 3.2s).
- `.gitignore` — added `frontend/node_modules/`, `frontend/dist/`, `services/*/node_modules/`, `services/*.log`.
- Originals in `~/workspace/course12-capstone-react/` and
  `~/workspace/course12-capstone-services/` were left untouched; the copies
  under `course12-capstone/` are now the canonical ones to push.

## Verification log (2026-11-06, all local, real output)
- `manage.py check` — no issues. `manage.py test` — **Ran 10 tests, OK**.
- `services/test.sh` — all endpoints 200 (dealers 3, models 9, makes 3, reviews 3,
  `POST /reviews` 201); new aliases curled separately: `/fetchDealers` 200,
  `/fetchDealer/1` 200, `/fetchDealers/ON` 200 (1 dealer), `/dealers?state=ON` 200,
  `/fetchDealer/99` 404.
- Full-stack E2E (services :3001/:3002 + Django :8000 with both env vars set):
  `/dealers/` and `/dealer/1/` rendered the proxied dealer; admin login 302;
  `/api/me/` anon `false` / logged-in `admin`; JSON review POST 201 and forwarded
  to the reviews service; React registration flow created + logged in `reacttester`.
  Test review and test user deleted afterwards; DB back to 3 seeded reviews.
- `frontend`: `npm run build` passed (36 modules, 1.32s, JS 155.51 kB);
  `vite preview` :4173 served index 200 with live proxy data. Bundle contains
  "Create an account" / "Register".
- All test servers stopped afterwards; ports 3001/3002/4173/8000 free.

## Module 5 — CI/CD, Containerize & Deploy to Kubernetes: STILL BLOCKED (No)
- **Docker is not installed on this VM** — `docker`, `podman`, `nerdctl` all
  absent (`which` + `/usr/bin/*docker*` + `/usr/bin/*podman*` all empty), so
  **no Docker image was built**. Do not attest to it.
- `Dockerfile` exists as a file only, never built. `.github/workflows/ci.yml`
  exists as a file only — it has never run (no repo push has happened from
  this machine, and the workflow only runs on push/PR). It is set up to run
  `manage.py check` + `manage.py test` on ubuntu-latest, so a push would
  trigger a real CI run — but that run has not happened yet.
- Nothing is deployed to Kubernetes or IBM Code Engine.
- What M5 needs next: a machine/CI with Docker (or the IBM Skills Network
  lab) to `docker build`, push the image, run the CI workflow, and deploy.
  The retake answers for M5 stay **No** until that is actually done.

## Module 6 — Share Your Project (peer review): NOT SUBMITTED
Requires the public GitHub repo URL + Mark submission + grading peers.
The repo exists with 33 files, but `frontend/` + `services/` + the new
Django changes are not pushed yet. Push first, then submit in Mark.

## Module 7 — Enhancement (optional): NOT ATTEMPTED
Car-inventory back-end service exists (`GET /api/inventory/`, 9 models)
and the React front end now exists too, but no optional enhancement lab
was claimed or submitted.

## Before the retakes (checklist for the parent agent / browser window)
1. Push `~/workspace/course12-capstone/` to
   https://github.com/SadmanJarif/car-dealership-portal (includes new
   `frontend/`, `services/`, `RETAKE-ANSWERS.md`, updated Django code).
   Verify on the repo page that `frontend/src/components/Register.jsx`
   and `services/dealers-service/server.js` (with `/fetchDealers`) are present.
2. Wait for Coursera's 8-hour retry window (earliest ≈ 10:04 PM PST Nov 5 /
   ≈ 12:04 PM Dhaka Nov 6 — confirm the countdown on Coursera).
3. Submit M2, M3, M4 with the answers in this sheet, one module at a time,
   and record the new scores. If any question's wording does not match a
   topic here, answer truthfully from the code.
4. Do NOT submit M5 — it is still honestly No.
