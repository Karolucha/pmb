from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/(?P<page_number>\d+)/$', views.article_detail, name='articles'),
    url(r'^sacraments/(?P<sacrament_id>\d+)/$', views.sacraments, name='sacraments'),
    url(r'^galeries/(?P<galery_id>\d+)/$', views.galery, name='galeries'),
    url('^$', views.index, name='main'),
    # url(r'^article/(?P<page_number>\d{1,4})?/$', views.articles, name='article_detail'),

]