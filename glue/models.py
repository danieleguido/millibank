from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from glue import bibtex


class Geo( models.Model): # geo spot, with zoom
	lat = models.FloatField() # map center LAT
	lon = models.FloatField() # map center LON
	zoom = models.IntegerField() # start zoom
	content = models.TextField( default="", blank=True, null=True ) # textual GEO description

# class Tag( models.Model ):
class Tag(models.Model):

	# feel free to add tag type to this model ... :D
	AUTHOR = 'Au'
	KEYWORD = 'Ke'
	INSTITUTION = 'In'
	RESEARCHER = 'Rs'
	PLACE = 'Pl'
	DATE = 'Da'
	GEOCOVER = 'GC'


	TYPE_CHOICES = (
        (AUTHOR, 'AUTHOR'),
        (KEYWORD, 'KEYWORD'),
        (INSTITUTION, 'Institution'),
        (RESEARCHER, 'Researcher'),
        (PLACE, 'Place'),
        (DATE, 'Date'),
        (GEOCOVER, 'Geographic coverage')
    )

	name = models.CharField(max_length=128) # e.g. 'Mr. E. Smith'
	slug = models.SlugField(max_length=128) # e.g. 'mr-e-smith'
	type = models.CharField( max_length=2, choices=TYPE_CHOICES ) # e.g. 'author' or 'institution'

	def __unicode__(self):
		return "%s : %s"% ( self.get_type_display(), self.name)

	class Meta:
		ordering = ["type", "slug" ]
		unique_together = ("type", "slug")

class Pin( models.Model ):
	published='P'
	draft='D'

	PIN_STATUS_CHOICES = ( (published,"published"),(draft,"draft") )

	slug = models.SlugField()
	title = models.CharField( max_length=160, default="", blank=True, null=True )
	abstract = models.TextField( default="", blank=True, null=True )
	content = models.TextField( default="", blank=True, null=True )
	language =  models.CharField( max_length=2, default='EN', choices=settings.LANGUAGES ) # magic admin features: create a pin for the same language

	mimetype = models.CharField( max_length=255, default="", blank=True, null=True )
	sort =  models.IntegerField( default=0 )

	date = models.DateField( blank=True, null=True ) # main date, manually added
	date_last_modified = models.DateField( auto_now=True ) # date last save()

	local = models.FileField( upload_to='pins/%Y-%m/',  blank=True, null=True ) # local stored file
	permalink  = models.TextField( default="", blank=True, null=True ) # remote link

	related = models.ManyToManyField("self", symmetrical=True, null=True, blank=True)
	parent  = models.ForeignKey("self", null=True, blank=True, related_name="children" )
	status  = models.CharField( max_length=2, default="D",choices=PIN_STATUS_CHOICES)

	geos = models.ManyToManyField( Geo, blank=True, null=True ) # add geographic point
	tags = models.ManyToManyField( Tag, blank=True, null=True ) # add tags !
	users = models.ManyToManyField( User, blank=True, null=True )

	class Meta:
		unique_together = ( "slug", "language" )
		ordering = ('sort','-id')

	def __unicode__(self):
		return "%s (%s) a.k.a. %s" % (self.slug, self.language, self.title)

	# use this function if and only if the pin content is in bibtex (CLEAN) format
	def bib( self ):
		return bibtex( self.content )
		

	def json( self ):
		return{
			'id': self.id,
			'slug':self.slug,
			'title': self.title,
			'abstract': self.abstract,
			'content': self.content,
			'language': self.language,
			'mimetype': self.mimetype
		}





class PageAbstract( models.Model ):
	slug     =  models.SlugField()
	title    =  models.CharField( max_length=160, default="", blank=True, null=True )
	abstract =  models.TextField( default="", blank=True, null=True )
	content  =  models.TextField( default="", blank=True, null=True )
	
	language =  models.CharField( max_length=2, default='EN', choices=settings.LANGUAGES ) # magic admin features: create a pin for the same language
	sort     =  models.IntegerField( default=0 )
	
	class Meta:
		unique_together = ( "slug", "language" )
		abstract = True

	def __unicode__(self):
		return "%s (%s) a.k.a. %s" % (self.slug, self.language, self.title)
	def json( self ):
		return{
			'id': self.id,
			'slug':self.slug,
			'title': self.title,
			'abstract': self.abstract,
			'content': self.content,
			'language': self.language
		}

class Page( PageAbstract ):
	pins = models.ManyToManyField( Pin, null=True, blank=True, related_name="page")



class Serie( models.Model ):
	# note: Serie are not unique, but 
	MAIN = "Mn"
	GHOST = "Gh" # a non published serie ?
	SIBLING = "Sb" # a sibling

	TYPE_CHOICES = (
        (MAIN, 'main or default serie'), # normally editable only by staff
        (GHOST, 'ghost'),
        (SIBLING, 'sibling'),
    )

	slug     =  models.SlugField( )
	title    =  models.CharField( max_length=160, default="", blank=True, null=True )
	abstract =  models.TextField( default="", blank=True, null=True )
	content  =  models.TextField( default="", blank=True, null=True ) # a looong description
	sort  =  models.IntegerField( default=0 )

	type = models.CharField( max_length=2, choices=TYPE_CHOICES, default=SIBLING )

	date = models.DateField( blank=True, null=True ) # main date, manually added
	date_last_modified = models.DateField( auto_now=True ) # date last save()

	related = models.ManyToManyField("self", symmetrical=True, null=True, blank=True )
	frames = models.ManyToManyField( Pin, through='Frame', null=True, blank=True )
	users = models.ManyToManyField( User, blank=True, null=True ) # authors
	


class Frame( models.Model ):

	KEY = "Ke"
	GHOST = "Gh" # visible but just for reference.
	SIMPLE = "Sl" # visible but just for reference.

	TYPE_CHOICES = (
        (KEY, 'key frame'),
        (GHOST, 'ghost'),
        (SIMPLE, 'simple frame'),
    )

	pin = models.ForeignKey( Pin )
	serie = models.ForeignKey( Serie )
	sort  =  models.IntegerField( default=0 )
	
	type = models.CharField( max_length=2, choices=TYPE_CHOICES, default=SIMPLE  )

	abstract =  models.TextField( default="", blank=True, null=True ) # a description of the passage

	class Meta:
		unique_together = ( "serie", "sort" )
		ordering = ('sort', )