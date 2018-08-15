from datetime import datetime, timedelta
from adminek.views.generic_views import BaseGenericView
from django.shortcuts import render, redirect

from app.models import MassSchemaRows, Intentions, IntentionWeek


class IntentionView(BaseGenericView):
    messes = {}

    def __init__(self, **kwargs):
        self.days = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota']
        super().__init__(**kwargs)

    def get_for_single(self, model_class, id_object):
        object_context = IntentionWeek.objects.filter(id=id_object).prefetch_related('intentions_set')[0]
        intentions = []
        for intention in object_context.intentions_set.all().order_by('date', 'hour'):
            intentions.append(intention)
        return {
            'intentionweek': object_context,
            'intentions': intentions
        }

    def get(self, request, *args, **kwargs):
        method = kwargs.get('method', 'get')
        if method == 'edit':
            self.context = {}
            intentions = []
            self.context['object'] = self.get_for_single(self.model_class, kwargs['pk'])
            intention_week = self.context['object']
            date = intention_week['intentionweek'].week
            self.context['date'] =  intention_week['intentionweek'].week
            i = 0
            intentions_day = []
            for intention in intention_week['intentions']:
                if intention.date != date:
                    intentions.append({
                        'day': self.days[i],
                        'intentions': intentions_day.copy()})
                    i += 1
                    date = intention.date
                    intentions_day = []
                intentions_day.append(intention)

            intentions.append({
                'day': self.days[i],
                'intentions': intentions_day.copy()})
            self.template_name = 'others/intentions_form.html'
            self.context['intentions'] = intentions
            return render(request, self.template_name, self.context)
        else:
            return super().get(request, *args, **kwargs)

    def get_template_name(self, method):
        if method == 'edit':
            self.template_name = 'others/intentionweek_edit'
        else:
            super().get_template_name(method)

    def post(self, request, *args, **kwargs):
        self.context = {}
        params = dict(request.POST)
        intentions = []
        if 'stepDay' in params.keys():
            self.context['date'] = request.POST['date']
            old_week = IntentionWeek.objects.filter(week=self.context['date'])
            if old_week.exists():
                return redirect('intentionweek', method='edit', pk=old_week[0].id, object_name='intentionweek')
            self.prepare_intentions(intentions, True, self.days[0], 0)
            for index, day in enumerate(self.days[1:]):
                self.prepare_intentions(intentions, False, day, index+1)
            self.context['intentions'] = intentions
            print('what are ', self.context)
            return render(request, 'others/intentions_form.html', self.context)
        else:
            return super().post(request, *args, **kwargs)

    def prepare_intentions(self, intentions, is_sunday, day, index):
        sunday_hours = MassSchemaRows.objects.filter(is_sunday=is_sunday)
        hours_in_sunday = []
        for sun in sunday_hours:
            hours_in_sunday.extend(sun.hours.split(', '))
        hours_in_sunday.sort()
        hours = []
        for hour in hours_in_sunday:
            date = (datetime.strptime(self.context['date'], '%Y-%m-%d') + timedelta(days=index)).date()
            intention = Intentions(hour=hour, date=date)
            hours.append(intention)
        intentions.append({
            'day': day,
            'intentions': hours})

    def create(self, request, *args, **kwargs):
        params = dict(request.POST)
        intention_week = IntentionWeek(week=request.POST['date'])
        intention_week.save()

        for day in self.days:
            hours_for_day = {key: value for key, value in params.items() if key.startswith(day+'-hour')}
            for hour_key in hours_for_day:
                hour = hour_key.split('-')[-1]
                intention = Intentions(date=params[day+'-date-'+hour][0], hour=hour,
                                       title=params[day+'-content-'+hour][0], week=intention_week)
                intention.save()

        return redirect('detail', method='list', object_name='intentionweek')


    def edit(self, request, *args, **kwargs):
        params = dict(request.POST)
        for day in self.days:
            hours_for_day = {key: value[0] for key, value in params.items() if key.startswith(day+'-hour')}
            for hour_key in hours_for_day:
                hour = hour_key.split('-')[-1]
                intention = Intentions.objects.filter(id=params[day+'-id-'+hour][0])[0]
                intention.title = params[day+'-content-'+hour][0]
                intention.save()
