import logging

from django.db.models import Q
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from glue.forms import LoginForm, AddPinForm, EditPinForm
from glue.models import Pin, Page, Serie


logger = logging.getLogger('glue')

# slugs of walt pages.
WALT_W = 'wander'
WALT_A = 'ask'
WALT_L = 'learn'
WALT_T = 'try'
WALT_PAGES = [ WALT_W, WALT_A, WALT_L, WALT_T ]

# 
#	SHARED, commont context (tags, language, user availability...)
#
def sc( request, tags=[], d={}, load_walt=True ):
	
	# startup
	d['tags'] = tags
	d['language'] = get_language()
	d['languages'] = dict( settings.LANGUAGES )
	d['warnings'] = {}
	
	if load_walt:
		d['walt'] = dict([(p.slug,p) for p in Page.objects.filter( language=d['language'], slug__in=WALT_PAGES ) ] )

	# load edit mode
	d['login_form'] = LoginForm( auto_id="id_login_%s")
	d['add_pin_form'] = AddPinForm( auto_id="id_add_pin_%s")

	return d

def home( request ):
	data = sc( request, tags=[ "home" ] )
	data['series'] = Serie.objects.all()

	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

def tag( request, tag_type, tag_slug ):
	data = sc( request, tags=[ "tags" ] )
	
	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

def _walt( data, slug ):
	data['page'] = get_object_or_404( Page, language=data['language'], slug=slug )
	data['series'] = Serie.objects.filter( frame__pin__page__slug=slug ).distinct()
	return data

def waltw( request ):
	data = sc( request, tags=[ "w" ] )
	data = _walt( data, WALT_W )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )
	
def walta( request ):
	data = sc( request, tags=[ "a" ] )
	data = _walt( data, WALT_A )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

def waltl( request ):
	data = sc( request, tags=[ "l" ] )
	data = _walt( data, WALT_L )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

def waltt( request ):
	data = sc( request, tags=[ "t" ] )
	data = _walt( data, WALT_T )
	return render_to_response(  "walt/walt.html", RequestContext(request, data ) )

# call this function once. It will check for page availability and other stories...
@staff_member_required
def setup( request ):
	data = sc( request, tags=[ "home" ] )
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
				p = Page( title=slug, language=l, slug=slug)
				p.save()
				logger.info( "slug='%s', language: %s created" % ( slug, l ) )

	logger.info('setup completed!')
	return render_to_response(  "walt/index.html", RequestContext(request, data ) )