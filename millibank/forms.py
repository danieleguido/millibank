import logging, hashlib

from django import forms
from django.db import IntegrityError
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from millibank.models import Project, Cling

logger = logging.getLogger('glue')


class LoginForm(forms.Form):
	username = forms.CharField( label=_('login'), max_length=64 )
	password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )


class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['owner', 'slug']


class ClingForm(forms.ModelForm):
  class Meta:
    model = Cling
    exclude = []

  def clean(self):
    if 'owner' not in self.cleaned_data:
      raise forms.ValidationError('euh.. the user?')
    owner = self.cleaned_data['owner']

    logger.info('cleaning url: "%s..." from user: %s' % (self.cleaned_data['url'][:15], owner))
    url_hash = hashlib.sha224(self.cleaned_data['url']).hexdigest()
    
    if self.instance is None or self.instance.url != self.cleaned_data['url'] or self.instance.owner != owner:

      try:
        alias = Cling.objects.get(url_hash=url_hash)
        alias.diggers.add(alias.owner)
        alias.diggers.add(owner)
        alias.save()
        raise forms.ValidationError('url already exist, given username has been added to clings %s' % alias.pk)
      except Cling.DoesNotExist,e:
        pass  
    
    return super(ClingForm, self).clean()

class CreateProjectForm(forms.Form):
  project_title = forms.CharField(label=_('project title, e.g Untitled'), max_length=128)
  me_title = forms.CharField(label=_('media title, e.g. Printed version'), max_length=128)
  cling_url = forms.CharField(label=_('Could you provide an url for the media?'), max_length=256)
  cling_description = forms.CharField(label=_('what does this url describe?'), max_length=256)
