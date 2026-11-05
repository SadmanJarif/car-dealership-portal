from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel, CarDealer, DealerReview

class DealershipTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.make = CarMake.objects.create(name="Toyota", description="Japanese car maker")
        self.model = CarModel.objects.create(car_make=self.make, name="Camry", dealer_id=1, car_type="Sedan", year=2024)
        self.dealer = CarDealer.objects.create(full_name="Best Cars Dealership", city="Toronto", address="123 Main St", state="ON", zip="M1A 1A1", short_name="Best Cars")
        User.objects.create_user(username="tester", password="testpass123")

    def test_about_page(self):
        self.assertEqual(self.client.get("/about/").status_code, 200)

    def test_contact_page_and_post(self):
        self.assertEqual(self.client.get("/contact/").status_code, 200)
        r = self.client.post("/contact/", {"name": "Jarif", "email": "jarif@example.com", "message": "Hello"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Thank you")

    def test_index_and_dealers_list(self):
        self.assertContains(self.client.get("/"), "Best Cars")
        self.assertContains(self.client.get("/dealers/"), "Best Cars")

    def test_dealer_detail_and_api(self):
        self.assertEqual(self.client.get(f"/dealer/{self.dealer.id}/").status_code, 200)
        self.assertEqual(self.client.get("/api/dealers/").status_code, 200)
        self.assertEqual(self.client.get(f"/api/dealers/{self.dealer.id}/reviews/").status_code, 200)
        self.assertEqual(self.client.get("/api/inventory/").status_code, 200)
        self.assertEqual(self.client.get("/api/cars/").status_code, 200)

    def test_register_login_and_add_review_requires_login(self):
        self.assertEqual(self.client.get(f"/dealer/{self.dealer.id}/add-review/").status_code, 302)
        self.client.login(username="tester", password="testpass123")
        r = self.client.post(f"/dealer/{self.dealer.id}/add-review/", {
            "name": "tester", "purchase": "on", "purchase_date": "2024-05-01",
            "car_make": "Toyota", "car_model": "Camry", "car_year": 2024,
            "review": "Great service, excellent experience."})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(DealerReview.objects.count(), 1)

    def test_models(self):
        self.assertEqual(str(self.make), "Toyota")
        self.assertEqual(CarModel.objects.count(), 1)
