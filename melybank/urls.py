from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'walt.views.home', name='walt_home'),

    
    # login / logout
    url(r'^logout/$', 'logout_view', name='walt_logout'),
    url(r'^login/$', 'login_view', name='walt_login'),
    url(r'^ouch/$', 'not_found', name='not_found'),

    url(r'^admin/', include(admin.site.urls)),

    #storage
    url(r'^s/(?P<folder>[a-zA-Z\d\-]+)/(?P<index>[a-z\-_]+)\.(?P<extension>[a-z\d]+)/$', 'storage', name='walt_storage'), #i.e. proxy to storage space

    #walt categories
    url(r'^(?P<walt_category>[a-z])/(?P<slug>[a-zA-Z\-\d]+)$', 'walt.views.browse', name='walt_browse'),



)
