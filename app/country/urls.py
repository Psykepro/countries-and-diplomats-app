from django.urls import path

from .views import CountryDetailView, CountryListView

urlpatterns = [
    path('', CountryListView.as_view(), name='country-list'),
    path('<iso>/', CountryDetailView.as_view(), name='country-detail'),
]
