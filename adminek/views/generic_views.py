from django.apps import apps
from django.shortcuts import render, redirect
from django.views import View


class BaseGenericView(View):

    def get(self, request, *args, **kwargs):
        method = kwargs.get('method', 'get')
        object_name = kwargs['object_name']
        model_class = apps.get_model(app_label='app', model_name=object_name)
        context = model_class.get_context() if hasattr(model_class, 'get_context') else {}
        if kwargs['pk'] is not None:
            article = model_class.objects.get(id=kwargs['pk'])
            context['object'] = article
        print('context ', context)
        if method == 'delete':
            post_fix = '_delete.html'
        elif method == 'list':
            context['object_list'] = model_class.objects.all()
            post_fix = '_list.html'
        else:
            post_fix = '_form.html'
        template_name = 'app/' + object_name.lower() + post_fix
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        print("MISIU")
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
