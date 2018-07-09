from django.shortcuts import render
from datetime import datetime
# Create your views here.
from app.models import Actual, MassSchema, Hour, Announcement, WeekAnnouncment, OfficeHours, Sacrament
CURRENT_SEASON = 'wiosenny'

def get_context(page_number=None):
    print('page number', page_number)

    if page_number is not None and page_number != '0':
        page_number = int(page_number)
        offset = page_number*3
        limit = page_number*3+3
        print('numbers ', offset, limit)
        articles = Actual.objects.all()[offset:limit]
        articles_sum = Actual.objects.all().count()
        if articles_sum - offset > 2:
            older_number = page_number + 1
            next_number = page_number - 1
        else:
            older_number = None
            next_number = page_number - 1
    else:
        articles = Actual.objects.all()[:3]
        has_previous = False
        has_next = True
        next_number = None
        older_number = 1
    today = datetime.now().date()
    mass_schemas = MassSchema.objects.filter(season_name=CURRENT_SEASON)
    sundays = mass_schemas.filter(sunday=True).select_related()
    print(sundays[0].hour_set)


    masses = Hour.objects.select_related().all()
    print('masses mass_schemas', mass_schemas)
    churches = set(mass.church for mass in masses)
    oldes_sunday = []
    new_sunday = []
    mass_schema = {
        'sunday': {
            'old': oldes_sunday,
            'new': new_sunday
        },
        'other': {

        }
    }
    last_date = WeekAnnouncment.objects.last().date
    print(last_date)
    annoucements = Announcement.objects.filter(week_announcment__date=last_date)
    office_hours = OfficeHours.objects.all()
    sacraments_queryset = Sacrament.objects.all()
    print('return context')
    context = {
        'latest_question_list': '22',
        'annoucements': annoucements,
        'officeHours': office_hours,
        'sacraments_all': sacraments_queryset,
        'articles': articles,
        # 'has_previous': has_previous,
        # 'has_next': has_next,
        'mass_schema': mass_schema,
        'next_number': next_number,
        'older_number': older_number,
        'old_messes': '08:30, 10:00, 11:30',
        'new_messes': '07:00, 13:30, 18:00',
        'old_messes_other': '9:00, 17:00'
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
