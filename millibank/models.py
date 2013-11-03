import re, os
from datetime import datetime
from markdown import markdown

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import utc

from millibank.utils import uuslug, uutinyurl


class Tag(models.Model):
  '''
    feel free to add tag types to this model ... :D
  '''
  
  FREE = '' # i.e, no special category at all
  PLACE = 'Pl'
  DATE = 'Da'
  SECTION = 'S' # project only
  
  TYPE_CHOICES = (
    (FREE, 'no category'),
    (PLACE, 'Place'),
    (DATE, 'Date'),
    (SECTION, 'SECTION'),
  )

  name = models.CharField(max_length=128) # e.g. 'Mr. E. Smith'
  slug = models.SlugField(max_length=128, unique=True) # e.g. 'mr-e-smith'
  type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=FREE) # e.g. 'author' or 'institution'
  
  related = models.ManyToManyField('self', symmetrical=False, null=True, blank=True) # tag specification e.g. we want to specify an institution for a given author
  
  def __unicode__(self):
    return "%s : %s"% (self.get_type_display(), self.name)

  class Meta:
    ordering = ["type", "slug" ]

  def json(self):
    return{
      'id': self.id,
      'slug':self.slug,
      'name':self.name,
      'type':self.type,
      'type_label':self.get_type_display()
    }

  def save(self, **kwargs):
    self.slug = uuslug(model=Tag, instance=self, value='%s-%s' % (self.type, self.name))
    super(Tag, self).save()


class Cling(models.Model):
  '''

  The millibank atom
  ---

  '''
  owner = models.ForeignKey(User) # the first owner ;D
  url  = models.TextField(default="") # remote link
  url_hash  = models.CharField(max_length=64) # easy index for url. Not unique, but ...
  tinyurl = models.CharField(max_length=8, unique=True) # database unique url

  def __unicode__(self):
    return "%s"% (self.url)

  def save(self, **kwargs):
    tinyurl = uutinyurl(value=self.url_hash)
    super(Cling, self).save()


class Me(models.Model):
  '''

  A Millibank Entity - or just extension of the self
  ---

  '''
  PUBLIC  = 'P'
  DRAFT   = 'D'

  STATUS_CHOICES = (
    (PUBLIC, 'public'),
    (DRAFT, 'draft'),
  )

  title = models.CharField(max_length=160, default="")
  content = models.TextField(default="", blank=True, null=True)
  slug = models.SlugField(max_length=160, unique=True)

  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, blank=True, null=True)

  owner = models.ForeignKey(User) # the original owner
  authors = models.ManyToManyField(User, blank=True, null=True, related_name="other_mes") # co-authors co-owners
  
  tags = models.ManyToManyField(Tag, blank=True, null=True)

  mirror = models.ForeignKey(Cling)
  clings = models.ManyToManyField(Cling, through='Alter', related_name="other_mes")

  date_last_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return "%s"% (self.title)

  def save(self, **kwargs):
    self.slug = uuslug(model=Me, instance=self, value=self.title)
    super(Me, self).save()


class Alter(models.Model):
  '''

  Millibank Entity Alter-Egos
  ---

  '''
  me = models.ForeignKey(Me)
  cling = models.ForeignKey(Cling)
  date_joined = models.DateTimeField(auto_now=True)
  position = models.IntegerField(default=-1,null=True, blank=True)


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
  content = models.TextField(default="", blank=True, null=True)
  slug = models.SlugField(max_length=128, unique=True)

  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, blank=True, null=True)

  owner = models.ForeignKey(User) # the original owner
  authors = models.ManyToManyField(User, blank=True, null=True, related_name="other_projects") # co-authors
  
  tags = models.ManyToManyField(Tag, blank=True, null=True)
  mes = models.ManyToManyField(Me, through='Serie')

  date_last_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return "%s"% (self.title)

  def clings(self):
    '''
    global clings counter
    '''
    pass

  def json(self, deep=False):
    # divide tags according to type
    tags = {}

    for t in self.tags.all():
      t_type = '%s'%t.get_type_display()
      if t_type not in tags:
        tags[t_type] = []
      tags[t_type].append(t.json())

    return{
      'id': self.id,
      'slug':self.slug,
      'status': self.get_status_display(),
      'title': self.title,
      'content': self.content,
      'owner': self.owner.username,
      'tags': tags,
      'type': self.type,
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified is not None else None,
      'authors': [a.username for a in self.authors.all()]

    }

  def save(self, **kwargs):
    self.slug = uuslug(model=Project, instance=self,value=self.title)
    super(Project, self).save()


class Serie(models.Model):
  '''

  THe serie of Millibank Entity constituing a project
  ---

  '''
  project = models.ForeignKey(Project)
  me = models.ForeignKey(Me)
  date_joined = models.DateTimeField(auto_now=True)
  position = models.IntegerField(default=-1,null=True, blank=True)


