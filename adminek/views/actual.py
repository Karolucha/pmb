from django.shortcuts import render
from django.views import View

from app.models import Actual

ACTIONS = [{
  'name': 'Aktualności',
  'object_name': 'Actual'
}, {
  'name': 'Godziny działania kancelari',
  'object_name': 'OfficeHours'
}, {
  'name': 'Sakramenty lista',
  'object_name': 'Sacrament'
}]

def index(request):
    return render(request, 'index2.html', {'actions': ACTIONS})


def actual_list(request):
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




class ActualDetailView(View):
    def get(self, request, *args, **kwargs):
        # object_name = kwargs['object_name']
        # model_class = apps.get_model(app_label='app',model_name=object_name)
        if kwargs['pk'] is None:
            return render(request, 'actual_new.html')
        article = Actual.objects.get(id=kwargs['pk'])
        return render(request, 'actual_detail.html', {
            'article': article})

    def post(self, request, *args, **kwargs):
        if kwargs['pk'] is None:
            article = Actual(content=request.POST['content'],
                             title=request.POST['title'])
        elif request.POST.get('delete'):
            article = Actual.objects.get(id=kwargs['pk'])
            article.delete()
        else:
            article = Actual.objects.get(id=kwargs['pk'])
            article.content = request.POST['content']
            article.title = request.POST['title']
        article.save()
        return render(request, 'actual_detail.html', {
            'article': article})
