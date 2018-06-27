from django.conf.urls import url

from adminek.views import actual, cancelary

urlpatterns = [
    url('^adminek', actual.index, name='index'),
    url('^actual_list$', actual.actual_list, name='actual'),
    url('^actual_detail/(?P<actual_id>\d{1,4})/delete', actual.actual_delete, name='actual_delete'),
    url(r'^object/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', actual.ActualDetailView.as_view(), name='detail'),
    url(r'^actual_detail/(?P<pk>[0-9]+)?$', actual.ActualDetailView.as_view(), name='actual_detail'),
    url('^cancelary/add$', cancelary.CancelaryCreateView.as_view(), name='cancelary_add'),
    url('^cancelary_list$', cancelary.CancelaryListView.as_view(), name='cancelary'),
    url('^cancelary/(?P<pk>[0-9]+)', cancelary.CancelaryUpdateView.as_view(), name='detail_day'),
]