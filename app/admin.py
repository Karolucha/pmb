from django.contrib import admin
from django import forms
# Register your models here.
from django.forms import models, TimeField, TimeInput, SplitDateTimeWidget, DateInput

from app.models import *
from django.contrib.admin import widgets


class MassForm(forms.ModelForm):
    # church = HTMLField()
    # week_of_mass = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = MassSchema
        fields = ['season_start', 'season_end',
                  'season_name',
                  'sunday']

        # 'monday', 'tuesday', 'wednesday', 'thursday',
                  # 'friday', 'sunday',
#test 1234qwer


class myHour(forms.ModelForm):
    class Meta:
        model = Hour
        fields = 'hour', 'church'
        widgets = {
            'hour': TimeInput(attrs={'type': 'time'})
        }


class myHours(admin.StackedInline):
    model=Hour
    form=myHour


@admin.register(MassSchema)
class MassAdmin(admin.ModelAdmin):
    inlines = [myHours]
    form = MassForm

#----------------------Aktualnosci

class ActualForm(forms.ModelForm):
    class Meta:
        model = Actual
        fields = 'title', 'content'


@admin.register(Actual)
class ActualAdmin(admin.ModelAdmin):
    summer_note_fields = '__all__'
    form = ActualForm


#---------------------------ANNOUNCEMENTS-----------#

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = 'content',


class AnnouncementAdmin(admin.StackedInline):
    model = Announcement
    form = AnnouncementForm


@admin.register(WeekAnnouncement)
class WeekAnnouncmentAdmin(admin.ModelAdmin):
    inlines = [AnnouncementAdmin]
    model = WeekAnnouncement
    date = forms.DateField(widget=TimeInput)


#---------------INTENCJE

class IntentionForm(forms.ModelForm):
    class Meta:
        model = Intentions
        fields = 'hour', 'date', 'title'
        widgets = {
            'hour': TimeInput(attrs={'type': 'time'})
        }


class IntentionAdmin(admin.StackedInline):
    model=Intentions
    form=IntentionForm


class WeekIntentionForm(forms.ModelForm):
    # church = HTMLField()
    # week_of_mass = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = IntentionWeek
        fields = ['week']

#@admin.register(Intentions)
class IntentionsAdmin(admin.ModelAdmin):
    inlines = [IntentionAdmin]
    form = WeekIntentionForm


#----------------------Sakramenty

class SacramentForm(forms.ModelForm):
    class Meta:
        model = Sacrament
        fields = 'name', 'content'

@admin.register(Sacrament)
class SacramentAdmin(admin.ModelAdmin):
    form = SacramentForm


admin.site.register(OfficeHours)
# admin.site.register(Sacraments)
# admin.site.register(SubPages)
