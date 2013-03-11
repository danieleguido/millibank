from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',

	url(r'^$', 'glue.api.index', name='glue_api_index'),

	url(r'^manage/(?P<model_name>[a-zA-Z_]+)/$', 'glue.api.manage_objects', name='glue_api_manage_objects'),
	url(r'^manage/(?P<model_name>[a-zA-Z_]+)/(?P<pk>\d+)$', 'glue.api.manage_single_object', name='glue_api_manage_single_object'),

	url(r'^test/$', 'glue.api.test', name='glue_api_test'), # get list, post single page

	url(r'^page/$', 'glue.api.pages', name='glue_api_pages'), # get list, post single page
	url(r'^page/(?P<page_id>\d+)/$', 'glue.api.page', name='glue_api_page'), 
	url(r'^page/(?P<page_slug>[a-zA-Z\d\-]+)/(?P<page_language>[a-zA-Z]{2})/$', 'glue.api.page_by_slug', name='glue_api_page_by_slug'),

	url(r'^pin/$', 'glue.api.pins', name='glue_api_pins'), # get list, post single page
	url(r'^pin/(?P<pin_id>\d+)/$', 'glue.api.pin', name='glue_api_pin'),
	url(r'^pin/(?P<pin_id>\d+)/tag/$', 'glue.api.pin_tags', name='glue_api_pin_tags'), 
	url(r'^pin/(?P<pin_id>\d+)/alchemy/$', 'glue.api.pin_alchemy', name='glue_api_pin_alchemy'), 
	url(r'^pin/(?P<pin_slug>[a-zA-Z\d\-]+)/(?P<pin_language>[a-zA-Z]{2})/$', 'glue.api.pin_by_slug', name='glue_api_pin_by_slug'), 
	url(r'^pin/(?P<pin_id>\d+)/publish/$', 'glue.api.publish_pin', name='glue_api_publish_pin'), 
	url(r'^pin/(?P<pin_id>\d+)/clean/$', 'glue.api.pin_clean', name='glue_api_pin_clean'), 
	url(r'^pin/upload/$', 'glue.api.pin_upload', name='glue_api_pin_upload'), 


	url(r'^serie/$', 'glue.api.series', name='glue_api_series'), # get list, post single serie
	url(r'^serie/(?P<serie_id>\d+)/$', 'glue.api.serie', name='glue_api_serie'), # get a signle serie WITHOUT its frame collection. POST to edit serie Data
	url(r'^serie/(?P<serie_id>\d+)/frames/$', 'glue.api.serie_frames', name='glue_api_serie_frames'), # get a signle serie along wiht its frame collection. POST to add frame...

	url(r'^frame/$', 'glue.api.frames', name='glue_api_frames'), # get list of frames per author (useless)
	url(r'^frame/(?P<frame_id>\d+)/$', 'glue.api.frame', name='glue_api_frame'), # GET: full information 


	url(r'^access-denied/', 'glue.api.access_denied', name='glue_api_access_denied'), 
)
