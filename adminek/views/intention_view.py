from datetime import datetime
from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import MassSchema, Hour, MassSchemaRows, Intentions


class IntentionView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):
        print(MassSchemaRows.objects.all())
        # self.get_schema()
        object_context = model_class.objects.filter(id=id_object).prefetch_related('intentions_set')[0]
        intentions = []
        for intention in object_context.intentions_set.all().order_by('date', 'hour'):
            intentions.append(intention)
            # print(hour.church, hour.is_mb, hour.hour)
        # print(object_context.season_end)
        return {
            'intentionweek': object_context,
            'intentions': intentions
        }

    # def get(self, request, *args, **kwargs):
    #     method = kwargs.get('method', 'get')
    #     if method == 'next':
    #         return render(request, self.template_name, self.context)
    #     else:
    #         return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        self.context = {}
        params = dict(request.POST)
        method = kwargs.get('method', 'get')
        print('keys ', params)
        intentions = []
        print('stepDay ','stepDay' in params.keys())
        if 'stepDay' in params.keys():
            self.context['date'] = request.POST['date']
            print('masses', MassSchemaRows.objects.all())
            sunday_hours = MassSchemaRows.objects.filter(is_sunday=True)
            for hour in MassSchemaRows.objects.all():
                print('hour', hour.is_sunday, hour.hours)
            hours_in_sunday = []
            for sun in sunday_hours:
                hours_in_sunday.extend(sun.hours.split(', '))
            hours_in_sunday.sort()
            for hour in hours_in_sunday:

                intention = Intentions(hour=hour, date=self.context['date'])
                intentions.append(intention)
            # current_hours = MassSchemaRows.objects.filter(is_sunday=False)
            self.context['intentions'] = intentions
            return render(request, 'intentions_form.html', self.context)
        else:
            return super().post(request, *args, **kwargs)

    #     schema = WeekAnnouncement(date=request.POST['date'])
    #     schema.save()
    #     self.add_new_announcements(request, schema)
    #
    #     return redirect('detail', method='list', object_name='weekannouncement')
    #
    # def edit(self, request, *args, **kwargs):
    #     anothers = dict(request.POST)
    #     schema = WeekAnnouncement.objects.get(id=kwargs['pk'])
    #     schema.save()
    #     self.add_new_announcements(request, schema)
    #     self.messes = {}
    #
    #     for name, value in anothers.items():
    #         print('items edited', name, value)
    #         if name.startswith('old-'):
    #             row_number = name.split('-')[-1]
    #             announcement = Announcement.objects.get(id=row_number)
    #             announcement.content = value
    #             announcement.save()
    #         if name == 'deletions':
    #             for hour_element_id in value:
    #                 hour_id = hour_element_id.split('-')[-1]
    #                 hour = Announcement.objects.get(id=hour_id)
    #                 hour.delete()
    #     schema.save()
    #
    # def add_new_announcements(self, request, schema):
    #     anothers = dict(request.POST)
    #     print('anothers', anothers)
    #     for name, value in anothers.items():
    #         if name.startswith('a-'):
    #             announcement = Announcement(content=value,
    #                                         week_announcment=schema)
    #             announcement.save()
    #
