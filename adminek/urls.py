from django.conf.urls import url

from adminek.views import actual, cancelary, generic_views, mass_view
from adminek.views import announcement_view
from adminek.views import intention_view

urlpatterns = [
    url('^adminek', actual.index, name='index'),
    url('^actual_list$', actual.actual_list, name='actual'),
    url('^actual_detail/(?P<actual_id>\d{1,4})/delete', actual.actual_delete, name='actual_delete'),
    url(r'^object/(?P<method>\w+)?/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', generic_views.BaseGenericView.as_view(), name='detail'),
    url(r'^mass/(?P<method>\w+)?/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', mass_view.MassSchemaView.as_view(), name='mass'),
    url(r'^announcement/(?P<method>\w+)?/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', announcement_view.AnnouncementView.as_view(), name='announcement'),
    url(r'^intentionweek/(?P<method>\w+)?/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', intention_view.IntentionView.as_view(), name='intentionweek'),
    url(r'^actual_detail/(?P<pk>[0-9]+)?$', actual.ActualDetailView.as_view(), name='actual_detail'),
]
