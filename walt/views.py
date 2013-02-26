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


from glue.models import Pin, Page


logger = logging.getLogger('glue')

# slugs of walt pages.
WALT_PAGES = ['wander','ask','learn','try']

# 
#	SHARED, commont context (tags, language, user availability...)
#
def sc( request, tags=[], d={} ):
	
	# startup
	d['tags'] = tags
	d['language'] = get_language()
	d['languages'] = dict( settings.LANGUAGES )
	d['warnings'] = {}

	d['walt'] = dict([(p.slug,p) for p in Page.objects.filter( language=d['language'], slug__in=WALT_PAGES ) ] )
	return d

def home( request ):
	data = sc( request, tags=[ "home" ] )

	return render_to_response(  "walt/index.html", RequestContext(request, data ) )
	try:
		data['page'] = Page.objects.get( slug="index", language=data['language'])
	except Page.DoesNotExist:
		p_en = Page( title="Home Page", language='EN', slug="index")
		p_en.save()

		p_fr = Page( title="Home Page", language='FR', slug="index")
		p_fr.save()

		data['page'] = p_fr if data['language'] == 'FR' else p_en

	# load all pins without page
	data['pins'] = Pin.objects.filter(language=data['language'], page__slug="index" ).order_by("-id")

	# get news
	data['news'] = Pin.objects.filter(language=data['language'], page__isnull=True ).order_by("-id")

	return render_to_response(  "walt/index.html", RequestContext(request, data ) )

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