from django.contrib import admin
from millibank.models import Cling, Me_Cling, Me, Project_Me, Project, Profile
from millibank.forms import ClingForm


class Project_MeInline(admin.TabularInline):
    model = Project_Me
    extra = 1


class Me_ClingInline(admin.TabularInline):
    model = Me_Cling
    extra = 1


class ClingAdmin(admin.ModelAdmin):
  search_fields = ['url']
  readonly_fields=('url_hash', 'value', 'diggers',)
  form = ClingForm


class MeAdmin(admin.ModelAdmin):
  search_fields = ['title']
  readonly_fields=('slug',)
  inlines = (Me_ClingInline,)


class ProjectAdmin(admin.ModelAdmin):
  search_fields = ['title']
  readonly_fields=('slug',)
  inlines = (Project_MeInline,)


class ProfileAdmin(admin.ModelAdmin):
  search_fields = ['bio']

  '''  if self.pk is not None:
      # it is an update, check if the cling hasn't been modified
      cling = Cling.objects.get(pk=self.pk)
      require_checking = cling.url_hash != url_hash
      logger.info('    updating cling')
    
    if self.pk is None or require_checking:
      try:
        exhisting_cling = Cling.objects.get(url_hash=url_hash)
        
        
      except Cling.DoesNotExist, e: # add tranquilly
        exhisting_cling = None
        logger.exception(e)
        pass

      if exhisting_cling and exhisting_cling.owner != self.owner:
        logger.info('    exhisting_cling.owner != self.owner! %s' % exhisting_cling.diggers.count())
        exhisting_cling.diggers.add(self.owner)
        exhisting_cling.value = exhisting_cling.diggers.count()
        exhisting_cling.save()
        instance = exhisting_cling
  '''


admin.site.register(Cling, ClingAdmin)
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Me, MeAdmin)
admin.site.register(Project, ProjectAdmin)

