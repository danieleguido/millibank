from django.contrib import admin
from glue.models import Page, Pin, Tag, Serie, Frame


class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']


admin.site.register( Page )
admin.site.register( Pin )
admin.site.register( Tag, TagAdmin )
admin.site.register( Serie )
admin.site.register( Frame )