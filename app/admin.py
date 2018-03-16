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
    widgets = {
        'hour': DateInput(attrs={'type': 'time'})
    }
class MassHourForm(forms.ModelForm):
    class Meta:
        model=WeekOfMass
        fields = 'week_day',

class MassHours(admin.StackedInline):
    # hour = forms.TypedChoiceField(choices=[('10:00', '10 AM'), ('12:00', '12 PM')] )
    model = WeekOfMass
    # form = myHour
    # inlines = [myHour]


@admin.register(MassSchema)
class MassAdmin(admin.ModelAdmin):
    inlines = [myHours]
    form = MassForm


class SomeForm(forms.ModelForm):
    class Meta:
        model = Announcment
        fields = 'content',
        widgets = {
            'content': SummernoteWidget(),
        }


class AnnouncmentAdmin(admin.StackedInline):
    model = Announcment
    form = SomeForm


@admin.register(WeekAnnouncment)
class WeekAnnouncementAdmin(SummernoteModelAdmin):
    inlines = [AnnouncmentAdmin]
    summer_note_fields = '__all__'
    model = WeekAnnouncment
    date = forms.DateField(widget=TimeInput)


class ActualForm(forms.ModelForm):
    class Meta:
        model = Actual
        fields = 'title', 'content'
        widgets = {
            'content': SummernoteWidget(),
        }


@admin.register(Actual)
class Announcment(SummernoteModelAdmin):
    summer_note_fields = '__all__'
    form = ActualForm

admin.site.register(OfficeHours)
admin.site.register(Intentions)
admin.site.register(SubPages)
