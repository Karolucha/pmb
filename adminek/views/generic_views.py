from django.apps import apps
from django.shortcuts import render, redirect
from django.views import View


class BaseGenericView(View):
    template_name = None
    object_name = None
    model_class = None
    context = None
    values = None

    def get_for_single(self, model_class, id_object):
        return model_class.objects.get(id=id_object)
        # context['object'] = model_object

    def get(self, request, *args, **kwargs):
        method = kwargs.get('method', 'get')
        self.object_name = kwargs['object_name']
        self.model_class = apps.get_model(app_label='app', model_name=self.object_name)
        self.context = self.model_class.get_context() if hasattr(self.model_class, 'get_context') else {}
        if kwargs['pk'] is not None:
            # model_object = model_class.objects.get(id=kwargs['pk'])
            self.context['object'] = self.get_for_single(self.model_class, kwargs['pk'])
        self.get_template_name(method)
        print('context ', self.context)
        print('render model class', self.model_class)
        return render(request, self.template_name, self.context)

    def get_template_name(self, method):

        if method == 'delete':
            post_fix = '_delete.html'
        elif method == 'list':
            self.context['object_list'] = self.model_class.objects.all()
            post_fix = '_list.html'
        else:
            post_fix = '_form.html'

        self.template_name = 'app/' + self.object_name.lower() + post_fix

    def post(self, request, *args, **kwargs):
        object_name = kwargs['object_name']
        self.model_class = apps.get_model(app_label='app', model_name=object_name)
        # fields = [field.name for field in self.model_class._meta.get_fields()]
        # values = {field: request.POST[field] for field in fields
        #           if field != 'id'}
        if kwargs['pk'] is None:
            self.set_values(request)
            self.create(request, *args, **kwargs)
            # values = {field: request.POST[field] for field in fields
            #           if field != 'id'}
            # model_object = self.model_class(**values)
            # model_object.save()
        elif request.POST.get('delete'):
            self.delete(*args, **kwargs)
        else:
            self.set_values(request)
            self.edit(request, *args, **kwargs)
            # model_object = self.model_class.objects.filter(id=kwargs['pk'])
            # values = {field: request.POST[field] for field in fields
            #           if field != 'id'}
            # model_object.update(**values)
        # template_name = 'app/' + object_name.lower() + '_list.html'
        return redirect('detail', method='list', object_name=object_name)
        # return render(request, template_name, {
        #     'object_list': model_class.objects.all()})

    def create(self, request, *args, **kwargs):
        model_object = self.model_class(**self.values)
        model_object.save()

    def edit(self, request, *args, **kwargs):
        model_object = self.model_class.objects.filter(id=kwargs['pk'])
        model_object.update(**self.values)
        
    def delete(self, *args, **kwargs):
        model_object = self.model_class.objects.get(id=kwargs['pk'])
        model_object.delete()

    def set_values(self, request):
        post_items = dict(request.POST)
        fields = [field.name for field in self.model_class._meta.get_fields()]
        self.values = {field: request.POST[field] for field in fields
                       if field != 'id' if field in post_items.keys()}
