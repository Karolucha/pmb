import os
from PIL import Image

from django.core.files.storage import FileSystemStorage

from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse
from app.models import WeekAnnouncement, Announcement, Galery, ImageWithCaption
from pmb.settings import MEDIA_ROOT


class GaleryView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        object_context = model_class.objects.filter(id=id_object).prefetch_related('imagewithcaption_set')[0]
        print('object_context', object_context.date)
        # images = []
        # for msg in object_context.imagewithcaption_set.all().order_by('id'):
        #     images.append(msg.url)
        #     print(msg.url)
        images = object_context.imagewithcaption_set.all().order_by('id')
        return {
            'galery': object_context,
            'images': images,
            'size': len(list(images)),
            'images_numbers': [{
                                   'idx': i+1, 'image':img} for i, img in enumerate(list(images))]
        }

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
                print('name',myfile.name)
                names = myfile.name.split('.')
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                announcement = ImageWithCaption(galery=schema,
                                                image=myfile.name,
                                                image_all=myfile.name)
                announcement.save()
                # im1 = Image.open(os.path.join(MEDIA_ROOT, myfile.name))
                # width = 350
                # height = 150
                # im2 = im1.resize((width, height), Image.NEAREST)
                # print('names', names, os.path.join(MEDIA_ROOT,names[0]+'.thumbnail.' + names[1]))
                # im2.save(os.path.join(MEDIA_ROOT,names[0]+'.thumbnail.' + names[1]))
                # image_all = ImageWithCaption(galery=schema,
                #                                 image=myfile.name)
                # image_all.save()


