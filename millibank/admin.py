from django.contrib import admin
from millibank.models import Cling, Me_Cling, Me, Project_Me, Project


class Project_MeInline(admin.TabularInline):
    model = Project_Me
    extra = 1

class Me_ClingInline(admin.TabularInline):
    model = Me_Cling
    extra = 1

class ClingAdmin(admin.ModelAdmin):
  search_fields = ['url']
  readonly_fields=('url_hash', 'value',)

class MeAdmin(admin.ModelAdmin):
  search_fields = ['title']
  readonly_fields=('slug',)
  inlines = (Me_ClingInline,)


class ProjectAdmin(admin.ModelAdmin):
  search_fields = ['title']
  readonly_fields=('slug',)
  inlines = (Project_MeInline,)




admin.site.register(Cling, ClingAdmin)

admin.site.register(Me, MeAdmin)
admin.site.register(Project, ProjectAdmin)

