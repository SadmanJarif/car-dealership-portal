from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel, CarDealer, DealerReview

class Command(BaseCommand):
    help = "Seed demo dealers, makes, models and one review (local demo data only)"
    def handle(self, *args, **options):
        toyota, _ = CarMake.objects.get_or_create(name="Toyota", defaults={"description": "Japanese car maker"})
        honda, _ = CarMake.objects.get_or_create(name="Honda", defaults={"description": "Japanese car maker"})
        ford, _ = CarMake.objects.get_or_create(name="Ford", defaults={"description": "American car maker"})
        dealers = [
            {"full_name": "Best Cars Dealership", "short_name": "Best Cars", "city": "Toronto", "address": "123 Main St", "state": "ON", "zip": "M1A 1A1", "lat": 43.65, "long": -79.38},
            {"full_name": "City Auto Mall", "short_name": "City Auto", "city": "Vancouver", "address": "456 Oak Ave", "state": "BC", "zip": "V6B 1A1", "lat": 49.28, "long": -123.12},
            {"full_name": "Sunshine Motors", "short_name": "Sunshine", "city": "Austin", "address": "789 Elm Rd", "state": "TX", "zip": "78701", "lat": 30.27, "long": -97.74},
        ]
        for d in dealers:
            dealer, _ = CarDealer.objects.get_or_create(full_name=d["full_name"], defaults=d)
            CarModel.objects.get_or_create(car_make=toyota, name="Camry", dealer_id=dealer.id, defaults={"car_type": "Sedan", "year": 2024})
            CarModel.objects.get_or_create(car_make=honda, name="CR-V", dealer_id=dealer.id, defaults={"car_type": "SUV", "year": 2024})
            CarModel.objects.get_or_create(car_make=ford, name="F-150", dealer_id=dealer.id, defaults={"car_type": "SUV", "year": 2023})
            if not dealer.reviews.exists():
                DealerReview.objects.create(dealer=dealer, name="Alex", purchase=True, purchase_date="2024-05-01", car_make="Toyota", car_model="Camry", car_year=2024, sentiment="positive", review="Great service and a fair price. Excellent experience overall.")
        self.stdout.write(self.style.SUCCESS("Seeded 3 dealers, 3 makes, 9 car models, 3 reviews."))
