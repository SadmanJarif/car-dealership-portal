// Dealers back-end service for the IBM Course 12 capstone.
// Serves the dealer / inventory data the Django app proxies when
// DEALERS_API_URL is set (see djangoapp/restapis.py: get_dealers_from_cf
// does a plain GET with no params and expects a JSON array of dealers).
// Demo data only, in-memory — no MongoDB required.

const express = require("express");
const { dealers, makes, models } = require("./data");

const app = express();
app.use(express.json());

app.get("/health", (req, res) => res.json({ status: "ok", service: "dealers" }));

// GET /dealers — all dealers (the exact call the Django proxy makes).
// Optional ?state=<state> filter (Django get_dealers_by_state_from_cf).
app.get("/dealers", (req, res) => {
  if (req.query.state) {
    return res.json(dealers.filter((d) => d.state.toLowerCase() === String(req.query.state).toLowerCase()));
  }
  res.json(dealers);
});

// IBM capstone naming aliases (same data, same shapes):
//   GET /fetchDealers            -> all dealers
//   GET /fetchDealer/:id        -> one dealer, 404 when unknown
//   GET /fetchDealers/:state    -> dealers in one state
app.get("/fetchDealers", (req, res) => res.json(dealers));
app.get("/fetchDealer/:id", (req, res) => {
  const dealer = dealers.find((d) => d.id === Number(req.params.id));
  if (!dealer) return res.status(404).json({ error: "dealer not found" });
  res.json(dealer);
});
app.get("/fetchDealers/:state", (req, res) => {
  res.json(dealers.filter((d) => d.state.toLowerCase() === req.params.state.toLowerCase()));
});

// GET /dealers/:id — one dealer, 404 when unknown.
app.get("/dealers/:id", (req, res) => {
  const dealer = dealers.find((d) => d.id === Number(req.params.id));
  if (!dealer) return res.status(404).json({ error: "dealer not found" });
  res.json(dealer);
});

// GET /dealers/:id/models — car models stocked by one dealer.
app.get("/dealers/:id/models", (req, res) => {
  const dealerId = Number(req.params.id);
  if (!dealers.some((d) => d.id === dealerId)) {
    return res.status(404).json({ error: "dealer not found" });
  }
  res.json(models.filter((m) => m.dealer_id === dealerId));
});

// GET /inventory — all car models (matches Django api_inventory shape).
app.get("/inventory", (req, res) => res.json(models));

// GET /makes — all car makes (matches Django api_cars shape).
app.get("/makes", (req, res) => res.json(makes));

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`dealers service listening on port ${PORT}`));
