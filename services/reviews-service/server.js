// Reviews back-end service for the IBM Course 12 capstone.
// Serves the dealer reviews the Django app proxies when REVIEWS_API_URL
// is set (see djangoapp/restapis.py: get_dealer_reviews_from_cf calls
// GET with a `dealerId` query param and expects a JSON array of reviews).
// Demo data only, in-memory — no MongoDB required.

const express = require("express");
const { reviews } = require("./data");

const app = express();
app.use(express.json());

app.get("/health", (req, res) => res.json({ status: "ok", service: "reviews" }));

// GET /reviews?dealerId=<id> — reviews for one dealer (the exact call the
// Django proxy makes). Without a query param, returns all reviews.
app.get("/reviews", (req, res) => {
  const dealerId = req.query.dealerId;
  if (dealerId === undefined) return res.json(reviews);
  res.json(reviews.filter((r) => r.dealer_id === Number(dealerId)));
});

// GET /reviews/dealer/:dealerId — same filter as a path param, convenience.
app.get("/reviews/dealer/:dealerId", (req, res) => {
  res.json(reviews.filter((r) => r.dealer_id === Number(req.params.dealerId)));
});

// POST /reviews — add a review (stored in-memory only; lost on restart).
app.post("/reviews", (req, res) => {
  const nextId = reviews.reduce((max, r) => Math.max(max, r.id), 0) + 1;
  const created = { id: nextId, ...req.body };
  reviews.push(created);
  res.status(201).json(created);
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => console.log(`reviews service listening on port ${PORT}`));
