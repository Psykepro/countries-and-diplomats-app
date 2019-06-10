import requests

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .models import Country
from .choices import REGION_CHOICES
from .external_api_providers import (RestCountriesProvider as RProvider,
                                     CountriesIOProvider as CProvider)


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'country_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        countries = self.queryset
        paginator = Paginator(countries, self.paginate_by)
        region_selected = self.request.GET.get('region', '')
        iso_selected = self.request.GET.get('iso', '')
        page = self.request.GET.get('page')

        try:
            countries = paginator.page(page)
        except PageNotAnInteger:
            countries = paginator.page(1)
        except EmptyPage:
            countries = paginator.page(paginator.num_pages)

        context.update({'list_countries': countries,
                        'region_choices': REGION_CHOICES,
                        'iso_choices': CProvider.get_iso2_codes(),
                        'region_selected': region_selected,
                        'iso_selected': iso_selected,
                        })
        return context

    def _get_filters(self):
        filters = {}

        for filter_key in RProvider.SUPPORTED_COUNTRY_FILTERS:
            filter_val = self.request.GET.get(filter_key)
            if filter_val:
                filters.update({filter_key: filter_val})

        return filters

    def get_queryset(self):
        filters = self._get_filters()
        self.queryset = RProvider.get_filtered_countries_as_json(**filters)
        return self.queryset


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country
    template_name = 'country_detail.html'

    def get_object(self, queryset=None):
        response = requests.get(RProvider
                                .get_country_url_by_iso(self.kwargs['iso']))
        response_data = response.json()
        item = Country(**response_data)
        return item
