from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview, ContactMessage
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(CarDealer)
admin.site.register(DealerReview)
admin.site.register(ContactMessage)
