from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DealerReview, ContactMessage

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First name")
    last_name = forms.CharField(max_length=30, required=True, label="Last name")
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = DealerReview
        fields = ["name", "purchase", "purchase_date", "car_make", "car_model", "car_year", "review"]
        widgets = {"purchase_date": forms.DateInput(attrs={"type": "date"})}

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
