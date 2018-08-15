import os

from froala_editor import File, Image, S3

from froala_editor import DjangoAdapter, FlaskAdapter, PyramidAdapter

from django.http import HttpResponse
import json
from froala_editor import Image
from froala_editor import DjangoAdapter
import sys
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
# def index(request):
#     return render_to_response(os.path.join(settings.STATIC_DIR, 'common/index.html')
from pmb import settings


@csrf_exempt
def froala_view(request, *args, **kwargs):
    print('FROALA VIEW')
    print('UPLOADED!', request.POST)
    try:
        response = Image.upload(DjangoAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


# def froala_view(request, *args, **kwargs):
#     print('UPLOADED!', request.POST)


def load_images(request):
    try:
        response = Image.list('/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")

def get_image(request,*args,**kwargs):
    file_name = kwargs['name']
    extension = kwargs['extension']
    full_filename = "{}.{}".format(file_name, extension)
    # file = os.path.join(settings.STATIC_DIR, 'common/index.html')
    file = open(os.path.join('public', full_filename), "rb")
    # file = open(os.path.join('/public/'+file_name+ '.'+extension)
    return HttpResponse(file.read(), content_type="image/"+extension)
    # return HttpResponse(file, content_type="application/json")
