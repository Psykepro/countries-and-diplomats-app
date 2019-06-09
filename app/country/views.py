import requests

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .models import Country
from .utilities import RestCountriesUtilities as RUtility


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'country_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        countries = self.queryset
        paginator = Paginator(countries, self.paginate_by)

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
        query = self.request.GET.get('name')
        filters = {'name': query} if query else {}
        response_data = RUtility.get_filtered_countries_as_json(**filters)
        if isinstance(response_data, dict):
            self.queryset = []
        else:
            self.queryset = response_data
        return self.queryset


class CountryDetailView(LoginRequiredMixin, DetailView):

    model = Country
    template_name = 'country_detail.html'

    def get_object(self, queryset=None):
        response = requests.get(RUtility
                                .get_country_url_by_iso(self.kwargs['iso']))
        response_data = response.json()
        item = Country(**response_data)
        return item
