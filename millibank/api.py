import logging
from millibank.models import Project, Profile
from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

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
  result = Epoxy(request).single(Project, {'slug':slug})
  return result.json()