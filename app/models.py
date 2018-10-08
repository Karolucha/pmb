import os

from django.db import models
import ast
#from stdimage import StdImageField

from pmb.settings import MEDIA_ROOT


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
    ('f', 'św. Faustyny'),
    ('mb', 'Miłosierdzia Bożego'),
)


class MassSchema(models.Model):
    # hours = models.ForeignKey(Hour)

    # week_of_mass = ListField(choices=DAYS_OF_WEEK, verbose_name='Dni których dotyczy rozpiska')
    season_name = models.CharField(max_length=50, verbose_name='nazwa sezonu', null=True, blank=True)
    season_start = models.DateField(verbose_name='Pierwszy dzień sezonu', null=True, blank=True)
    season_end = models.DateField(verbose_name='Ostatni dzień sezonu', null=True, blank=True)
    # monday = models.BooleanField(verbose_name='Poniedziałek', default=False)
    # tuesday = models.BooleanField(verbose_name='Wtorek', default=False)
    # wednesday = models.BooleanField(verbose_name='Środa', default=False)
    # thursday = models.BooleanField(verbose_name='Czwartek', default=False)
    # friday = models.BooleanField(verbose_name='Piątek', default=False)
    sunday = models.BooleanField(verbose_name='Niedziela', default=False)
    # saturday = models.BooleanField(verbose_name='Niedziela', default=False)

    def __str__(self):
        if self.sunday:
            sunday = " (niedzielne) "
        else:
            sunday = ""
        return "Msze święte w dniach " + str(self.season_start) + " - " + str(self.season_end) + sunday

    @staticmethod
    def get_foreign_name():
        return 'Hour'




    class Meta:
        verbose_name = 'Lista mszy w sezonie'
        verbose_name_plural = 'Schemat mszy'

class WeekOfMass(models.Model):
    week_day = models.CharField(choices=DAYS_OF_WEEK, max_length=12, null=True, blank=True,
                                verbose_name='Dzień tygodnia')
    mass_chema = models.ForeignKey(MassSchema, verbose_name='Lista mszy w sezonie', on_delete=models.CASCADE)

class Hour(models.Model):
    hour = models.TimeField(verbose_name='godzina mszy')
    mass = models.ForeignKey(MassSchema, verbose_name='msza', on_delete=models.CASCADE)
    church = models.CharField(max_length=50, choices=churches, verbose_name='kościół')

    def __str__(self):
        return 'g.' + str(self.hour) + ' kościół ' + self.church

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


class WeekAnnouncement(models.Model):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True, verbose_name='niedziela')

    def __str__(self):
        return "Na niedzielę " + str(self.date)

    class Meta:
        ordering = '-date',
        verbose_name='Ogłoszenia duszpasterskie'
        verbose_name_plural = 'Ogłoszenia duszpasterskie'


class Announcement(models.Model):
    content = models.CharField(max_length=15000, null=True, blank=True, verbose_name='treść')
    week_announcment = models.ForeignKey(WeekAnnouncement, verbose_name='Ogłoszenia', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.week_announcment.date)

    class Meta:
        verbose_name='Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'


class IntentionWeek(models.Model):
    week = models.DateField(max_length=200)
    description = models.CharField(max_length=500,null=True,blank=True)
    display_now = models.BooleanField(default=False)
    def __str__(self):
        return 'Intencje na tydzień od ' + str(self.week)

# class IntentionDay(models.Model):

class Intentions(models.Model):
    weeks = (
        ('I Tydzień', 'I Tydzień'),
        ('II Tydzień', 'II Tydzień'),
    )
    date = models.DateField(verbose_name='data')
    hour = models.TimeField(verbose_name='godzina')
    title = models.CharField(max_length=200, verbose_name='nazwa intencji')
    week = models.ForeignKey(IntentionWeek, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + ' g. ' + str(self.hour) + ' ' + self.title + '...'

    class Meta:
        verbose_name='Intencja'
        verbose_name_plural = 'Intencje'


class OfficeHours(models.Model):
    day = models.CharField(max_length=15, verbose_name='dzien tygodnia', choices=DAYS_OF_WEEK)
    start = models.TimeField(verbose_name='od godziny')
    end = models.TimeField(verbose_name='do godziny')

    class Meta:
        verbose_name = 'Godziny działania kancelarii w danym dniu'
        verbose_name_plural = 'Godziny działania kancelarii'

    # @property
    # def get_tem

    def __str__(self):
        return "Godziny dla dnia " + str(self.day)

    @staticmethod
    def get_context():
        return {'days': DAYS_OF_WEEK}


class Actual(models.Model):
    title = models.CharField(max_length=200, verbose_name='tytuł')
    content = models.CharField(max_length=25000, verbose_name='zawartość')
    date = models.DateTimeField(verbose_name='data publikacji', auto_now=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Nowy artykuł aktualności'
        verbose_name_plural = 'Aktualność'
        ordering = '-date',


class Sacrament(models.Model):
    name = models.CharField(max_length=50, verbose_name='nazwa sakramentu')
    content = models.CharField(max_length=15000, verbose_name='opis')

    def __str__(self):
        return 'Sakrament: ' + self.name

    class Meta:
        verbose_name = 'Sakrament'
        verbose_name_plural = 'Sakramenty'


class Ceremony(models.Model):
    name = models.CharField(max_length=50)
    time = models.TimeField()
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=20)
    church = models.CharField(churches, max_length=30)
    display_start = models.DateField()
    display_end = models.DateField()
    display_now = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SectionRows(models.Model):
    section_kind = models.CharField(max_length=50)
    row_content = models.CharField(max_length=500)


class MassSchemaRows(models.Model):
    is_sunday = models.BooleanField()
    church = models.CharField(churches, max_length=30)
    hours = models.CharField(max_length=100)


class Galery(models.Model):
    title = models.CharField(max_length=200, verbose_name='tytuł')
    description = models.CharField(max_length=25000, verbose_name='opis')
    date = models.DateTimeField(verbose_name='data publikacji', auto_now=True)
    date_event = models.DateField(verbose_name='data wydarzenia', null=True, blank=True)
    article = models.ForeignKey(Actual, null=True, blank=True, on_delete=models.CASCADE)


class ImageWithCaption(models.Model):
    image = models.ImageField()
    #image_all = StdImageField(upload_to=os.path.join(MEDIA_ROOT, 'public'), blank=True, variations={'large': (640, 480), 'thumbnail': (100, 100, True)})
    caption = models.CharField(max_length=500, null=True, blank=True)
    galery = models.ForeignKey(Galery, on_delete=models.CASCADE)


class ActivityGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name='nazwa')
    description = models.CharField(max_length=1000, verbose_name='opis', null=True, blank=True)
    meeting_description = models.CharField(max_length=1000, verbose_name='kiedy spotkania', null=True, blank=True)


class Church(models.Model):
    name = models.CharField(max_length=200, verbose_name='nazwa')
    description = models.CharField(max_length=1000, verbose_name='opis', null=True, blank=True)


class Pastor(models.Model):
    name = models.CharField(max_length=100, verbose_name='imię i nazwisko')
    image = models.ImageField()


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='dane')
    value = models.CharField(max_length=100, verbose_name='dane parafii')
