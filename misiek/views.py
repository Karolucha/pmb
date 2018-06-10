from django.shortcuts import render
from django.views import View
from django.views import generic

from app.models import Actual
def get_context():
    return {
        'list': 'admin'
    }


def index(request):
    print('my index')
    actions = [
    {
      'name': 'Aktualności',
      'link': 'actual'
    },
    {
      'name': 'Godziny działania kancelari',
      'link': 'cancelary'
    }
  ]
    return render(request, 'index2.html', {'actions': actions})

def cancelary(request):
    print('my index')
    return render(request, 'cancelary.html', get_context())

def actual(request):
    print('just actual')
    # actual_list_links = [
    #     {'name': 'Festyn parafialny', 'id': 10},
    #     {'name': 'Boże ciało', 'id': 9},
    # ]
    actual_list_links = Actual.objects.all()
    return render(request, 'actual.html', {'actual_list_links': actual_list_links})

def actual_detail(request, actual_id):
    print('ACTUAL DETAIL')
    article = Actual.objects.get(id=actual_id)
    print(article.title)
    return render(request, 'actual_detail.html', {
        'article': article})


class DetailView(View):
    def get(self, request, *args, **kwargs):
        print('GET')
        article = Actual.objects.get(id=kwargs['pk'])
        # form = PostForm()
        return render(request, 'actual_detail.html', {
            'article': article})

    def post(self, request, *args, **kwargs):
        print('POST', request.POST)
        article = Actual.objects.get(id=kwargs['pk'])
        article.content = request.POST['content']
        article.title = request.POST['title']
        article.save()
        return render(request, 'actual_detail.html', {
            'article': article})
