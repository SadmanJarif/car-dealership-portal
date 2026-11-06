#!/usr/bin/env python3
"""Generate the 50-dealer seed for Django (seed_dealership.py) and the Node
dealers service (services/dealers-service/data.js) from ONE dealer list so
both stores always agree. Also generates services/reviews-service/data.js
(one seeded review per dealer). Run from ~/workspace/course12-capstone."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "workspace" / "course12-capstone"
# If run from inside the repo, ROOT is the repo itself.
if (Path(__file__).resolve().parent / "manage.py").exists():
    ROOT = Path(__file__).resolve().parent
if not (ROOT / "manage.py").exists():
    raise SystemExit(f"repo root not found, tried {ROOT}")

DEALERS = [
    ("Best Cars Dealership", "Best Cars", "Toronto", "123 Main St", "ON", "M1A 1A1", 43.65, -79.38),
    ("City Auto Mall", "City Auto", "Vancouver", "456 Oak Ave", "BC", "V6B 1A1", 49.28, -123.12),
    ("Sunshine Motors", "Sunshine", "Austin", "789 Elm Rd", "TX", "78701", 30.27, -97.74),
    ("Sunflower Auto Plaza", "Sunflower", "Wichita", "100 E Douglas Ave", "KS", "67202", 37.69, -97.34),
    ("Prairie State Motors", "Prairie State", "Kansas City", "200 Minnesota Ave", "KS", "66101", 39.11, -94.63),
    ("Capital City Cars", "Capital City", "Topeka", "300 SW 10th Ave", "KS", "66603", 39.05, -95.68),
    ("Overland Park Auto Mall", "Overland Park", "Overland Park", "400 W 95th St", "KS", "66212", 38.98, -94.67),
    ("Jayhawk Auto Center", "Jayhawk", "Lawrence", "500 Massachusetts St", "KS", "66044", 38.97, -95.24),
    ("Golden State Motors", "Golden State", "Los Angeles", "600 S Grand Ave", "CA", "90012", 34.05, -118.25),
    ("Bay Area Auto Hub", "Bay Area", "San Francisco", "700 Market St", "CA", "94103", 37.77, -122.42),
    ("Silicon Valley Cars", "Silicon Valley", "San Jose", "800 W Santa Clara St", "CA", "95113", 37.34, -121.89),
    ("Palm City Motors", "Palm City", "San Diego", "900 Broadway", "CA", "92101", 32.72, -117.16),
    ("Lone Star Auto", "Lone Star", "Houston", "1000 Main St", "TX", "77002", 29.76, -95.37),
    ("Alamo City Motors", "Alamo City", "San Antonio", "1100 Commerce St", "TX", "78205", 29.42, -98.49),
    ("Big D Dealership", "Big D", "Dallas", "1200 Elm St", "TX", "75201", 32.78, -96.80),
    ("River City Auto", "River City", "Fort Worth", "1300 Houston St", "TX", "76102", 32.76, -97.33),
    ("Empire State Motors", "Empire State", "New York", "1400 5th Ave", "NY", "10001", 40.75, -73.99),
    ("Upstate Auto Mall", "Upstate", "Buffalo", "1500 Main St", "NY", "14201", 42.89, -78.88),
    ("Hudson Valley Cars", "Hudson Valley", "Albany", "1600 State St", "NY", "12207", 42.65, -73.76),
    ("Sunshine State Auto", "Sunshine State", "Miami", "1700 Biscayne Blvd", "FL", "33101", 25.77, -80.19),
    ("Orange Blossom Motors", "Orange Blossom", "Orlando", "1800 Orange Ave", "FL", "32801", 28.54, -81.38),
    ("Gulf Coast Cars", "Gulf Coast", "Tampa", "1900 Franklin St", "FL", "33602", 27.95, -82.46),
    ("Windy City Auto", "Windy City", "Chicago", "2000 Wacker Dr", "IL", "60601", 41.88, -87.63),
    ("Prairie Auto Plaza", "Prairie Auto", "Springfield", "2100 Monroe St", "IL", "62701", 39.78, -89.65),
    ("Rockford Motors", "Rockford", "Rockford", "2200 State St", "IL", "61101", 42.27, -89.09),
    ("Buckeye Auto Mall", "Buckeye", "Columbus", "2300 High St", "OH", "43215", 39.96, -83.00),
    ("Queen City Motors", "Queen City", "Cincinnati", "2400 Vine St", "OH", "45202", 39.10, -84.51),
    ("Lake Erie Cars", "Lake Erie", "Cleveland", "2500 Euclid Ave", "OH", "44113", 41.50, -81.69),
    ("Liberty Auto Center", "Liberty", "Philadelphia", "2600 Market St", "PA", "19103", 39.95, -75.17),
    ("Steel City Motors", "Steel City", "Pittsburgh", "2700 Liberty Ave", "PA", "15222", 40.44, -80.00),
    ("Peach State Auto", "Peach State", "Atlanta", "2800 Peachtree St", "GA", "30303", 33.75, -84.39),
    ("Savannah Motors", "Savannah", "Savannah", "2900 Bull St", "GA", "31401", 32.08, -81.09),
    ("Desert Sun Auto", "Desert Sun", "Phoenix", "3000 Washington St", "AZ", "85004", 33.45, -112.07),
    ("Canyon State Cars", "Canyon State", "Tucson", "3100 Congress St", "AZ", "85701", 32.22, -110.97),
    ("Emerald City Motors", "Emerald City", "Seattle", "3200 Pine St", "WA", "98101", 47.61, -122.33),
    ("Lilac City Auto", "Lilac City", "Spokane", "3300 Riverside Ave", "WA", "99201", 47.66, -117.43),
    ("Motor City Auto", "Motor City", "Detroit", "3400 Woodward Ave", "MI", "48201", 42.33, -83.05),
    ("Grand Rapids Motors", "Grand Rapids", "Grand Rapids", "3500 Monroe Ave", "MI", "49503", 42.96, -85.67),
    ("Tar Heel Auto", "Tar Heel", "Charlotte", "3600 Tryon St", "NC", "28202", 35.23, -80.84),
    ("Research Triangle Cars", "Research Triangle", "Raleigh", "3700 Fayetteville St", "NC", "27601", 35.78, -78.64),
    ("Mile High Motors", "Mile High", "Denver", "3800 16th St", "CO", "80202", 39.74, -104.99),
    ("Rocky Mountain Auto", "Rocky Mountain", "Colorado Springs", "3900 Tejon St", "CO", "80903", 38.83, -104.82),
    ("Twin Cities Auto", "Twin Cities", "Minneapolis", "4000 Hennepin Ave", "MN", "55401", 44.98, -93.27),
    ("North Star Motors", "North Star", "St. Paul", "4100 Wabasha St", "MN", "55101", 44.95, -93.09),
    ("Rose City Cars", "Rose City", "Portland", "4200 Burnside St", "OR", "97204", 45.52, -122.68),
    ("Silver State Auto", "Silver State", "Las Vegas", "4300 Las Vegas Blvd", "NV", "89101", 36.17, -115.14),
    ("Beehive State Motors", "Beehive State", "Salt Lake City", "4400 State St", "UT", "84101", 40.76, -111.89),
    ("Gateway City Auto", "Gateway City", "St. Louis", "4500 Olive St", "MO", "63101", 38.63, -90.20),
    ("Badger State Motors", "Badger State", "Milwaukee", "4600 Wisconsin Ave", "WI", "53202", 43.04, -87.91),
    ("Hoosier Auto Mall", "Hoosier", "Indianapolis", "4700 Meridian St", "IN", "46204", 39.77, -86.16),
]
assert len(DEALERS) == 50, f"expected 50 dealers, got {len(DEALERS)}"
assert sum(1 for d in DEALERS if d[4] == "KS") == 5, "expected 5 Kansas dealers"

def py_dict(d):
    full, short, city, addr, state, zipc, lat, lng = d
    return (f'{{"full_name": "{full}", "short_name": "{short}", "city": "{city}", '
            f'"address": "{addr}", "state": "{state}", "zip": "{zipc}", "lat": {lat}, "long": {lng}}}')

# --- Django seed ---
lines = [
    'from django.core.management.base import BaseCommand',
    'from djangoapp.models import CarMake, CarModel, CarDealer, DealerReview',
    '',
    '',
    'class Command(BaseCommand):',
    '    help = "Seed demo dealers, makes, models and reviews (local demo data only): 50 dealers"',
    '    def handle(self, *args, **options):',
    '        toyota, _ = CarMake.objects.get_or_create(name="Toyota", defaults={"description": "Japanese car maker"})',
    '        honda, _ = CarMake.objects.get_or_create(name="Honda", defaults={"description": "Japanese car maker"})',
    '        ford, _ = CarMake.objects.get_or_create(name="Ford", defaults={"description": "American car maker"})',
    '        dealers = [',
]
for d in DEALERS:
    lines.append(f'            {py_dict(d)},')
lines += [
    '        ]',
    '        for d in dealers:',
    '            dealer, _ = CarDealer.objects.get_or_create(full_name=d["full_name"], defaults=d)',
    '            CarModel.objects.get_or_create(car_make=toyota, name="Camry", dealer_id=dealer.id, defaults={"car_type": "Sedan", "year": 2024})',
    '            CarModel.objects.get_or_create(car_make=honda, name="CR-V", dealer_id=dealer.id, defaults={"car_type": "SUV", "year": 2024})',
    '            CarModel.objects.get_or_create(car_make=ford, name="F-150", dealer_id=dealer.id, defaults={"car_type": "SUV", "year": 2023})',
    '            if not dealer.reviews.exists():',
    '                DealerReview.objects.create(dealer=dealer, name="Alex", purchase=True, purchase_date="2024-05-01", car_make="Toyota", car_model="Camry", car_year=2024, sentiment="positive", review="Great service and a fair price. Excellent experience overall.")',
    '        self.stdout.write(self.style.SUCCESS("Seeded 50 dealers, 3 makes, 150 car models, 50 reviews."))',
    '',
]
seed_path = ROOT / "djangoapp" / "management" / "commands" / "seed_dealership.py"
seed_path.write_text("\n".join(lines))
print(f"wrote {seed_path} ({len(DEALERS)} dealers)")

# --- Node dealers data.js ---
js_dealers = []
for i, d in enumerate(DEALERS, start=1):
    full, short, city, addr, state, zipc, lat, lng = d
    js_dealers.append(f'  {{ id: {i}, full_name: "{full}", short_name: "{short}", city: "{city}", address: "{addr}", state: "{state}", zip: "{zipc}", lat: {lat}, long: {lng} }},')
js_models = []
mid = 1
for i in range(1, 51):
    for name, ctype, year, make in [("Camry", "Sedan", 2024, "Toyota"), ("CR-V", "SUV", 2024, "Honda"), ("F-150", "SUV", 2023, "Ford")]:
        js_models.append(f'  {{ id: {mid}, name: "{name}", car_type: "{ctype}", year: {year}, dealer_id: {i}, car_make: "{make}" }},')
        mid += 1
data_js = "\n".join([
    "// Demo data only — mirrors the Django seed in",
    "// ~/workspace/course12-capstone/djangoapp/management/commands/seed_dealership.py",
    "// (50 dealers, 3 car makes, 150 car models). In-memory; no database required.",
    "",
    "const dealers = [",
    *js_dealers,
    "];",
    "",
    "const makes = [",
    '  { id: 1, name: "Toyota", description: "Japanese car maker" },',
    '  { id: 2, name: "Honda", description: "Japanese car maker" },',
    '  { id: 3, name: "Ford", description: "American car maker" },',
    "];",
    "",
    "// One Camry (Toyota, Sedan, 2024), one CR-V (Honda, SUV, 2024) and one",
    "// F-150 (Ford, SUV, 2023) per dealer — 150 models total, matching the seed.",
    "const models = [",
    *js_models,
    "];",
    "",
    "module.exports = { dealers, makes, models };",
    "",
])
dealers_js = ROOT / "services" / "dealers-service" / "data.js"
dealers_js.write_text(data_js)
print(f"wrote {dealers_js}")

# --- Node reviews data.js (one seeded review per dealer) ---
js_reviews = []
for i in range(1, 51):
    js_reviews.append(f'  {{ id: {i}, dealer_id: {i}, name: "Alex", purchase: true, purchase_date: "2024-05-01", car_make: "Toyota", car_model: "Camry", car_year: 2024, sentiment: "positive", review: "Great service and a fair price. Excellent experience overall." }},')
reviews_js = "\n".join([
    "// Demo data only — mirrors the Django seed in",
    "// ~/workspace/course12-capstone/djangoapp/management/commands/seed_dealership.py",
    "// (one review per dealer, 50 total). In-memory; no database required.",
    "",
    "const reviews = [",
    *js_reviews,
    "];",
    "",
    "module.exports = { reviews };",
    "",
])
reviews_path = ROOT / "services" / "reviews-service" / "data.js"
reviews_path.write_text(reviews_js)
print(f"wrote {reviews_path}")
print("done — 50 dealers, 5 in KS")
