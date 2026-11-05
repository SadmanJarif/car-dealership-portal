// Demo data only — mirrors the Django seed in
// ~/workspace/course12-capstone/djangoapp/management/commands/seed_dealership.py
// (3 dealers, 3 car makes, 9 car models). In-memory; no database required.

const dealers = [
  { id: 1, full_name: "Best Cars Dealership", short_name: "Best Cars", city: "Toronto", address: "123 Main St", state: "ON", zip: "M1A 1A1", lat: 43.65, long: -79.38 },
  { id: 2, full_name: "City Auto Mall", short_name: "City Auto", city: "Vancouver", address: "456 Oak Ave", state: "BC", zip: "V6B 1A1", lat: 49.28, long: -123.12 },
  { id: 3, full_name: "Sunshine Motors", short_name: "Sunshine", city: "Austin", address: "789 Elm Rd", state: "TX", zip: "78701", lat: 30.27, long: -97.74 },
];

const makes = [
  { id: 1, name: "Toyota", description: "Japanese car maker" },
  { id: 2, name: "Honda", description: "Japanese car maker" },
  { id: 3, name: "Ford", description: "American car maker" },
];

// One Camry (Toyota, Sedan, 2024), one CR-V (Honda, SUV, 2024) and one
// F-150 (Ford, SUV, 2023) per dealer — 9 models total, matching the seed.
const models = [
  { id: 1, name: "Camry", car_type: "Sedan", year: 2024, dealer_id: 1, car_make: "Toyota" },
  { id: 2, name: "CR-V", car_type: "SUV", year: 2024, dealer_id: 1, car_make: "Honda" },
  { id: 3, name: "F-150", car_type: "SUV", year: 2023, dealer_id: 1, car_make: "Ford" },
  { id: 4, name: "Camry", car_type: "Sedan", year: 2024, dealer_id: 2, car_make: "Toyota" },
  { id: 5, name: "CR-V", car_type: "SUV", year: 2024, dealer_id: 2, car_make: "Honda" },
  { id: 6, name: "F-150", car_type: "SUV", year: 2023, dealer_id: 2, car_make: "Ford" },
  { id: 7, name: "Camry", car_type: "Sedan", year: 2024, dealer_id: 3, car_make: "Toyota" },
  { id: 8, name: "CR-V", car_type: "SUV", year: 2024, dealer_id: 3, car_make: "Honda" },
  { id: 9, name: "F-150", car_type: "SUV", year: 2023, dealer_id: 3, car_make: "Ford" },
];

module.exports = { dealers, makes, models };
