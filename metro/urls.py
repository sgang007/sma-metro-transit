from django.urls import path
from .views import calculate_fare, CsvUploader

urlpatterns = [
    path('calculate-fare/', calculate_fare, name='calculate-fare'),
    path('', CsvUploader.as_view(), name='csv-uploader')
]