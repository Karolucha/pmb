import os

from django.core.files.storage import FileSystemStorage

from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse
from app.models import WeekAnnouncement, Announcement, Galery, ImageWithCaption


class GaleryView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        object_context = model_class.objects.filter(id=id_object).prefetch_related('imagewithcaption_set')[0]
        print('object_context', object_context.date)
        # images = []
        # for msg in object_context.imagewithcaption_set.all().order_by('id'):
        #     images.append(msg.url)
        #     print(msg.url)
        return {
            'galery': object_context,
            'images': object_context.imagewithcaption_set.all().order_by('id')
        }

    # def get(self, request, *args, **kwargs):
    #     method = kwargs.get('method', 'get')
    #     if method == 'download':
    #         object_context = WeekAnnouncement.objects.filter(id=kwargs['pk']).prefetch_related('announcement_set')[0]
    #         return document.download_docx()
    #     else:
    #         return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print('time to save', dict(request.POST).keys())
        schema = Galery(
            title=request.POST['title'], description=request.POST['description'])
        schema.save()
        self.add_new_announcements(request, schema)

        return redirect('detail', method='list', object_name='weekannouncement')

    def edit(self, request, *args, **kwargs):
        anothers = dict(request.FILES)
        print(anothers)
        schema = Galery.objects.get(id=kwargs['pk'])
        schema.title = request.POST['title']
        schema.description = request.POST['description']
        schema.save()
        self.add_new_announcements(request, schema)
        self.messes = {}

        for name, value in anothers.items():
            # if name.startswith('old-'):
            #     row_number = name.split('-')[-1]
            #     announcement = Announcement.objects.get(id=row_number)
            #     announcement.content = value[0]
            #     announcement.save()
            if name == 'deletions':
                for hour_element_id in value:
                    hour_id = hour_element_id.split('-')[-1]
                    hour = ImageWithCaption.objects.get(id=hour_id)
                    hour.delete()
        schema.save()

    def add_new_announcements(self, request, schema):
        anothers = dict(request.FILES)
        print(anothers)
        for name, value in anothers.items():
            print('what a name ', name, name.startswith('n-a-'))
            if name.startswith('n-a-'):
                myfile = request.FILES[name]
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                announcement = ImageWithCaption(galery=schema,
                                                image=myfile.name)
                announcement.save()


