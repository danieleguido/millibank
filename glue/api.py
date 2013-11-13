import logging

from django.db.models.loading import get_model
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

logger = logging.getLogger('glue')


def index(request):
  '''
  Help or manual should be placed here
  '''
  result = Epoxy(request)
  return result.json()


def access_denied(request):
  '''
  Denial of access if user ios not staff.
  '''
  return Epoxy.error(request, message='access denied');


@staff_member_required
def get_objects(request, app_name, model_name):
  '''
  This is for debug purposes only. Please provide specific api method inside your own app.api.py file.
  '''
  try:
    m = get_model(app_name, model_name)
    
    queryset = m.objects.filter()
  except AttributeError, e:
    return Epoxy.error(request, message='model "%s" not found' % model_name, code='AttributeError')
  
  result = Epoxy(request).queryset(
    queryset,
    model=m
  )

  result.meta('module', '%s.%s' % (m.__module__, m.__name__))
  return result.json()


@staff_member_required
def get_object(request, app_name, model_name, pk):
  m = get_model(app_name, model_name)
  result = Epoxy(request).single(m, {'pk':pk})
  return result.json()