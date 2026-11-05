# Best Cars Dealership — React Front End (IBM Course 12 Capstone)

React front end for the Car Dealership Portal capstone. It calls the Django
JSON APIs of the back end in `~/workspace/course12-capstone/` (do not modify
that folder; it is read-only for this app).

## Pages

- **Dealer list** (`/`) — dealers from `GET /api/dealers/`, with search and a
  car-makes strip from `GET /api/cars/`.
- **Dealer detail** — dealer from `GET /api/dealers/<id>/`, reviews from
  `GET /api/dealers/<id>/reviews/`, and that dealer's stock from
  `GET /api/inventory/`.
- **Add a review** — posts to the Django form view
  `POST /dealer/<id>/add-review/` (the Django app exposes no JSON POST
  review endpoint). Requires a Django login in the same browser; see
  “Review submission” below.

## Run it

```bash
cd ~/workspace/course12-capstone/frontend
npm install
npm run dev        # Vite dev server on http://127.0.0.1:5173
```

The Django back end must be running on `http://127.0.0.1:8000`
(from `~/workspace/course12-capstone/`, see its SUMMARY.md). The Vite dev
server proxies `/api`, `/dealer` and `/login` to it, so API and form calls
are same-origin from the browser.

```bash
npm run build      # production build into dist/
npm run preview    # serve the production build on http://127.0.0.1:4173
```

## Configuration

Set the back-end base URL with `VITE_API_BASE_URL` (see `.env.example`).
Empty (the default) means same-origin — use the Vite proxy in dev/preview,
or serve the built files from the Django host.

## Review submission

The form first loads the Django form page to read its CSRF token, then
POSTs the review form-encoded with the Django session cookie
(`credentials: 'include'`). That only works when:

1. the user is logged in to the Django site in the same browser
   (the header links to the Django login page), and
2. the React app is served same-origin with the Django back end.

If either is missing, submission fails with a clear error message — it
never reports a fake success. See `SUMMARY.md` for the verified behaviour.
