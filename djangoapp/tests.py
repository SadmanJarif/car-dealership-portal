from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel, CarDealer, DealerReview


class DealershipTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.make = CarMake.objects.create(name="Toyota", description="Japanese car maker")
        self.model = CarModel.objects.create(car_make=self.make, name="Camry", dealer_id=1, car_type="Sedan", year=2024)
        self.dealer = CarDealer.objects.create(
            full_name="Best Cars Dealership",
            city="Toronto",
            address="123 Main St",
            state="ON",
            zip="M1A 1A1",
            short_name="Best Cars")
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

    def test_api_me_anonymous_and_logged_in(self):
        r = self.client.get("/api/me/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"authenticated": False, "username": None})
        self.client.login(username="tester", password="testpass123")
        r = self.client.get("/api/me/")
        self.assertEqual(r.json(), {"authenticated": True, "username": "tester"})

    def test_api_post_review_json(self):
        # Anonymous JSON review is refused (403), as the React app expects.
        r = self.client.post(f"/api/dealers/{self.dealer.id}/reviews/",
                             data='{"name": "anon", "review": "Great!"}',
                             content_type="application/json")
        self.assertEqual(r.status_code, 403)
        self.client.login(username="tester", password="testpass123")
        import json as _json
        r = self.client.post(f"/api/dealers/{self.dealer.id}/reviews/",
                             data=_json.dumps({"name": "tester", "review": "Great service!",
                                               "purchase": False, "car_make": "Toyota",
                                               "car_model": "Camry", "car_year": 2024}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(DealerReview.objects.count(), 1)
        self.assertEqual(r.json()["sentiment"], "positive")

    def test_post_review_helper_posts_to_external_service(self):
        # restapis.post_review() POSTs to the reviews service URL; verified
        # against a stubbed post_request so no network is needed.
        from unittest import mock
        from . import restapis
        with mock.patch.object(restapis, "post_request",
                               return_value={"id": 99, "dealer_id": 1}) as m:
            result = restapis.post_review("http://127.0.0.1:3002/reviews",
                                          {"dealer_id": 1, "review": "Great!"})
        m.assert_called_once_with("http://127.0.0.1:3002/reviews",
                                  {"dealer_id": 1, "review": "Great!"})
        self.assertEqual(result["id"], 99)

    def test_proxy_helpers_use_external_service_when_configured(self):
        # get_dealer_by_id / get_dealers_by_state call the dealers service.
        from unittest import mock
        from django.test import override_settings
        from . import restapis
        with override_settings(DEALERS_API_URL="http://127.0.0.1:3001/dealers"):
            with mock.patch.object(restapis, "get_request",
                                   return_value={"id": 1, "full_name": "Best Cars"}) as m:
                self.assertEqual(restapis.get_dealer_by_id(1)["full_name"], "Best Cars")
                m.assert_called_with("http://127.0.0.1:3001/dealers/1")
            with mock.patch.object(restapis, "get_request",
                                   return_value=[{"id": 1}]) as m:
                self.assertEqual(restapis.get_dealers_by_state("ON"), [{"id": 1}])
                m.assert_called_with("http://127.0.0.1:3001/dealers", state="ON")
