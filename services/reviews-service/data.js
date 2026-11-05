// Demo data only — mirrors the Django seed in
// ~/workspace/course12-capstone/djangoapp/management/commands/seed_dealership.py
// (one review per dealer, 3 total). In-memory; no database required.

const reviews = [
  { id: 1, dealer_id: 1, name: "Alex", purchase: true, purchase_date: "2024-05-01", car_make: "Toyota", car_model: "Camry", car_year: 2024, sentiment: "positive", review: "Great service and a fair price. Excellent experience overall." },
  { id: 2, dealer_id: 2, name: "Alex", purchase: true, purchase_date: "2024-05-01", car_make: "Toyota", car_model: "Camry", car_year: 2024, sentiment: "positive", review: "Great service and a fair price. Excellent experience overall." },
  { id: 3, dealer_id: 3, name: "Alex", purchase: true, purchase_date: "2024-05-01", car_make: "Toyota", car_model: "Camry", car_year: 2024, sentiment: "positive", review: "Great service and a fair price. Excellent experience overall." },
];

module.exports = { reviews };
