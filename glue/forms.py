from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.conf import settings
from glue.models import Tag, Serie, Frame

class LoginForm(forms.Form):
	username = forms.CharField( label=_('login'), max_length=64 )
	password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )


class AddPageForm(forms.Form):
	def __init__(self, *args, **kwargs):
		
		super(AddPageForm, self).__init__(*args, **kwargs)

		for l,lang in settings.LANGUAGES:
			self.fields['title_%s' % l] = forms.CharField( label=_("%s title" % lang), required=True )
			
	slug = forms.SlugField( required=True )


class AddSerieForm(forms.Form):
	def __init__(self, *args, **kwargs):
		
		super(AddSerieForm, self).__init__(*args, **kwargs)

		for l,lang in settings.LANGUAGES:
			self.fields['title_%s' % l] = forms.CharField( label=_("%s title" % lang), required=True )
			
	slug = forms.SlugField( required=True )

	type = forms.ChoiceField( label=_("type"), required=True, choices=Serie.TYPE_CHOICES )

class AddFrameForm(forms.Form):
	slug = forms.SlugField( required=True )
	type = forms.ChoiceField( label=_("type"), required=True, choices=Frame.TYPE_CHOICES )
	sort = forms.IntegerField( min_value=1 )

class AddPinForm(forms.Form):
	
	def __init__(self, *args, **kwargs):

		super(AddPinForm, self).__init__(*args, **kwargs)

		for l,lang in settings.LANGUAGES:
			self.fields['title_%s' % l] = forms.CharField( label=_("%s title" % lang), required=True )
            

	slug = forms.SlugField( required=True )
	
	permalink = forms.URLField( required=False )
	abstract = forms.CharField( label=_("abstract"), required=False, widget=forms.Textarea )
	content = forms.CharField( label=_("content"), required=False, widget=forms.Textarea )
	mimetype = forms.CharField( label=_("mimetype"), max_length=255, required=False, widget=forms.Textarea )

	page_slug = forms.SlugField( required=False, widget=forms.HiddenInput )
	parent_pin_slug = forms.SlugField( required=False, widget=forms.HiddenInput )

class EditPinForm(forms.Form):
	title = forms.CharField( label=_("title"),required=True )
	abstract = forms.CharField( label=_("abstract"), required=False, widget=forms.Textarea )
	content = forms.CharField( label=_("content"), required=False, widget=forms.Textarea )
	permalink = forms.URLField( required=False )

class UploadPinForm(forms.Form): # an upload form without file :D (upload via ajax)
	page_slug = forms.SlugField( required=False, widget=forms.HiddenInput )
	parent_pin_slug = forms.SlugField( required=False, widget=forms.HiddenInput )

class AddTagForm(forms.Form):
	name = forms.CharField( label=_("tag name"),required=True )
	slug = forms.SlugField( required=True )
	type = forms.CharField( label=_("type"), required=True, widget = forms.ChoiceField( widget=forms.Select, choices=Tag.TYPE_CHOICES ) )