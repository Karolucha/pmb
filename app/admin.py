from django.contrib import admin
from django import forms
# Register your models here.
from django.forms import models, TimeField, TimeInput
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from tinymce.models import HTMLField

from app.models import *



class MassForm(forms.ModelForm):
    # church = HTMLField()

    class Meta:
        model=Mass
        # exclude=["church"]
        fields =['church', 'season_end', 'season_start', 'season_name', 'week_day']
#         formfield_overrides = {
#             models.TextField: {'widget': RichTextEditorWidget},
#         }

#test 1234qwer


class MassHours(admin.StackedInline):
    # hour = forms.TypedChoiceField(choices=[('10:00', '10 AM'), ('12:00', '12 PM')] )
    model = Hour

@admin.register(Mass)
class MassAdmin(admin.ModelAdmin):
    inlines = [MassHours]
    form = MassForm


class AnnouncmentAdmin(admin.StackedInline):
    model=Announcment

@admin.register(WeekAnnouncment)
class WeekAnnouncementAdmin(SummernoteModelAdmin):
    inlines = [AnnouncmentAdmin]
    summer_note_fields = '__all__'
    model=WeekAnnouncment
    date = forms.CharField(widget=SummernoteWidget())
    # formfield_overrides = {
    #         models.TextField: {'widget': RichTextEditorWidget},
    #     }
# admin.site.register(WeekAnnouncment)
admin.site.register(OfficeHours)
admin.site.register(Actual)
admin.site.register(Intentions)
admin.site.register(SubPages)