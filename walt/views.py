import logging

from django.db.models import Q
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from glue.forms import LoginForm, AddPinForm, EditPinForm, AddSerieForm
from glue.models import Pin, Page, Serie


logger = logging.getLogger('glue')

# slugs of walt pages.
WALT_W = 'wander'
WALT_A = 'augment'
WALT_L = 'learn'
WALT_T = 'try'
WALT_PAGES = [ WALT_W, WALT_A, WALT_L, WALT_T ]

WALT_PAGES_ABSTRACT ={
	WALT_W: _('put here random element, usually blog posts or your own content'),
	WALT_A: _('put here content having iframe, like vimeo videos or soundcloud audio'),
	WALT_L: _('put here articles, papers and books'),
	WALT_T: _('put here tools and applications'),
}

# 
#	SHARED, commont context (tags, language, user availability...)
#
def sc( request, tags=[], d={}, load_walt=True, username=None ):
	
	# startup
	d['tags'] = tags
	d['language'] = get_language()
	d['languages'] = dict( settings.LANGUAGES )
	d['warnings'] = {}
	d['exception'] = False
	d['walt'] = {}
	d['spiff'] = ""
	
	d['filters'] = {}
	if username is not None:
		d['spiff'] = username
		d['filters']['authors__username'] = username

	try:
		if load_walt:
			for page_slug in WALT_PAGES:

				d['walt'][ page_slug ] = {
					'page': Page.objects.get( language=d['language'], slug=page_slug ),
					'pins': Pin.objects.filter(  language=d['language'], page__slug=page_slug ).filter( **d['filters'] )
				}
	except Page.DoesNotExist,e:
		d['exception'] = e
		
	# d['walt'] = dict([(p.slug,p) for p in Page.objects.filter( language=d['language'], slug__in=WALT_PAGES ) ] ) if load_walt else {}
	

	# load edit mode
	d['login_form'] = LoginForm( auto_id="id_login_%s")
	d['add_pin_form'] = AddPinForm( auto_id="id_add_pin_%s")
	d['add_serie_form'] = AddSerieForm( auto_id="id_add_serie_%s")

	return d



def login_view( request ):
	
	form = LoginForm( request.POST )
	next = request.REQUEST.get('next', 'walt_home')

	login_message = { 'next': next if len( next ) else 'walt_home'}

	if request.method != 'POST':
		data = sc( request, tags=[ "index" ], d=login_message )
		return render_to_response('walt/login.html', RequestContext(request, data ) )
	
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


	data = sc( request, tags=[ "index" ], d=login_message )


	return render_to_response('walt/login.html', RequestContext(request, data ) )

def logout_view( request ):
	logout( request )
	return redirect( 'walt_home' )



def home( request ):
	data = sc( request, tags=[ "home" ] )
	data['series'] = Serie.objects.filter( language=data['language'] ).order_by( '-date_last_modified','-id' )


	if request.user.is_authenticated():
		
		serie = Serie.objects.filter( language=data['language'], authors=request.user ).order_by( '-date_last_modified','-id' )[:1]

		data['workon_serie'] = serie
	else:
		data['workon_serie'] = None
	# has last serie
	
	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

@login_required
def spiff( request, username ):
	data = sc( request, tags=[ "home" ], username=username )

	

	data['series'] = Serie.objects.all()

	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

@login_required
def tag( request, tag_type, tag_slug ):
	data = sc( request, tags=[ "tags" ] )
	
	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

@login_required
def pin( request, pin_slug ):
	data = sc( request, tags=[ "pin" ] )
	data['pin'] = get_object_or_404( Pin, language=data['language'], slug=pin_slug )
	data['series'] = Serie.objects.filter( frames__pin__slug=pin_slug ).distinct()
	
	return render_to_response(  "walt/pin.html", RequestContext(request, data ) )

@login_required
def serie( request, serie_slug ):
	data = sc( request, tags=[ "serie" ] )
	data['serie'] = get_object_or_404( Serie, slug=serie_slug, language=data['language'] )
	
	return render_to_response(  "walt/serie.html", RequestContext(request, data ) )


def _walt( data, slug, username ):
	data['page'] = get_object_or_404( Page, language=data['language'], slug=slug )
	
	data['pins'] = Pin.objects.filter(  language=data['language'], page__slug=slug ).filter( **data['filters'] )

	# top series (series using )

	data['series'] = Serie.objects.filter( frames__pin__page__slug=slug ).distinct()
	
	return data

@login_required
def waltw( request, username=None ):
	data = sc( request, tags=[ "w" ] )
	data = _walt( data, WALT_W, username )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

@login_required
def walta( request, username=None ):
	data = sc( request, tags=[ "a" ] )
	data = _walt( data, WALT_A, username )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

@login_required
def waltl( request, username=None ):
	data = sc( request, tags=[ "l" ] )
	data = _walt( data, WALT_L, username )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

@login_required
def waltt( request, username=None ):
	data = sc( request, tags=[ "t" ] )
	data = _walt( data, WALT_T, username )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

# call this function once. It will check for page availability and other stories...
@staff_member_required
def setup( request ):
	data = sc( request, tags=[ "home" ], load_walt=False )
	logger.info('setup view called')

	logger.info('check for GLUE editor group...')
	try:
		g = Group.objects.get( name='GLUE EDITORS' )
		logger.info( "group name='%s' exists" % 'GLUE EDITORS' )
	except Group.DoesNotExist, e:
		g = Group( name='GLUE EDITORS' )
		g.save()
		logger.info( "group name='%s' created" % 'GLUE EDITORS' )
		request.user.groups.add( g )
		logger.info( "staff user name='%s' added to group '%s'" % ( request.user.username, 'GLUE EDITORS' ) )
		

	if len( data['languages'] )< 2:
		data['warnings']['languages'] = _("not enough languages")
		logger.warning("not enough languages (at least 2). Check local_settings.py LANGUAGES tuple!")
		return render_to_response(  "walt/index.html", RequestContext(request, data ) )

	if len( data['languages'] ) > 8:
		data['warnings']['languages'] = _("too many languages")
		logger.warning("too many languages (max 8). Check local_settings.py LANGUAGES tuple!")
		
		return render_to_response(  "walt/index.html", RequestContext(request, data ) )

	logger.info('check for WALT pages...')

	for slug in WALT_PAGES:
		for l in data['languages']:
			
			try:
				p = Page.objects.get( slug=slug, language=l )
				logger.info( "slug='%s', language: %s exists" % ( slug,l ) )
			except Page.DoesNotExist, e :
				p = Page( title=slug, language=l, slug=slug, abstract=WALT_PAGES_ABSTRACT[ slug ])
				p.save()
				logger.info( "slug='%s', language: %s created" % ( slug, l ) )

	logger.info('setup completed!')
	return home( request )

