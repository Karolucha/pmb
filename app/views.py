from django.shortcuts import render
from datetime import datetime
# Create your views here.
from adminek.views.mass_view import MassSchemaIssue
from app.models import Actual, MassSchema, Hour, Announcement, WeekAnnouncement, OfficeHours, Sacrament, MassSchemaRows, \
    Ceremony, DAYS_OF_WEEK, IntentionWeek

CURRENT_SEASON = 'wiosenny'

def get_context(page_number=None):
    print('page number', page_number)

    if page_number is not None and page_number != '0':
        page_number = int(page_number)
        offset = page_number*3
        limit = page_number*3+3
        print('numbers ', offset, limit)
        articles = Actual.objects.all().order_by('-date')[offset:limit]
        articles_sum = Actual.objects.all().count()
        if articles_sum - offset > 2:
            older_number = page_number + 1
            next_number = page_number - 1
        else:
            older_number = None
            next_number = page_number - 1
    else:
        articles = Actual.objects.all().order_by('-date')[:3]
        has_previous = False
        has_next = True
        next_number = None
        older_number = 1
    # today = datetime.now().date()
    # mass_schemas = MassSchema.objects.filter(season_name=CURRENT_SEASON)
    # sundays = mass_schemas.filter(sunday=True).select_related()
    # print(sundays[0].hour_set)


    # masses = Hour.objects.select_related().all()
    # print('masses mass_schemas', mass_schemas)
    # churches = set(mass.church for mass in masses)
    # oldes_sunday = []
    # new_sunday = []
    # mass_schema = {
    #     'sunday': {
    #         'old': oldes_sunday,
    #         'new': new_sunday
    #     },
    #     'other': {
    #
    #     }
    # }
    today = datetime.now().date()

    intentions = []
    context_int = {}
    context_int['object'] = IntentionWeek.objects.filter(week__lt=today).order_by('-week').prefetch_related('intentions_set')[0]
    date = context_int['object'].week
    i = 0
    intentions_day = []
    days = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota']
    sorted_by = context_int['object'].intentions_set.all()
    for intention in sorted_by.order_by('date', 'hour'):
        if intention.date != date:
            intentions.append({
                'day': days[i],
                'intentions': intentions_day.copy()})
            i += 1
            date = intention.date
            intentions_day = []
        intentions_day.append(intention)

    intentions.append({
        'day': days[i],
        'intentions': intentions_day.copy()})

    context_int['intentions'] = intentions

    annoucements = WeekAnnouncement.objects.filter(date__lt=today).order_by('-date').prefetch_related('announcement_set')[0].announcement_set.all()
    office_hours = OfficeHours.objects.all()
    sacraments_queryset = Sacrament.objects.all()
    print('return context')
    # http: // mateusz.pl / czytania / 2018 / 20180810.html
    today_listening = "http://mateusz.pl/czytania/{}/{}.html".format(datetime.now().year,datetime.now().strftime('%Y%m%d'))
    mass_issue = MassSchemaIssue()
    mass_issue.get_schema()

    context = {
        'DAYS_OF_WEEK': DAYS_OF_WEEK,
        'latest_question_list': '22',
        'intention_week': context_int,
        # 'intention_week': IntentionWeek.objects.filter(display_now=True).prefetch_related('intentions_set')[0],
        'annoucements': annoucements,
        'officeHours': office_hours,
        'sacraments_all': sacraments_queryset,
        'articles': articles,
        'ceremonies': Ceremony.objects.all(),
        'today_listening': today_listening,
        # 'has_previous': has_previous,
        # 'has_next': has_next,
        'next_number': next_number,
        # 'mass_schema': mass_schema,
        'older_number': older_number,
        'old_messes': MassSchemaRows.objects.filter(church='mb', is_sunday=True)[0].hours,
        'new_messes': MassSchemaRows.objects.filter(church='f', is_sunday=True)[0].hours,
        'old_messes_other': MassSchemaRows.objects.filter(church='mb', is_sunday=False)[0].hours
    }
    return context

def index(request):
    print('index')
    return render(request, 'index.html', get_context())

def article_detail(request, page_number):
    print('article_detail page number', page_number)
    return render(request, 'index.html', get_context(page_number))


def sacraments(request, sacrament_id):
    context = get_context()
    sacrament = Sacrament.objects.get(id=sacrament_id)
    print(sacrament)
    context['sacrament'] = sacrament
    return render(request, 'index.html', context)
