from datetime import datetime
from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import MassSchema, Hour, MassSchemaRows


class MassSchemaView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        # self.get_schema()
        object_context = model_class.objects.filter(id=id_object).prefetch_related('hour_set')[0]
        print('SCHEMAT DLA NIEDZIELI? ', object_context.sunday)
        hours_set = []
        for hour in object_context.hour_set.all().order_by('hour'):
            hour.is_mb = hour.church == 'mb'
            hours_set.append(hour)
        return {
            'schema': object_context,
            'hours': hours_set
        }

    def create(self, request, *args, **kwargs):
        print('time to save')
        anothers = dict(request.POST)
        schema = MassSchema(season_start=request.POST['season_start'],
                            season_end=request.POST['season_end'],
                            sunday='sunday' in anothers.keys()
                            )
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
        schema.sunday = 'sunday' in anothers.keys()
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

    def delete(self, *args, **kwargs):
        mass_schema = MassSchema.objects.filter(id=kwargs['pk']).prefetch_related('hour_set')[0]
        for mass in mass_schema.hour_set.all():
            mass.delete()

        mass_schema.delete()

class MassSchemaIssue():

    def get_schema(self):
        print('get schema')
        now = datetime.now().date()
        closest_sunday = None
        MassSchemaRows.objects.all().delete()

        schema = MassSchema.objects.filter(
            season_start__lt=now, season_end__gt=now).prefetch_related('hour_set')
        if len(schema) > 0:
            print('schema!')
            self.save_for_schema(schema, True)
            self.save_for_schema(schema, False)

    def save_for_schema(self, schema, is_sunday):

        others = schema.filter(sunday=is_sunday)
        print('save for schema ', others)
        if others:
            self.save_for_church(schema, is_sunday, others, 'mb')
            self.save_for_church(schema, is_sunday, others, 'f')

    def save_for_church(self, schema, is_sunday, others, church):
        print('now is_sunday', is_sunday)
        masses_mb = [mass.hour.strftime('%H:%M') for mass in others[0].hour_set.filter(church=church).order_by('hour')]
        print(masses_mb)
        row_schema = MassSchemaRows(is_sunday=is_sunday, church=church,
                                    hours=', '.join(masses_mb))
        row_schema.save()