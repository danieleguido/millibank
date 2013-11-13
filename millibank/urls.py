from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import millibank
#from glue.urls import glue_api_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'millibank.views.home', name='millibank_home'),
    url(r'^a/(?P<username>[a-zA-Z])/$', 'author', name='millibank_author'),
    # login / logout
    url(r'^logout/$', 'logout_view', name='millibank_logout'),
    url(r'^login/$', 'login_view', name='millibank_login'),
    url(r'^ouch/$', 'ot_found', name='millibank_not_found'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^glue/', include('glue.urls')),
    # millybank categories
    url(r'^(?P<millibank_category>[a-z])/(?P<slug>[a-zA-Z\-\d]+)$', 'millibank.views.browse', name='millibank_browse'),
)
