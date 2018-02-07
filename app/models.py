from datetime import time
from django.db import models
from django.db import models
import ast

class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        return value
        # if value is None:
        #     return value
        #
        # return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
DAYS_OF_WEEK = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
    (6, 'Sobota'),
    (7, 'Niedziela'),
)

churches = (
    (0, 'św. Faustyny'),
    (1, 'Miłosierdzia Bożego'),
)

class Mass(models.Model):


    # hours = models.ForeignKey(Hour)
    week_day = models.CharField(choices=DAYS_OF_WEEK, max_length=12, null=True, blank=True, verbose_name='Dzień tygodnia')
    church = models.CharField(max_length=50, null=True, blank=True, choices=churches)
    season_name = models.CharField(max_length=20, verbose_name='nazwa sezonu', null=True, blank=True)
    season_start = models.DateField(verbose_name='Pierwszy dzień sezonu', null=True, blank=True)
    season_end = models.DateField(verbose_name='Ostatni dzień sezonu', null=True, blank=True)

    class Meta:
        verbose_name='Msze święte w dniu'
        verbose_name_plural = 'Msze święte'

class Hour(models.Model):
    hour=models.TimeField(verbose_name='godzina mszy', null=True, blank=True)
    mass = models.ForeignKey(Mass, null=True, blank=True, verbose_name='msza')



    class Meta:
        verbose_name='godzina'
        verbose_name_plural = 'godziny mszy'

class SubPages(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tytuł')
    shortcut = models.CharField(max_length=50, null=True, blank=True, verbose_name='Co wyświetlać w karcie')
    category = models.CharField(max_length=50, null=True, blank=True, verbose_name='Grupa podstron(0-jeśli nowa)')
    class Meta:
        verbose_name='Podstrona'
        verbose_name_plural = 'Podstrony'

class WeekAnnouncment(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name='niedziela')
    class Meta:
        verbose_name='Ogłoszenia duszpasterskie'
        verbose_name_plural = 'Ogłoszenia duszpasterskie'



class Announcment(models.Model):
    treść = models.CharField(max_length=50, null=True, blank=True)
    ogloszenia = models.ForeignKey(WeekAnnouncment, verbose_name='Ogłoszenia')
    class Meta:
        verbose_name='Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'


class Intentions(models.Model):
    date = models.DateTimeField(verbose_name='termin_mszy')
    title = models.CharField(max_length=100, verbose_name='nazwa intencji')
    # tydzien_w_roku = models.IntegerField()
    class Meta:
        verbose_name='Intencja'
        verbose_name_plural = 'Intencje'


class OfficeHours(models.Model):
    day = models.CharField(max_length=10, verbose_name='dzien tygodnia')
    start = models.IntegerField(verbose_name='od godziny')
    end = models.IntegerField(verbose_name='do godziny')
    class Meta:
        verbose_name='Godziny działania kancelarii w danym dniu'
        verbose_name_plural = 'Godziny działania kancelarii'

class Actual(models.Model):
    title = models.CharField(max_length=100, verbose_name='tytuł')
    content = models.CharField(max_length=1000, verbose_name='zawartość')
    date = models.DateTimeField(verbose_name='data publikacji')
    class Meta:
        verbose_name='Nowy artykuł aktualności'
        verbose_name_plural = 'Aktualność'
