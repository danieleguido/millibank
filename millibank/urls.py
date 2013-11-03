from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'millibank.views.home', name='millibank_home'),

    # login / logout
    url(r'^logout/$', 'millibank.views.logout_view', name='millibank_logout'),
    url(r'^login/$', 'millibank.views.login_view', name='millibank_login'),
    url(r'^ouch/$', 'millibank.views.not_found', name='not_found'),

    url(r'^admin/', include(admin.site.urls)),

    # millybank categories
    url(r'^(?P<millibank_category>[a-z])/(?P<slug>[a-zA-Z\-\d]+)$', 'millibank.views.browse', name='millibank_browse'),

)
