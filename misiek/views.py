from django.shortcuts import render
from django.views import View
from django.views import generic

from app.models import Actual
def get_context():
    return {
        'list': 'admin'
    }

ACTIONS = [
{
  'name': 'Aktualności',
  'link': 'actual'
},
{
  'name': 'Godziny działania kancelari',
  'link': 'cancelary'
}
]


def index(request):
    print('my index')

    return render(request, 'index2.html', {'actions': ACTIONS})


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


def actual_delete(request, actual_id):
    article = Actual.objects.get(id=actual_id)
    if request.POST:
        article.delete()
        return render(request, 'index2.html', {'actions': ACTIONS})
    else:
        return render(request, 'actual_delete.html', {
            'article': article})


class DetailView(View):
    def get(self, request, *args, **kwargs):
        print('GET', kwargs['pk'], kwargs['pk'] == 0)
        if kwargs['pk'] is None:
            return render(request, 'actual_new.html')

        print('not new')
        article = Actual.objects.get(id=kwargs['pk'])
        # form = PostForm()
        return render(request, 'actual_detail.html', {
            'article': article})

    def post(self, request, *args, **kwargs):
        print('POST', request.POST)
        if kwargs['pk'] is None:
            article = Actual(content=request.POST['content'],
                             title=request.POST['title'])
        # elif request.POST.get('delete'):
        #     article = Actual.objects.get(id=kwargs['pk'])
        #     article.delete()
        else:
            article = Actual.objects.get(id=kwargs['pk'])
            article.content = request.POST['content']
            article.title = request.POST['title']
        article.save()
        return render(request, 'actual_detail.html', {
            'article': article})
