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
    path("api/dealers/", views.api_dealers, name="api_dealers"),
    path("api/dealers/<int:dealer_id>/", views.api_dealer_detail, name="api_dealer_detail"),
    path("api/dealers/<int:dealer_id>/reviews/", views.api_dealer_reviews, name="api_dealer_reviews"),
    path("api/inventory/", views.api_inventory, name="api_inventory"),
    path("api/cars/", views.api_cars, name="api_cars"),
]
