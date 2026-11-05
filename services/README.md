# Course 12 Capstone — Node.js Back-End Services (local only)

Two small Node.js/Express services for the IBM Course 12 capstone (Car
Dealership Portal). They are the external dealers + reviews back-end the
Django app proxies when `DEALERS_API_URL` / `REVIEWS_API_URL` are set
(see `../djangoapp/restapis.py`). **Local only — not
submitted to Coursera/Mark, not published to GitHub.**

Data is demo-only and in-memory (no MongoDB needed): 3 dealers, 3 car
makes, 9 car models, 3 reviews — the same seed as the Django app
(`course12-capstone/djangoapp/management/commands/seed_dealership.py`).

## Services

| Service | Folder | Default port | Start |
|---|---|---|---|
| Dealers | `dealers-service/` | 3001 | `npm start` in that folder |
| Reviews | `reviews-service/` | 3002 | `npm start` in that folder |

Or start both at once from this folder: `./start-all.sh` (stops with
`./stop-all.sh`, or Ctrl-C the script).

## Endpoints

Dealers service (port 3001):

- `GET /health` → `{"status":"ok","service":"dealers"}`
- `GET /dealers` → all 3 dealers (the exact call the Django proxy makes)
- `GET /dealers/:id` → one dealer, 404 when unknown
- `GET /dealers/:id/models` → car models stocked by that dealer
- `GET /inventory` → all 9 car models
- `GET /makes` → all 3 car makes

Reviews service (port 3002):

- `GET /health` → `{"status":"ok","service":"reviews"}`
- `GET /reviews?dealerId=<id>` → reviews for one dealer (the exact call
  the Django proxy makes — note the `dealerId` query param)
- `GET /reviews` → all 3 reviews
- `GET /reviews/dealer/:dealerId` → same filter as a path param
- `POST /reviews` → add a review (in-memory only, lost on restart)

## Wiring the Django app to these services

```bash
DEALERS_API_URL=http://127.0.0.1:3001/dealers \
REVIEWS_API_URL=http://127.0.0.1:3002/reviews \
  ../.venv/bin/python ../manage.py runserver 127.0.0.1:8000
```

With those set, the Django `/dealers/` page proxies the dealers service
and dealer reviews come from the reviews service; without them it falls
back to the local SQLite database (same data either way).

## Verify

`./test.sh` starts both services, curls every endpoint, and prints the
results (also recorded in `SUMMARY.md`).
