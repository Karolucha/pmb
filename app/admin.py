from django.contrib import admin
from django import forms
# Register your models here.
from django.forms import models, TimeField, TimeInput, SplitDateTimeWidget, DateInput
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from tinymce.models import HTMLField
from django.forms.extras.widgets import SelectDateWidget
from app.models import *
from django.contrib.admin import widgets


class MassForm(forms.ModelForm):
    # church = HTMLField()
    # week_of_mass = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = MassSchema
        fields = ['season_start', 'season_end',
                  'season_name',
                  'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'sunday', 'saturday']
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
        widgets = {
            'content': SummernoteWidget(),
        }


@admin.register(Actual)
class ActualAdmin(SummernoteModelAdmin):
    summer_note_fields = '__all__'
    form = ActualForm


#---------------------------ANNOUNCEMENTS-----------#

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = 'content',
        widgets = {
            'content': SummernoteWidget(),
        }


class AnnouncementAdmin(admin.StackedInline):
    model = Announcement
    form = AnnouncementForm


@admin.register(WeekAnnouncment)
class WeekAnnouncmentAdmin(admin.ModelAdmin):
    inlines = [AnnouncementAdmin]
    model = WeekAnnouncment
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



admin.site.register(OfficeHours)
# admin.site.register(SubPages)
