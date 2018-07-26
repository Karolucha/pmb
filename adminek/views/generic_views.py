from django.apps import apps
from django.shortcuts import render, redirect
from django.views import View


class BaseGenericView(View):

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
        print('context ', self.context)
        self.get_template_name(method)
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
        model_class = apps.get_model(app_label='app', model_name=object_name)
        fields = [field.name for field in model_class._meta.get_fields()]
        if kwargs['pk'] is None:
            values = {field: request.POST[field] for field in fields
                      if field != 'id'}
            model_object = model_class(**values)
            model_object.save()
        elif request.POST.get('delete'):
            model_object = model_class.objects.get(id=kwargs['pk'])
            model_object.delete()
            # model_object.save()
        else:
            model_object = model_class.objects.filter(id=kwargs['pk'])
            values = {field: request.POST[field] for field in fields
                      if field != 'id'}
            model_object.update(**values)

        template_name = 'app/' + object_name.lower() + '_list.html'
        return redirect('detail', method='list', object_name=object_name)
        # return render(request, template_name, {
        #     'object_list': model_class.objects.all()})
