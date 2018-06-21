from django.conf.urls import include, url

from misiek import views
urlpatterns = [
    # ex: /polls/
    url('^adminek', views.index, name='index'),
    url('^actual_list$', views.actual, name='actual'),
    url('^actual_detail/(?P<actual_id>\d{1,4})/delete', views.actual_delete, name='actual_delete'),
    # url('^object/(?P<actual_id>\d{1,4})/delete', views.actual_delete, name='delete'),
    url(r'^object/(?P<object_name>\w+)/(?P<pk>[0-9]+)?$', views.DetailView.as_view(), name='detail'),
    url(r'^actual_detail/(?P<pk>[0-9]+)?$', views.DetailView.as_view(), name='actual_detail'),
    # url(r'^actual_new$', views.DetailView.as_view(), name='actual_detail'),
    url('^cancelary/add$', views.CancelaryCreateView.as_view(), name='cancelary_add'),
    url('^cancelary_list$', views.CancelaryListView.as_view(), name='cancelary'),
    url('^cancelary/(?P<pk>[0-9]+)', views.CancelaryUpdateView.as_view(), name='detail_day'),
    # url(r'^article/(?P<page_number>\d{1,4})?/$', views.articles, name='article_detail'),
]