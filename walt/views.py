from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from glue.models import Pin, Page

# 
#	SHARED, commont context (tags, language, user availability...)
#
def sc( request, tags=[], d={} ):
	# startup
	d['tags'] = tags
	d['language'] = get_language()


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