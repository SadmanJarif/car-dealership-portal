from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
from .forms import RegistrationForm, ReviewForm, ContactForm
from . import restapis

POSITIVE_WORDS = ("great", "excellent", "fantastic", "wonderful", "amazing",
                  "awesome", "superb", "outstanding", "love", "loved", "best",
                  "perfect", "brilliant", "happy", "pleased", "recommend")
NEGATIVE_WORDS = ("terrible", "awful", "horrible", "worst", "bad", "poor",
                  "disappointing", "disappointed", "rude", "slow", "broken")

def analyze_sentiment(text):
    """Keyword sentiment analysis for a review (local build; no Watson NLU
    wired in). Positive words -> 'positive', negative words -> 'negative',
    otherwise 'neutral'. 'Fantastic services' -> positive."""
    low = (text or "").lower()
    if any(w in low for w in POSITIVE_WORDS):
        return "positive"
    if any(w in low for w in NEGATIVE_WORDS):
        return "negative"
    return "neutral"

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
    # otherwise local database — same data either way. The proxied list is
    # now actually rendered, not discarded.
    # ?state=<state> filters to dealers in one state (get_dealers_by_state).
    state = request.GET.get("state")
    proxied = restapis.get_dealers()
    if proxied is not None:
        dealers = proxied
        if state:
            dealers = [d for d in dealers
                       if str(d.get("state", "")).lower() == state.lower()]
    else:
        dealers = CarDealer.objects.all()
        if state:
            dealers = dealers.filter(state__iexact=state)
    return render(request, "djangoapp/dealers.html", {"dealers": dealers, "proxied": proxied})

def dealer_detail(request, dealer_id):
    db_dealer = get_object_or_404(CarDealer, pk=dealer_id)
    dealer = db_dealer
    # Prefer the external service for the dealer + reviews when configured.
    proxied_dealer = restapis.get_dealer_by_id(dealer_id)
    if proxied_dealer is not None:
        dealer = proxied_dealer
    proxied_reviews = restapis.get_dealer_reviews(dealer_id)
    if proxied_reviews is not None:
        reviews = proxied_reviews
    else:
        reviews = db_dealer.reviews.all().order_by("-created_at")
    return render(request, "djangoapp/dealer_detail.html", {"dealer": dealer, "reviews": reviews})

@login_required
def add_review(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dealer = dealer
            review.sentiment = analyze_sentiment(review.review)
            review.save()
            # Also post the review to the external reviews back-end when
            # configured (restapis.post_review); the local save above is
            # the fallback and always happens, so a down service loses nothing.
            if settings.REVIEWS_API_URL:
                restapis.post_review(settings.REVIEWS_API_URL, {
                    "dealer_id": dealer.id,
                    "name": review.name,
                    "purchase": review.purchase,
                    "purchase_date": str(review.purchase_date) if review.purchase_date else "",
                    "car_make": review.car_make,
                    "car_model": review.car_model,
                    "car_year": review.car_year,
                    "sentiment": review.sentiment,
                    "review": review.review,
                })
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
def api_me(request):
    # Lets the React front end show Login/Register vs username/Logout.
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "username": request.user.username})
    return JsonResponse({"authenticated": False, "username": None})

def api_dealers(request):
    # ?state=<state> filters to dealers in one state (get_dealers_by_state).
    qs = CarDealer.objects.all()
    state = request.GET.get("state")
    if state:
        qs = qs.filter(state__iexact=state)
    dealers = list(qs.values("id", "full_name", "city", "address", "state", "zip", "lat", "long", "short_name"))
    return JsonResponse(dealers, safe=False)

def api_dealer_detail(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    data = {"id": dealer.id, "full_name": dealer.full_name, "city": dealer.city,
            "address": dealer.address, "state": dealer.state, "zip": dealer.zip}
    return JsonResponse(data)

def api_dealer_reviews(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)
    if request.method == "POST":
        # JSON review submission (used by the React ReviewForm via
        # restapis.post_review semantics). Login + CSRF required.
        if not request.user.is_authenticated:
            return JsonResponse({"error": "login required"}, status=403)
        try:
            data = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid JSON"}, status=400)
        # Normalise optional fields the React form sends empty.
        data.setdefault("purchase", False)
        if not data.get("purchase_date"):
            data["purchase_date"] = None
        if not data.get("car_year"):
            data["car_year"] = 2024
        form = ReviewForm(data)
        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)
        review = form.save(commit=False)
        review.dealer = dealer
        review.sentiment = analyze_sentiment(review.review)
        review.save()
        if settings.REVIEWS_API_URL:
            restapis.post_review(settings.REVIEWS_API_URL, {
                "dealer_id": dealer.id,
                "name": review.name,
                "purchase": review.purchase,
                "purchase_date": str(review.purchase_date) if review.purchase_date else "",
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
                "sentiment": review.sentiment,
                "review": review.review,
            })
        return JsonResponse({"id": review.id, "dealer_id": dealer.id, "name": review.name,
                             "sentiment": review.sentiment, "review": review.review}, status=201)
    reviews = list(dealer.reviews.values("name", "purchase", "purchase_date", "car_make", "car_model", "car_year", "sentiment", "review"))
    return JsonResponse(reviews, safe=False)

def api_inventory(request):
    cars = list(CarModel.objects.select_related("car_make").values("id", "name", "car_type", "year", "dealer_id", "car_make__name"))
    return JsonResponse(cars, safe=False)

def api_cars(request):
    makes = list(CarMake.objects.values("id", "name", "description"))
    return JsonResponse(makes, safe=False)

def analyze_review(request):
    # GET sentiment analysis of a review text, e.g.
    # /djangoapp/analyze_review/?review=Fantastic+services
    # Returns {"review": "...", "sentiment": "positive"}.
    # Same keyword rule as analyze_sentiment() in this local build
    # (no Watson NLU wired in).
    text = request.GET.get("review") or request.GET.get("text") or ""
    return JsonResponse({"review": text, "sentiment": analyze_sentiment(text)})

def get_cars(request):
    # Exact endpoint the IBM capstone rubric calls: /djangoapp/get_cars
    # Returns all car makes with their models (the full inventory).
    cars = []
    for make in CarMake.objects.all():
        cars.append({
            "id": make.id,
            "name": make.name,
            "description": make.description,
            "models": list(make.models.values("id", "name", "car_type", "year", "dealer_id")),
        })
    return JsonResponse({"car_makes": cars, "count": len(cars)}, safe=False)
