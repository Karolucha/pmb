import os
from PIL import Image

from django.core.files.storage import FileSystemStorage

from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect
from django.core.files import File
from app.models import Galery, ImageWithCaption


class GaleryView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        object_context = model_class.objects.filter(id=id_object).prefetch_related('imagewithcaption_set')[0]
        images = object_context.imagewithcaption_set.all().order_by('id')
        return {
            'galery': object_context,
            'images': images,
        }

    def create(self, request, *args, **kwargs):
        schema = Galery(
            title=request.POST['title'], description=request.POST['description'])
        schema.save()
        self.add_new_images(request, schema)
        return redirect('detail', method='list', object_name='weekannouncement')

    def edit(self, request, *args, **kwargs):
        anothers = dict(request.POST)
        schema = Galery.objects.get(id=kwargs['pk'])
        schema.title = request.POST['title']
        schema.description = request.POST['description']
        schema.save()
        self.add_new_images(request, schema)

        for name, value in anothers.items():
            if name == 'deletions':
                for img_attr_id in value:
                    img_id = img_attr_id.split('-')[-1]
                    hour = ImageWithCaption.objects.get(id=img_id)
                    hour.delete()
        schema.save()

    def add_new_images(self, request, schema):
        uploaded_files = dict(request.FILES)
        for name, value in uploaded_files.items():
            if name.startswith('n-a-'):
                if isinstance(value, list):
                    for uploaded in value:
                        self.save_image(request, uploaded, schema)
                else:
                    myfile = request.FILES[name]
                    self.save_image(request, myfile, schema)

    def save_image(self, request, image_file, gallery):
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_with_caption = ImageWithCaption(galery=gallery,
                                                  image=image_file.name)
            image_with_caption.save()


