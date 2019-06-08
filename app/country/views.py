import requests

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from core.models import Country
from .utilities import get_country_url_by_iso, get_all_countries_url


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'country/country_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        list_countries = self.get_queryset()
        paginator = Paginator(list_countries, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            countries = paginator.page(page)
        except PageNotAnInteger:
            countries = paginator.page(1)
        except EmptyPage:
            countries = paginator.page(paginator.num_pages)

        context['list_countries'] = countries
        return context

    def get_queryset(self):
        response = requests.get(get_all_countries_url())
        response_data = response.json()
        return response_data


class CountryDetailView(LoginRequiredMixin, DetailView):

    model = Country
    template_name = 'country/country_detail.html'

    def get_object(self, queryset=None):
        response = requests.get(get_country_url_by_iso(self.kwargs['iso']))
        response_data = response.json()
        item = Country(**response_data)
        return item
