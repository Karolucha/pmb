from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import WeekAnnouncement, Announcement


class AnnouncementView(BaseGenericView):
    messes = {}

    def get_for_single(self, model_class, id_object):

        object_context = model_class.objects.filter(id=id_object).prefetch_related('announcement_set')[0]
        print('object_context', object_context.date)
        hours_set = []
        for msg in object_context.announcement_set.all().order_by('id'):
            print('conernt', msg.content)
            hours_set.append(msg)
            # print(hour.church, hour.is_mb, hour.hour)
        return {
            'schema': object_context,
            'announcements': hours_set
        }

    def get(self, request, *args, **kwargs):
        method = kwargs.get('method', 'get')
        if method == 'download':
            return redirect('detail', method='list', object_name='weekannouncement')
        else:
            return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print('time to save')
        schema = WeekAnnouncement(date=request.POST['date'])
        schema.save()
        self.add_new_announcements(request, schema)

        return redirect('detail', method='list', object_name='weekannouncement')

    def edit(self, request, *args, **kwargs):
        anothers = dict(request.POST)
        schema = WeekAnnouncement.objects.get(id=kwargs['pk'])
        schema.save()
        self.add_new_announcements(request, schema)
        self.messes = {}

        for name, value in anothers.items():
            print('items edited', name, value)
            if name.startswith('old-'):
                row_number = name.split('-')[-1]
                announcement = Announcement.objects.get(id=row_number)
                announcement.content = value[0]
                announcement.save()
            if name == 'deletions':
                for hour_element_id in value:
                    hour_id = hour_element_id.split('-')[-1]
                    hour = Announcement.objects.get(id=hour_id)
                    hour.delete()
        schema.save()

    def add_new_announcements(self, request, schema):
        anothers = dict(request.POST)
        print('anothers', anothers)
        for name, value in anothers.items():
            if name.startswith('a-'):
                announcement = Announcement(content=value,
                                            week_announcment=schema)
                announcement.save()

