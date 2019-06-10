from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.urls import reverse_lazy

from .models import Diplomat
from .choices import PATH_CHOICES

from country.external_api_providers import CountriesIOProvider as CProvider


class DiplomatListView(LoginRequiredMixin, ListView):
    model = Diplomat
    template_name = 'diplomat_list.html'
    paginate_by = 5
    context_object_name = 'list_diplomats'
    queryset = Diplomat.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DiplomatListView, self).get_context_data(**kwargs)
        path_selected = self.request.GET.get('path', '')
        iso_selected = self.request.GET.get('iso', '')
        diplomats = self.queryset
        paginator = Paginator(diplomats, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            diplomats = paginator.page(page)
        except PageNotAnInteger:
            diplomats = paginator.page(1)
        except EmptyPage:
            diplomats = paginator.page(paginator.num_pages)

        context.update({'list_diplomats': diplomats,
                        'path_choices': PATH_CHOICES,
                        'iso_choices': CProvider.get_iso2_choices(),
                        'path_selected': path_selected,
                        'iso_selected': iso_selected,
                        })
        return context

    def get_queryset(self):
        name_filter = self.request.GET.get('name', '')
        path_filter = self.request.GET.get('path', '')
        iso_filter = self.request.GET.get('iso', '')

        if path_filter != '':
            self.queryset = self.queryset.filter(path=path_filter)
        if iso_filter != '':
            self.queryset = self.queryset.filter(country_iso=iso_filter)
        if name_filter != '':
            self.queryset = [d for d in self.queryset
                             if name_filter in d.full_name]

        return self.queryset


class DiplomatDetailView(LoginRequiredMixin, DetailView):
    model = Diplomat
    template_name = 'diplomat_detail.html'


class DiplomatCreateView(LoginRequiredMixin, CreateView):
    model = Diplomat
    template_name = 'diplomat_form.html'
    fields = ['first_name', 'last_name', 'email',
              'phone', 'age', 'path', 'country_iso']
    success_url = reverse_lazy('diplomat-list')


class DiplomatUpdateView(LoginRequiredMixin, UpdateView):
    model = Diplomat
    template_name = 'diplomat_form.html'
    fields = ['first_name', 'last_name', 'email',
              'phone', 'age', 'path', 'country_iso']
    success_url = reverse_lazy('diplomat-list')


class DiplomatDelete(LoginRequiredMixin, DeleteView):
    model = Diplomat
    success_url = reverse_lazy('diplomat-list')
    template_name = 'diplomat_delete.html'
