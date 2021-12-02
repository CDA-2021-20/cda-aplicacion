from django.urls import path
from .views import CsvFormView, Charts, Tables

urlpatterns = [
    path("uploadcsv/", CsvFormView.as_view(), name="uploadcsv"),
]