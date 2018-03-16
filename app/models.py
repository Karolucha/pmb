from datetime import datetime, time
from django.db import models
from django.db import models
import ast

class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        print('to python ', value)
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        print('get grep value', value)
        return value
        # if value is None:
        #     return value
        #
        # return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
DAYS_OF_WEEK = (
    ('Poniedziałek', 'Poniedziałek'),
    ('Wtorek', 'Wtorek'),
    ('Środa', 'Środa'),
    ('Czwartek', 'Czwartek'),
    ('Piątek', 'Piątek'),
    ('Sobota', 'Sobota'),
    ('Niedziela', 'Niedziela'),
)

churches = (
    ('św. Faustyny', 'św. Faustyny'),
    ('Miłosierdzia Bożego', 'Miłosierdzia Bożego'),
)

# class Week()

class MassSchema(models.Model):
    # hours = models.ForeignKey(Hour)

    # week_of_mass = ListField(choices=DAYS_OF_WEEK, verbose_name='Dni których dotyczy rozpiska')
    season_name = models.CharField(max_length=20, verbose_name='nazwa sezonu', null=True, blank=True)
    season_start = models.DateField(verbose_name='Pierwszy dzień sezonu', null=True, blank=True)
    season_end = models.DateField(verbose_name='Ostatni dzień sezonu', null=True, blank=True)
    monday = models.BooleanField(verbose_name='Poniedziałek', default=False)
    tuesday = models.BooleanField(verbose_name='Wtorek', default=False)
    wednesday = models.BooleanField(verbose_name='Środa', default=False)
    thursday = models.BooleanField(verbose_name='Czwartek', default=False)
    friday = models.BooleanField(verbose_name='Piątek', default=False)
    sunday = models.BooleanField(verbose_name='Sobota', default=False)
    saturday = models.BooleanField(verbose_name='Niedziela', default=False)

    def __str__(self):
        return "Schemat mszy dla sezonu " + str(self.season_start) + " - " + str(self.season_end)

    class Meta:
        verbose_name = 'Lista mszy w sezonie'
        verbose_name_plural = 'Schemat mszy'

class WeekOfMass(models.Model):
    week_day = models.CharField(choices=DAYS_OF_WEEK, max_length=12, null=True, blank=True,
                                verbose_name='Dzień tygodnia')
    mass_chema = models.ForeignKey(MassSchema, verbose_name='Lista mszy w sezonie')

class Hour(models.Model):
    hour = models.TimeField(verbose_name='godzina mszy', null=True, blank=True)
    mass = models.ForeignKey(MassSchema, null=True, blank=True, verbose_name='msza')
    church = models.CharField(max_length=50, null=True, blank=True, choices=churches, verbose_name='kościół')

    def __str__(self):
        return str(self.hour)

    class Meta:
        verbose_name = 'Msza święta'
        verbose_name_plural = 'Msze'


class SubPages(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tytuł')
    shortcut = models.CharField(max_length=50, null=True, blank=True, verbose_name='Co wyświetlać w karcie')
    category = models.CharField(max_length=50, null=True, blank=True, verbose_name='Grupa podstron(0-jeśli nowa)')
    class Meta:
        verbose_name='Podstrona'
        verbose_name_plural = 'Podstrony'


class WeekAnnouncment(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name='niedziela')
    def __str__(self):
        return "Na niedzielę " + str(self.date)
    class Meta:
        ordering = '-date',
        verbose_name='Ogłoszenia duszpasterskie'
        verbose_name_plural = 'Ogłoszenia duszpasterskie'



class Announcment(models.Model):
    content = models.CharField(max_length=1500, null=True, blank=True, verbose_name='treść')
    week_announcment = models.ForeignKey(WeekAnnouncment, verbose_name='Ogłoszenia')
    def __str__(self):
        return str(self.week_announcment.date)
    class Meta:

        verbose_name='Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'


class Intentions(models.Model):
    # date = models.DateTimeField(verbose_name='termin_mszy')

    weeks = (
        ('I Tydzień', 'I Tydzień'),
        ('II Tydzień', 'II Tydzień'),
    )
    week = models.CharField(max_length=100, choices=weeks)
    date = models.ForeignKey(Hour)
    title = models.CharField(max_length=100, verbose_name='nazwa intencji')
    # tydzien_w_roku = models.IntegerField()
    class Meta:
        verbose_name='Intencja'
        verbose_name_plural = 'Intencje'


class OfficeHours(models.Model):
    day = models.CharField(max_length=10, verbose_name='dzien tygodnia', choices=DAYS_OF_WEEK)
    start = models.IntegerField(verbose_name='od godziny')
    end = models.IntegerField(verbose_name='do godziny')
    class Meta:
        verbose_name='Godziny działania kancelarii w danym dniu'
        verbose_name_plural = 'Godziny działania kancelarii'

class Actual(models.Model):
    title = models.CharField(max_length=100, verbose_name='tytuł')
    content = models.CharField(max_length=25000, verbose_name='zawartość')
    date = models.DateTimeField(verbose_name='data publikacji', default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Nowy artykuł aktualności'
        verbose_name_plural = 'Aktualność'
        ordering = '-date',