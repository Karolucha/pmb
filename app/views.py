from django.shortcuts import render
from datetime import datetime
from app.models import (Actual, WeekAnnouncement, OfficeHours, Sacrament, MassSchemaRows,
                        Ceremony, DAYS_OF_WEEK, IntentionWeek, Church, ActivityGroup, Pastor, Galery, Contact,
                        MassSchema)

CHURCHES = Church.objects.all()


def get_context(page_number=None):
    today = datetime.now().date()

    context = {
        'DAYS_OF_WEEK': DAYS_OF_WEEK,
        'annoucements': get_announcements(today),
        'mb': CHURCHES[0],
        'f': CHURCHES[1],
        'today_listening': "http://mateusz.pl/czytania/{}/{}.html".format(
            datetime.now().year, datetime.now().strftime('%Y%m%d')),
    }
    context.update(extend_for_intentions(today))
    context.update(extend_for_articles(page_number))
    context.update(extend_for_all_records(today))
    context.update(extend_for_messes())
    return context


def extend_for_intentions(today):
    intentions = []
    current_intentions_from_db = dict()
    object_intentions = IntentionWeek.objects.filter(week__lt=today).order_by('-week').prefetch_related('intentions_set')
    if len(object_intentions) < 1:
        return {}
    current_intentions_from_db['object'] = object_intentions[0]
    date = current_intentions_from_db['object'].week
    i = 0
    intentions_day = []
    days = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota']
    sorted_by = current_intentions_from_db['object'].intentions_set.all()
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

    current_intentions_from_db['intentions'] = intentions
    # print('return context ', current_intentions_from_db['object'].id)
    return {
        'intention_week': current_intentions_from_db,
    }


def extend_for_articles(page_number):

    if page_number is not None and page_number != '0':
        page_number = int(page_number)
        offset = page_number*3
        limit = page_number*3+3
        articles = Actual.objects.all().order_by('-date')[offset:limit]
        # articles = articles_more[:-1]
        articles_sum = Actual.objects.all().count()
        if articles_sum - limit > 0:
            older_number = page_number + 1
            next_number = page_number - 1

        else:
            older_number = None
            next_number = page_number - 1
    else:
        articles = Actual.objects.all().order_by('-date')[:3]
        next_number = None
        older_number = 1
    return {
        'articles': articles,
        'next_number': next_number,
        'older_number': older_number,
    }


def extend_for_all_records(today):
    return {
        'pastors': Pastor.objects.all().order_by('-id'),
        'galeries': Galery.objects.all(),
        'ceremonies': Ceremony.objects.filter(
            display_start__lt=today,
            display_end__gt=today
        ),
        'activity_groups': ActivityGroup.objects.all(),
        'officeHours': OfficeHours.objects.all(),
        'sacraments_all': Sacrament.objects.all(),
        'contacts': Contact.objects.all().order_by('id')
    }


# def extend_for_messes():
#     return {
#         'old_messes': get_messes_for('mb', True),
#         'new_messes': get_messes_for('f', True),
#         'new_messes_other': get_messes_for('f', False),
#         'old_messes_other': get_messes_for('mb', False)
#     }


def get_announcements(today):
    week_announcements = WeekAnnouncement.objects.filter(date__lt=today).order_by('-date').prefetch_related(
        'announcement_set')
    if len(week_announcements) > 0:
        return week_announcements[0].announcement_set.all()
    else:
        return []


def extend_for_messes():
    now = datetime.now().date()
    mass_schemas = MassSchema.objects.filter(
        season_start__lt=now, season_end__gt=now).prefetch_related('hour_set')
    # return ','.join(mass_schemas[0].hour_set.all().order_by('hour'))
    messes = {}
    for mass_schema in mass_schemas:
        post_fix = '_other' if mass_schema.sunday else ''
        messes.update(get_hours_splitted(mass_schema.hour_set.all().order_by('hour'), post_fix))
    return messes


def get_hours_splitted(hour_set, post_fix):
    hours = dict()
    hours['old_messes' + post_fix] = []
    hours['new_messes' + post_fix] = []
    for hour in hour_set:
        if hour.church == 'mb':
            prefix = 'old'
        else:
            prefix = 'new'
        hours[prefix + '_messes' + post_fix].append(hour.hour.strftime('%H:%M'))
    for key in hours:
        hours[key] = ','.join(hours[key])
    return hours


def index(request):
    return render(request, 'index.html', get_context())


def article_detail(request, page_number):
    return render(request, 'index.html', get_context(page_number))


def sacraments(request, sacrament_id):
    context = get_context()
    sacrament = Sacrament.objects.get(id=sacrament_id)
    context['sacrament'] = sacrament
    return render(request, 'index.html', context)


def galery(request, galery_id):
    context = get_context()
    one_galery = Galery.objects.filter(id=galery_id).prefetch_related('imagewithcaption_set')[0]
    images = one_galery.imagewithcaption_set.all().order_by('id')
    context['galery'] = one_galery
    context['images'] = images
    context['size'] = len(list(images))
    context['images_numbers'] = [{
                               'idx': i + 1, 'image': img} for i, img in enumerate(list(images))]
    return render(request, 'index_to_extend.html', context)
