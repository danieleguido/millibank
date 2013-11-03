from django.contrib import admin
from millibank.models import Project, Me, Cling, Tag


class ClingAdmin(admin.ModelAdmin):
  search_fields = ['url']


class MeAdmin(admin.ModelAdmin):
  search_fields = ['title']


class ProjectAdmin(admin.ModelAdmin):
  search_fields = ['title']


class TagAdmin(admin.ModelAdmin):
  search_fields = ['name']


admin.site.register(Cling, ClingAdmin)
admin.site.register(Me, MeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
