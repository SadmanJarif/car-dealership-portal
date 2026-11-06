from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dealers/", views.dealers_list, name="dealers"),
    path("dealer/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("dealer/<int:dealer_id>/add-review/", views.add_review, name="add_review"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("api/me/", views.api_me, name="api_me"),
    path("api/dealers/", views.api_dealers, name="api_dealers"),
    path("api/dealers/<int:dealer_id>/", views.api_dealer_detail, name="api_dealer_detail"),
    path("api/dealers/<int:dealer_id>/reviews/", views.api_dealer_reviews, name="api_dealer_reviews"),
    path("api/inventory/", views.api_inventory, name="api_inventory"),
    path("api/cars/", views.api_cars, name="api_cars"),
    path("djangoapp/get_cars", views.get_cars, name="get_cars"),
    # Course-rubric aliases under /djangoapp/ (same views as the local routes)
    path("djangoapp/login", views.login_view, name="djangoapp_login"),
    path("djangoapp/logout", views.logout_view, name="djangoapp_logout"),
    path("djangoapp/get_dealer_reviews/<int:dealer_id>/", views.api_dealer_reviews, name="djangoapp_get_dealer_reviews"),
    path("djangoapp/analyze_review/", views.analyze_review, name="djangoapp_analyze_review"),
]
