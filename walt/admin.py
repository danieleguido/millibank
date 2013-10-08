from django.contrib import admin
from walt.models import Document, Tag


class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']

class DocumentAdmin(admin.ModelAdmin):
	search_fields = ['title']

admin.site.register(Tag, TagAdmin)
admin.site.register(Document, DocumentAdmin)
