from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CarMake, CarModel, CarDealer, DealerReview
from .forms import RegistrationForm, ReviewForm, ContactForm
from . import restapis

def index(request):
    dealers = CarDealer.objects.all()
    return render(request, "djangoapp/index.html", {"dealers": dealers})

def about(request):
    return render(request, "djangoapp/about.html")

def contact(request):
    sent = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            sent = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, "djangoapp/contact.html", {"form": form, "sent": sent})

def dealers_list(request):
    # Back-end proxy first (external Node/Mongo service when configured),
    # otherwise local database — same data either way.
    proxied = restapis.get_dealers()
    dealers = CarDealer.objects.all()
    return render(request, "djangoapp/dealers.html", {"dealers": dealers, "proxied": proxied})

def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    reviews = dealer.reviews.all().order_by("-created_at")
    return render(request, "djangoapp/dealer_detail.html", {"dealer": dealer, "reviews": reviews})

@login_required
def add_review(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dealer = dealer
            review.sentiment = "positive" if "great" in review.review.lower() or "excellent" in review.review.lower() else "neutral"
            review.save()
            return redirect("dealer_detail", dealer_id=dealer.id)
    else:
        form = ReviewForm(initial={"name": request.user.username})
    return render(request, "djangoapp/add_review.html", {"dealer": dealer, "form": form})

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "djangoapp/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "djangoapp/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("index")

# ---- JSON back-end services (also used by the React/dynamic front end) ----
def api_dealers(request):
    dealers = list(CarDealer.objects.values("id", "full_name", "city", "address", "state", "zip", "lat", "long", "short_name"))
    return JsonResponse(dealers, safe=False)

def api_dealer_detail(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    data = {"id": dealer.id, "full_name": dealer.full_name, "city": dealer.city,
            "address": dealer.address, "state": dealer.state, "zip": dealer.zip}
    return JsonResponse(data)

def api_dealer_reviews(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    reviews = list(dealer.reviews.values("name", "purchase", "purchase_date", "car_make", "car_model", "car_year", "sentiment", "review"))
    return JsonResponse(reviews, safe=False)

def api_inventory(request):
    cars = list(CarModel.objects.select_related("car_make").values("id", "name", "car_type", "year", "dealer_id", "car_make__name"))
    return JsonResponse(cars, safe=False)

def api_cars(request):
    makes = list(CarMake.objects.values("id", "name", "description"))
    return JsonResponse(makes, safe=False)
