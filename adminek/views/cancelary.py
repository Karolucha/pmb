from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.models import OfficeHours, DAYS_OF_WEEK


class CancelaryListView(ListView):
    model = OfficeHours


class CancelaryDetailView(DetailView):
    model = OfficeHours


class CancelaryUpdateView(UpdateView):
    model = OfficeHours
    fields = '__all__'
    success_url = reverse_lazy('cancelary')


class CancelaryCreateView(CreateView):
    model = OfficeHours
    fields = '__all__'
    success_url = reverse_lazy('cancelary')

    def form_valid(self, form):
        model = form.save(commit=False)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('demos-ui-createview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = DAYS_OF_WEEK
        return context
