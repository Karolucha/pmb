from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect


class MassSchemaView(BaseGenericView):

    def get_for_single(self, model_class, id_object):

        object_context = model_class.objects.filter(id=id_object).prefetch_related('hour_set')[0]
        print('zbior', object_context.hour_set)
        for hour in object_context.hour_set.all():
            print('hour', hour.church)
        print(object_context.season_start)
        print(object_context.season_end)
        return {
            'schema': object_context,
            'hours': object_context.hour_set.all()
        }

    def post(self, request, *args, **kwargs):
        print('time to save')

        return redirect('detail', method='list', object_name='massschema')