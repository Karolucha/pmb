import os
from django.core.files.storage import FileSystemStorage
from adminek.views.generic_views import BaseGenericView
from django.shortcuts import redirect
from app.models import Pastor
from pmb.settings import MEDIA_ROOT


class PastorView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        object_context = model_class.objects.filter(id=id_object)[0]
        return object_context

    def post(self, request, *args, **kwargs):
        object_name = kwargs['object_name']
        self.model_class = Pastor
        if kwargs['pk'] is None:
            self.set_values(request)
            self.create(request, *args, **kwargs)
        elif request.POST.get('delete'):
            self.delete(request, *args, **kwargs)
        else:
            self.set_values(request)
            self.edit(request, *args, **kwargs)
        return redirect('detail', method='list', object_name=object_name)

    def delete(self, request, *args, **kwargs):
        pastor = Pastor.objects.filter(id=kwargs['pk'])
        if len(pastor) < 1:
            return super().delete()
        file = pastor[0].image.name
        os.remove(os.path.join(MEDIA_ROOT, file.name))
        super().delete()

    def create(self, request, *args, **kwargs):
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        pastor = Pastor(name=request.POST['name'], image=myfile.name)
        pastor.save()
        return redirect('detail', method='list', object_name='weekannouncement')

    def edit(self, request, *args, **kwargs):
        object_context = self.model_class.objects.filter(id=kwargs['pk'])[0]
        if request.FILES['image']:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(myfile.name, myfile)
            object_context.image = myfile.name
            object_context.save()
        if request.POST['name']:
            object_context.name = request.POST['name']
            object_context.save()


