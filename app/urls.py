from django.conf.urls import include, url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^articles/(?P<page_number>\d+)/$', views.article_detail, name='articles'),
    url('^$', views.index, name='index'),
    # url(r'^article/(?P<page_number>\d{1,4})?/$', views.articles, name='article_detail'),
    # ex: /polls/5/

]