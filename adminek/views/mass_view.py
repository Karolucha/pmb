from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import MassSchema, Hour


class MassSchemaView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):

        object_context = model_class.objects.filter(id=id_object).prefetch_related('hour_set')[0]
        print('zbior', object_context.hour_set)
        hours_set = []
        for hour in object_context.hour_set.all().order_by('hour'):
            hour.is_mb = hour.church =='mb'
            hours_set.append(hour)
            # print(hour.church, hour.is_mb, hour.hour)
        print(object_context.season_end)
        return {
            'schema': object_context,
            'hours': hours_set
        }

    def create(self, request, *args, **kwargs):
        print('time to save')
        schema = MassSchema(season_start=request.POST['season_start'],
                            season_end=request.POST['season_end'])
        schema.save()
        self.add_new_messes(request, schema)

        return redirect('detail', method='list', object_name='massschema')

    def edit(self, request, *args, **kwargs):
        anothers = dict(request.POST)
        schema = MassSchema.objects.get(id=kwargs['pk'])
        self.add_new_messes(request, schema)
        self.messes = {}

        for name, value in anothers.items():
            print('items edited', name, value)
            if name.startswith('hour-'):
                self.add_new_mass_property(name, value, 'hour')
            if name.startswith('church-'):
                self.add_new_mass_property(name, value, 'church')
            if name == 'deletions':
                for hour_element_id in value:
                    hour_id = hour_element_id.split('-')[-1]
                    hour = Hour.objects.get(id=hour_id)
                    hour.delete()

        for hour_row_id, mass in self.messes.items():
            hour_id = hour_row_id.split('-')[-1]
            print(hour_id)
            hour = Hour.objects.get(id=hour_id)
            hour.church = mass['church'][0]
            hour.hour = mass['hour'][0]
            print(hour.hour, hour.church)
            hour.save()
        schema.season_start = request.POST['season_start']
        schema.season_end = request.POST['season_end']
        schema.save()

    def add_new_messes(self, request, schema):
        anothers = dict(request.POST)
        print(anothers)
        self.group_messes(anothers)
        print('meser ', self.messes)
        for number, mass in self.messes.items():
            hour = Hour(church=mass['church'][0], hour=mass['hour'][0], mass=schema)
            print('hour', hour.church)
            hour.save()

    def group_messes(self, anothers):
        self.messes = {}
        for name, value in anothers.items():
            if name.startswith('n-'):
                if name.startswith('n-hour-'):
                    self.add_new_mass_property(name, value, 'hour')
                if name.startswith('n-church-'):
                    self.add_new_mass_property(name, value, 'church')

    def add_new_mass_property(self, name, value, prop):
        row_number = name.split('-')[-1]
        if row_number in self.messes.keys():
            self.messes[row_number][prop] = value
        else:
            self.messes[row_number] = {
                prop: value
            }
