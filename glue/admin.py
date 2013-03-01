from django.contrib import admin
from glue.models import Page, Pin, Tag


class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']


admin.site.register( Page )
admin.site.register( Pin )
admin.site.register( Tag, TagAdmin )