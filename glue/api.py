import logging

from django.db.models.loading import get_model
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm

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
  result = Epoxy(request)

  try:
    mod = get_model(app_name, model_name)
  except AttributeError, e:
    return result.throw_error(error='model "%s" not found' % model_name, code='AttributeError')
  
  if result.is_POST():
    class ObjForm(ModelForm):
      class Meta:
        model = mod
        exclude =()

    form = ObjForm(request.REQUEST)
    if form.is_valid():
      item = form.save(commit=False)
      result.add('item', item.json())
      item.save()
    else:
      return result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  queryset = mod.objects.filter()
  
  result.queryset(
    queryset,
    model=mod
  )

  result.meta('module', '%s.%s' % (mod.__module__, mod.__name__))
  return result.json()


@staff_member_required
def get_object(request, app_name, model_name, pk):
  result = Epoxy(request)
  mod = get_model(app_name, model_name)
  try:
    obj = mod.objects.get(pk=pk)
  except mod.DoesNotExist, e:
    return Epoxy.error(request, message="%s" % e, code=API_EXCEPTION_DOESNOTEXIST)
  
  

  if result.is_POST():
    class ObjForm(ModelForm):
      class Meta:
        model = mod
        exclude =()

    form = ObjForm(instance=obj, data=request.REQUEST)
    if form.is_valid():
      form.save(commit=False)
      obj.save()
    else:
      return result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
    result.add('item', obj.json())
  elif result.is_DELETE():
    obj.delete()
  else:
    result.add('item', obj.json())

  return result.json()