import os

from django.core.files.storage import FileSystemStorage

from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse
from app.models import WeekAnnouncement, Announcement, Pastor
from docx import Document
from django.core.files.base import ContentFile

class PastorView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        object_context = model_class.objects.filter(id=id_object)[0]
        print('pastor ', object_context.image.url)

        return object_context

    # def get(self, request, *args, **kwargs):
    #     method = kwargs.get('method', 'get')
    #     if method == 'download':
    #         object_context = WeekAnnouncement.objects.filter(id=kwargs['pk']).prefetch_related('announcement_set')[0]
    #         return document.download_docx()
    #     else:
    #         return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print('create in pastor_View', request.POST)
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        pastor = Pastor(name=request.POST['name'], image=myfile.name)
        pastor.save()
        # return render(request, 'core/simple_upload.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
        return redirect('detail', method='list', object_name='weekannouncement')

    def edit(self, request, *args, **kwargs):
        object_context = self.model_class.objects.filter(id=kwargs['pk'])[0]
        if request.FILES['image']:
            myfile = request.FILES['image']
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)
            object_context.image = myfile.name
            print('the name is ', myfile.name)
            object_context.save()
        if request.POST['name']:
            object_context.name = request.POST['name']
            object_context.save()
        # print('uploaded_file_url', uploaded_file_url)


