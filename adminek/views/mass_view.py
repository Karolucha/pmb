from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import MassSchema, Hour


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
        schema = MassSchema(season_start=request.POST['season_start'],
                            season_end=request.POST['season_end'])
        # schema.save()
        anothers = dict(request.POST)
        print(anothers)
        messes = {}
        for name, value in anothers.items():
            if name.startswith('n-'):
                if name.startswith('n-hour-'):
                    row_number = name.split('-')[-1]
                    if row_number in messes.keys():
                        messes[row_number]['hour'] = value
                    else:
                        messes[row_number] = {
                            'hour': value
                        }
                if name.startswith('n-church-'):
                    row_number = name.split('-')[-1]
                    if row_number in messes.keys():
                        messes[row_number]['church'] = value
                    else:
                        messes[row_number] = {
                            'church': value
                        }
        print('meser ', messes)
        for number, mass in messes.items():
            hour = Hour(church=mass['church'][0], hour=mass['hour'][0], mass=schema)
            # hour.save()
        return redirect('detail', method='list', object_name='massschema')
