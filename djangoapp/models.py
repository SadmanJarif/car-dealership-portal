from django.db import models
from django.contrib.auth.models import User

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    CAR_TYPES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon")]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField(default=1)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(default=2024)
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

class CarDealer(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200, default="")
    state = models.CharField(max_length=100, default="")
    zip = models.CharField(max_length=20, default="")
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    short_name = models.CharField(max_length=100, default="")
    full_name = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.full_name or self.name

class DealerReview(models.Model):
    dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, default="")
    car_model = models.CharField(max_length=100, default="")
    car_year = models.IntegerField(default=2024)
    sentiment = models.CharField(max_length=20, default="neutral")
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review by {self.name} for {self.dealer}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Contact from {self.name} <{self.email}>"
