from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from millibank.models import Project

class LoginForm(forms.Form):
	username = forms.CharField( label=_('login'), max_length=64 )
	password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )


class ProjectForm(ModelForm):
  class Meta:
    model = Project
    exclude = ['owner', 'slug']
