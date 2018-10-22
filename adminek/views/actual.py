from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from adminek.forms import SignUpForm
from adminek.tokens import account_activation_token
from app.models import Actual

ACTIONS = [{
  'name': 'Aktualności',
  'object_name': 'Actual'
}, {
  'name': 'Ogłoszenia duszpasterskie',
  'object_name': 'WeekAnnouncement'
}, {
  'name': 'Intencje',
  'object_name': 'IntentionWeek'
}, {
  'name': 'Godziny działania kancelarii',
  'object_name': 'OfficeHours'
}, {
  'name': 'Nabożeństwa',
  'object_name': 'Ceremony'
}, {
  'name': 'Msze święte',
  'object_name': 'MassSchema'
}, {
  'name': 'Galeria',
  'object_name': 'Galery'
}, {
  'name': 'Grupy działające',
  'object_name': 'ActivityGroup'
}, {
  'name': 'Sakramenty lista',
  'object_name': 'Sacrament'
}, {
  'name': 'Kościoły',
  'object_name': 'church'
}, {
  'name': 'Duszpasterze',
  'object_name': 'pastor'
}]

@login_required
def index(request):
    return render(request, 'index2.html', {'actions': ACTIONS})


def actual_list(request):
    actual_list_links = Actual.objects.all()
    return render(request, 'actual.html', {'actual_list_links': actual_list_links})


def actual_detail(request, actual_id):
    article = Actual.objects.get(id=actual_id)
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



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': 'PMB Jawor',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token': account_activation_token.make_token(user),
                'token': 's2err2t2%2',
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})