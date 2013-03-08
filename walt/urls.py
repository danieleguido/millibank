from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'walt.views.home', name='walt_home'),
    
    url(r'^setup/$', 'walt.views.setup', name='walt_setup'),
    url(r'^robots\.txt$', direct_to_template, {'template': 'walt/robots.txt', 'mimetype': 'text/plain'}),
    url(r'^humans\.txt$', direct_to_template, {'template': 'walt/humans.txt', 'mimetype': 'text/plain'}),
    url(r'^crossdomain\.xml$', direct_to_template, {'template': 'walt/crossdomain.xml', 'mimetype': 'text/xml'}),

    # login / logout
    url(r'^logout/$', 'walt.views.logout_view', name='walt_logout'),

    url(r'^login/$', 'walt.views.login_view', name='walt_login'),

    # url(r'^walt/', include('walt.foo.urls')),
    url(r'^api/', include('glue.urls')),

    url(r'^w/$', 'walt.views.waltw', name='walt_w'),
    url(r'^a/$', 'walt.views.walta', name='walt_a'),
    url(r'^l/$', 'walt.views.waltl', name='walt_l'),
    url(r'^t/$', 'walt.views.waltt', name='walt_t'),

    url(r'^w/(?P<username>[a-z\.]+)/$', 'walt.views.waltw', name='walt_w_spiff'),
    url(r'^a/(?P<username>[a-z\.]+)/$', 'walt.views.walta', name='walt_a_spiff'),
    url(r'^l/(?P<username>[a-z\.]+)/$', 'walt.views.waltl', name='walt_l_spiff'),
    url(r'^t/(?P<username>[a-z\.]+)/$', 'walt.views.waltt', name='walt_t_spiff'),
    
    url(r'^u/(?P<username>[a-z\.]+)/$', 'walt.views.spiff', name='walt_spiff'),

    url(r'^tag/(?P<tag_type>[a-z\-]+)/(?P<tag_slug>[a-zA-Z\d\-]+)/', 'walt.views.tag', name='walt_tag'),
    url(r'^serie/(?P<serie_slug>[a-zA-Z\_\d\-]+)/', 'walt.views.serie', name='walt_serie'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # all the rest. pins.
    url(r'^(?P<pin_slug>[a-zA-Z\d\-]+)/$', 'walt.views.pin', name='walt_pin'),
)
