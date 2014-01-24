from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import millibank
#from glue.urls import glue_api_urlpatterns

apipatterns = patterns('millibank.api',
  url(r'^$', 'home', name='millibank_api_home'),
  url(r'^profile/$', 'profiles', name='millibank_api_profiles'),
  url(r'^profile/(?P<username>[:a-zA-Z\-\.\d]+)/$', 'profile', name='millibank_api_profile'),
  url(r'^project/$', 'projects', name='millibank_api_projects'),
  url(r'^project/(?P<slug>[:a-zA-Z\-\.\d]+)/$', 'project', name='millibank_api_project'),
  url(r'^.*$', 'not_found', name='millibank_api_not_found'),
)

urlpatterns = patterns('',
    url(r'^$', 'millibank.views.home', name='millibank_home'),
    url(r'^u/(?P<username>[a-zA-Z_\-\.\d]+)/$', 'millibank.views.portfolio', name='millibank_portfolio'),
    url(r'^p/add/$', 'millibank.views.project_add', name='millibank_project_add'),
    url(r'^p/(?P<slug>[a-zA-Z_\-\.\d]+)/$', 'millibank.views.project', name='millibank_project'),
    
    # login / logout
    url(r'^logout/$', 'millibank.views.logout_view', name='millibank_logout'),
    url(r'^login/$', 'millibank.views.login_view', name='millibank_login'),
    url(r'^ouch/$', 'millibank.views.not_found', name='millibank_not_found'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^glue/', include('glue.urls')),
    url(r'^api/', include(apipatterns)),
    # millybank categories
    # url(r'^(?P<millibank_category>[a-z])/(?P<slug>[a-zA-Z\-\d]+)$', 'millibank.views.browse', name='millibank_browse'),
)
