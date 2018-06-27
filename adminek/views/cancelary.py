from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.models import OfficeHours


class CancelaryListView(ListView):
    model = OfficeHours


class CancelaryDetailView(DetailView):
    model = OfficeHours


class CancelaryUpdateView(UpdateView):
    model = OfficeHours
    fields = 'day', 'start', 'end'


class CancelaryCreateView(CreateView):
    model = OfficeHours
    fields = 'day', 'start', 'end'

