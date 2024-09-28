from django.urls import path
from .views import calculate_fare

urlpatterns = [
    path('calculate-fare/', calculate_fare, name='calculate-fare'),
]