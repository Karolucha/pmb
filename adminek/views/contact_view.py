from django.shortcuts import redirect, render
from django.views import View

from app.models import Contact


class ContactView(View):
    def post(self, request, *args, **kwargs):
        contact_data = Contact.objects.all()
        for data in contact_data:
            data.value = request.POST[data.name]
            data.save()
        return redirect('index')

    def get(self, request, *args, **kwargs):
        display_data = {}
        contact_data = Contact.objects.all()
        for data in contact_data:
            display_data[data.name] = data.value
        return render(request, 'app/contact_list.html', {
            'contacts': Contact.objects.all().order_by('id')
        })
