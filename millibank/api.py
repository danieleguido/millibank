import logging
from django.db.models import Q
from millibank.models import Project, Profile
from millibank.forms import ProjectForm
from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST
from glue.api import edit_object

logger = logging.getLogger('glue')


def home(request):
  '''
  Help or manual should be placed here
  '''
  result = Epoxy(request)
  return result.json()


def not_found(request):
  '''
  Help or manual should be placed here
  '''
  result = Epoxy(request)
  result.throw_error(code=API_EXCEPTION_DOESNOTEXIST)
  return result.json()


def profiles(request):
  result = Epoxy(request)
  result.queryset(Profile.objects.filter())
  return result.json()


def profile(request, username):
  result = Epoxy(request).single(Profile, {'user__username':username})
  return result.json()


def projects(request):
  result = Epoxy(request)
  result.queryset(Project.objects.filter())
  return result.json()


def project(request, slug):
  result = Epoxy(request)
  try:
    p = Project.objects.get(Q(slug=slug) | Q(pk=slug))
  except Project.DoesNotExist, e:
    return result.throw_error(code=API_EXCEPTION_DOESNOTEXIST).json()

  if result.is_GET():
    return result.item(p).json(deep=True)

  if not request.user.is_authenticated():
    # check ownerships or is_staffitude or is_author to enable it @todo
    return result.throw_error(code=API_EXCEPTION_AUTH).json()
    
  if result.is_POST():
    is_valid, p = edit_object(instance=p, Form=ProjectForm, request=request)
    if is_valid:
      p.save()
    else:
      return result.throw_error(error=p, code=API_EXCEPTION_FORMERRORS).json()

  return result.item(p).json() 

  