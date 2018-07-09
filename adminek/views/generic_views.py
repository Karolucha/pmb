from django.apps import apps
from django.shortcuts import render
from django.views import View


class BaseGenericView(View):

    def get(self, request, *args, **kwargs):
        object_name = kwargs['object_name']
        model_class = apps.get_model(app_label='app', model_name=object_name)
        context = model_class.get_context()
        template_name = 'app/' + object_name.lower() + '_form.html'
        if kwargs['pk'] is not None:
            article = model_class.objects.get(id=kwargs['pk'])
            context['object'] = article
        print('context ', context)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        object_name = kwargs['object_name']
        model_class = apps.get_model(app_label='app', model_name=object_name)
        fields = [field.name for field in model_class._meta.get_fields()]
        if kwargs['pk'] is None:
            values = {field: request.POST[field] for field in fields
                      if field != 'id'}
            model_object = model_class(**values)
        elif request.POST.get('delete'):
            model_object = model_class.objects.get(id=kwargs['pk'])
            model_object.delete()
        else:
            model_object = model_class.objects.filter(id=kwargs['pk'])
            values = {field: request.POST[field] for field in fields
                      if field != 'id'}
            model_object.update(**values)
        model_object.save()
        template_name = 'app/' + object_name.lower() + '_list.html'
        return render(request, template_name, {
            'object_list': model_class.objects.all()})
