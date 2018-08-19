from django.apps import apps
from django.shortcuts import render, redirect
from django.views import View


class BaseGenericView(View):
    template_name = None
    object_name = None
    model_class = None
    context = None
    values = None

    # def get_object(self):
    #     return self.get_for_single(self.model_class, )

    def get_for_single(self, model_class, id_object):
        return model_class.objects.get(id=id_object)

    def get(self, request, *args, **kwargs):
        method = kwargs.get('method', 'get')
        self.object_name = kwargs['object_name']
        self.model_class = apps.get_model(app_label='app', model_name=self.object_name)
        self.context = self.model_class.get_context() if hasattr(self.model_class, 'get_context') else {}
        if kwargs['pk'] is not None:
            self.context['object'] = self.get_for_single(self.model_class, kwargs['pk'])
        if method == 'list':
            self.context['object_list'] = self.get_for_list()
        self.get_template_name(method)
        print('render model class', self.model_class)
        return render(request, self.template_name, self.context)

    def get_for_list(self):
        return self.model_class.objects.all()

    def get_template_name(self, method):
        if method == 'delete':
            post_fix = '_delete.html'
        elif method == 'list':
            post_fix = '_list.html'
        else:
            post_fix = '_form.html'

        self.template_name = 'app/' + self.object_name.lower() + post_fix

    def post(self, request, *args, **kwargs):
        object_name = kwargs['object_name']
        self.model_class = apps.get_model(app_label='app', model_name=object_name)
        if kwargs['pk'] is None:
            self.set_values(request)
            self.create(request, *args, **kwargs)
        elif request.POST.get('delete'):
            self.delete(*args, **kwargs)
        else:
            self.set_values(request)
            self.edit(request, *args, **kwargs)
        return redirect('detail', method='list', object_name=object_name)

    def create(self, request, *args, **kwargs):
        model_object = self.model_class(**self.values)
        model_object.save()

    def edit(self, request, *args, **kwargs):
        model_object = self.model_class.objects.filter(id=kwargs['pk'])
        model_object.update(**self.values)
        
    def delete(self, *args, **kwargs):
        model_object = self.model_class.objects.get(id=kwargs['pk'])
        print('modelobject ', model_object.name)
        model_object.delete()

    def set_values(self, request):
        post_items = dict(request.POST)
        fields = [field.name for field in self.model_class._meta.get_fields()]
        self.values = {field: request.POST[field] for field in fields
                       if field != 'id' if field in post_items.keys()}
