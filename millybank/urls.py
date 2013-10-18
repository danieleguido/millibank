from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'millybank.views.home', name='millybank_home'),

    # login / logout
    url(r'^logout/$', 'millybank.views.logout_view', name='millybank_logout'),
    url(r'^login/$', 'millybank.views.login_view', name='millybank_login'),
    url(r'^ouch/$', 'millybank.views.not_found', name='not_found'),

    url(r'^admin/', include(admin.site.urls)),

    # millybank categories
    url(r'^(?P<millybank_category>[a-z])/(?P<slug>[a-zA-Z\-\d]+)$', 'millybank.views.browse', name='millybank_browse'),

)
