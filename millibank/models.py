import re, os, hashlib, logging
from datetime import datetime
from markdown import markdown

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import utc

from millibank.utils import uuslug, uutinyurl, oembed


logger = logging.getLogger('glue')

class Tag(models.Model):
  '''

  Millibank projects simple and FLAT tag system
  ---
  '''
  name = models.CharField(max_length=160, default="")
  slug = models.SlugField(max_length=160, unique=True)

  def __unicode__(self):
    return "%s"% (self.name)

  def save(self, **kwargs):
    self.slug = uuslug(model=Tag, instance=self, value=self.name)
    super(Tag, self).save()



class Cling(models.Model):
  '''

  The millibank atom
  ---

  '''
  url  = models.TextField() # remote link. Obbligatorio !
  url_hash  = models.CharField(unique=True, max_length=64, null=True, blank=True) # easy index for url. Not unique, but rare enough...
  
  oembed  = models.TextField(default="", null=True, blank=True) # oembed json as plain text. Compiled automatically!!
  description  = models.TextField(default="", null=True, blank=True) # a short description, as to speak.
  
  owner = models.ForeignKey(User) # the first digger ;D
  diggers = models.ManyToManyField(User, blank=True, null=True, related_name="shared_clings") # co-authors co-owners
  
  value = models.IntegerField(default=1, blank=True) # number of diggers, without doing any JOIN. updated on save.

  date_created = models.DateTimeField(default=datetime.now, blank=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  def json(self):
    d = _shared_json(self)
    d.update({
      'url': self.url,
      'url_hash': self.url_hash,
      'oembed' : self.oembed,
      'description': self.description,
      'owner': _shared_user(self.owner),
    })
    return d

  def __unicode__(self):
    return "%s (%s)"% (self.url, self.value)

  
  def save(self, **kwargs):
    self.url_hash = hashlib.sha224(self.url).hexdigest()
    if self.pk is not None:
      self.value = self.diggers.count()
      logger.info('update instance diggers to %s' % self.value)
      
      
      super(Cling, self).save()
    self.oembed = oembed(self.url)
    super(Cling, self).save()


class Me(models.Model):
  '''

  A Millibank Entity - or just extension of the self
  ---

  A Me is a shareable objects, that is you have to define the contributors
  '''
  PUBLIC  = 'P'
  DRAFT   = 'D'

  STATUS_CHOICES = (
    (PUBLIC, 'public'),
    (DRAFT, 'draft'),
  )

  title = models.CharField(max_length=160, default="")
  slug = models.SlugField(max_length=160, unique=True)

  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, blank=True, null=True)

  owner = models.ForeignKey(User, related_name="mes")
  contributors = models.ManyToManyField(User, blank=True, null=True, related_name="shared_mes", through='Me_User') # co-authors co-owners
  
  clings = models.ManyToManyField(Cling, through='Me_Cling')

  date_created = models.DateTimeField(default=datetime.now, blank=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return "%s"% (self.title)

  def save(self, **kwargs):
    self.slug = uuslug(model=Me, instance=self, value=self.title)
    super(Me, self).save()


class Me_User(models.Model):
  '''

  Millibank Entity Users:
  ---
  '''
  me = models.ForeignKey(Me)
  user = models.ForeignKey(User)
  role = models.CharField(max_length=160, default="", blank=True)


class Me_Cling(models.Model):
  '''

  Millibank Entity Alter-Egos
  ---

  '''
  me = models.ForeignKey(Me)
  cling = models.ForeignKey(Cling)
  position = models.IntegerField(default=0) # last 0 added is the me "cover" cling

  date_created = models.DateTimeField(default=datetime.now, blank=True)


class Project(models.Model):
  '''

  Millibank Project, a serie of Me
  ---

  '''
  PUBLIC  = 'P'
  DRAFT   = 'D'

  STATUS_CHOICES = (
    (PUBLIC, 'public'),
    (DRAFT, 'draft'), # draft is viewable/editable by authors and owner only.
  )

  title = models.CharField(max_length=128)
  slug = models.SlugField(max_length=128, unique=True, blank=True)

  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, blank=True, null=True)

  owner = models.ForeignKey(User) # the original owner. Contributors are contributor to the project's me!
  position = models.IntegerField(default=0) # the position in the user projects!

  mes = models.ManyToManyField(Me, through='Project_Me', null=True, blank=True)
  tags = models.ManyToManyField(Tag, null=True, blank=True)

  date_created = models.DateTimeField(auto_now_add=True, blank=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return "%s (by %s)"% (self.title, self.owner.username)

  def clings(self):
    '''
    global clings counter
    '''
    pass

  def json(self, deep=False):
    # divide tags according to type
    
    return{
      'id': self.id,
      'slug':self.slug,
      'status': self.get_status_display(),
      'title': self.title,
      'owner': self.owner.username,
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified is not None else None
    }

  def save(self, **kwargs):
    self.slug = uuslug(model=Project, instance=self, value=self.title)
    super(Project, self).save()


class Project_Me(models.Model):
  '''

  THe serie of Millibank Entity constituing a project
  ---

  '''
  project = models.ForeignKey(Project)
  me = models.ForeignKey(Me)
  position = models.IntegerField(default=0) # last 0 added is the me "cover" cling

  date_created = models.DateTimeField(default=datetime.now, blank=True)


class Profile(models.Model):
  '''
  
  Millibank way to handle users. Add some bio specific fields
  ---

  '''
  user = models.ForeignKey(User, unique=True)
  picture = models.ForeignKey(Cling) # the picture given as cling
  bio = models.TextField()
  excerpt = models.TextField() # a hand crafted summary, in markdown

  def __unicode__(self):
    return "%s (%s %s)"% (self.user.username, self.user.first_name, self.user.last_name)

  def json(self):
    d = _shared_json(self)
    d.update({
      #'url': reverse('millibank_api_profile', kwargs={'username': self.user.username}),
      'picture': self.picture.url,
      'excerpt' : markdown(self.excerpt),
      'bio': markdown(self.bio),
      'user': _shared_user(self.user),
    })
    return d

def _shared_json(item):
  '''
  Return a common json object for api invoc.
  '''
  d = {
    'id': item.id
  }

  if hasattr(item,'date_created'):
    d['date_created'] = item.date_created.isoformat()

  if hasattr(item,'date_last_modified'):
    d['date_last_modified'] = item.date_last_modified.isoformat()

  return d


def _shared_user(user):
  '''
  Return a common json object for a User api invoc.
  '''
  d = {
    'id': user.id,
    'fullname': user.username,
    'username': user.username
  }
  return d
