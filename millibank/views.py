import logging, os, urllib

from django.conf import settings
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from millibank.forms import LoginForm
from millibank.models import Project

from millibank import local_settings

logger = logging.getLogger(__name__)


def home(request):
  data = _shared_data( request, tags=['home'] )

  if request.user.is_authenticated():
    return me_public(request, username=request.user.username, data=data)

  return render_to_response(  "millibank/index.html", RequestContext(request, data ) )


def author(request, username):
  data = _shared_data( request, tags=['author'] )
  data['projects'] = Project.objects.filter(owner__username=username)

  return render_to_response(  "millibank/author.html", RequestContext(request, data ) )


@login_required(login_url=settings.LOGIN_URL)
def me_public(request, username, data):
  if data is None:
    data = _shared_data( request, tags=['home'] )

  data['projects'] = Project.objects.filter(Q(owner__username=username)|Q(authors__username=username))

  return render_to_response(  "millibank/me.html", RequestContext(request, data ) )

def browse(request, millibank_section, slug):
  '''

  Display Project tagged as millibank: WANDER
  =======================================

  '''
  data = _shared_data(request, tags=[millibank_section, slug])
  data['projects'] = Project.objects.filter(tags__type=millibank_section, tags__slug=slug)

  return render_to_response(  "millibank/browse.html", RequestContext(request, data ) )


def storage( request, folder=None, index=None, extension=None ):
  '''
	  
	Storage
	=======

	Direct storage solution. You only have to login. extension are given as first arg

	'''
  data = _shared_data(request, tags=['me'])

  storage_path = settings.STORAGE_ROOT_PROTECTED if request.user.is_authenticated() else settings.STORAGE_ROOT_PUBLIC 

  filepath = os.path.join(storage_path, folder, "%s.%s" % (index,extension));

  if os.path.exists(filepath):
    from django.core.servers.basehttp import FileWrapper
    from mimetypes import guess_type

    content_type = guess_type(filepath)

    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper, content_type=content_type[0])
    response['Content-Length'] = os.path.getsize(filepath)
    return response


  data['filepath'] = {
    'folder':folder,
    'index':index,
    'extension':extension,
    'total': filepath,
    'content-type':  guess_type( filepath )[0],
    'exists': os.path.exists( filepath )
  }
  
  return render_to_response(  "millibank/404.html", RequestContext(request, data ) )


def _shared_data( request, tags=[], d={} ):
  d['tags'] = tags
  d['debug'] = settings.DEBUG
  d['MILLIBANK_NAME'] = settings.MILLIBANK_NAME
  return d


def login_view( request ):
  if request.user.is_authenticated():
    return home( request )

  form = LoginForm( request.POST )
  next = request.REQUEST.get('next', 'millibank_home')

  login_message = { 'next': next if len( next ) else 'millibank_home'}

  if request.method != 'POST':
    data = _shared_data( request, tags=[ "login" ], d=login_message )
    return render_to_response('millibank/login.html', RequestContext(request, data ) )

  if form.is_valid():
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
      if user.is_active:
        login(request, user)
        # @todo: Redirect to next page

        return redirect( login_message['next'] )
      else:
        login_message['error'] = _("user has been disabled")
    else:
      login_message['error'] = _("invalid credentials")
      # Return a 'disabled account' error message
  else:
    login_message['error'] = _("invalid credentials")
    login_message['invalid_fields'] = form.errors
  
  data = _shared_data( request, tags=[ "login" ], d=login_message )
  return render_to_response('millibank/login.html', RequestContext(request, data ) )


def logout_view( request ):
  logout( request )
  return redirect( 'millibank_home' )


def not_found( request ):
  return render_to_response(  "millibank/404.html", RequestContext(request, {} ) )
