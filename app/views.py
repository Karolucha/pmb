from django.shortcuts import render
from datetime import datetime
# Create your views here.
from app.models import Actual, MassSchema, Hour, Announcement, WeekAnnouncment


def get_context(page_number=None):
    annoucements = ['Dziś obchodzimy wspomnienie św Tomasza',
                    'Zapraszamy na obchody']
    print('page number', page_number)

    if page_number is not None and page_number != '0':
        page_number = int(page_number)
        # newest_article = Actual.objects.()
        offset = page_number*3
        limit = page_number*3+3
        print('numbers ', offset, limit)
        articles = Actual.objects.all()[offset:limit]
        # print('articles ',articles)
        articles_sum = Actual.objects.all().count()
        # last_article = articles.order_by('date')[0]
        # print('article ', last_article.title)
        # if Actual.objects.filter(date__lt=articles.last().date):
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
    # mass = MassSchema.objects.filter(season_start__lte=today,
    #                                  season_end__gte=today)
    # mass = Hour.objects.filter(mass__season_start__gte=today,
    #                            mass__season_end__lte=today).select_related()
    masses = Hour.objects.select_related().all()
    print(masses[0].mass)
    churches = set(mass.church for mass in masses)
    oldes_sunday = []
    new_sunday = []
    # for i, hour in enumerate(masses):
    #     print(masses[i].mass)
    mass_schema = {
        'sunday': {
            'old': oldes_sunday,
            'new': new_sunday
        },
        'other': {

        }
    }

    # mass_schema = {
    #     'sunday': {
    #         church: [
    #             hour.hour for hour in masses if hour.church == church and
    #             hour.mass
    #
    #         ] for church in churches
    #     },
    #     'others': {
    #         church: [
    #             hour.hour for hour in masses if hour.church == church and
    #             not hour.mass.sunday
    #         ] for church in churches
    #     }
    # }
    last_date = WeekAnnouncment.objects.last().date
    annoucements = Announcement.objects.filter(week_announcment__date=last_date)
    context = {
        'latest_question_list': '22',
        'annoucements': annoucements,
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

# def articles(request, page_number=None):
#
#     return render(request, 'index.html', get_context(page_number=page_number))