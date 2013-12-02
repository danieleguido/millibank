import csv, re, urllib2, json, urllib
from urllib2 import HTTPError

from django.conf import settings
from django.utils.text import slugify

OEMBED_URLS = [
  {
    'service': 'VIMEO',
    'urlpattern': 'vimeo\.com\/(\d+)$',
    'endpoint': 'https://vimeo.com/api/oembed.xml?format=json&url=http%3A//vimeo.com/__urlpattern__'
  },
  {
    'service': 'YOUTUBE',
    'urlpattern': 'youtube\.com[^\=]+\=([A-Za-z\d]+)$',
    'endpoint':'http://www.youtube.com/oembed?url=http%3A//youtube.com/watch%3Fv%3D__urlpattern__&format=json'
  }
]

def unicode_dict_reader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
      yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])


def uuslug(model, instance, value, max_length=128):
  '''

    Return an unique slug identifier for the given instance.
    only if the instance.slug DOES NOT EXIST!

    @param text - the text to be slugified 

  '''
  slug = slugify(value)[:max_length] # safe autolimiting
  slug_base = slug
  i = 1;

  while model.objects.filter(slug=slug).count():
    candidate = '%s-%s' % (slug_base, i)

    if len(candidate) > max_length:
      slug = slug[:max_length-len('-%s' % i)]

    slug = re.sub('\-+','-',candidate)
    i += 1

  return slug


def uutinyurl(value, max_length=8):
  return value[:max_length]


def oembed(url):
  '''
  understand which oembed service can be applied to download oembed data for the given url
  '''
  for service in OEMBED_URLS:
    match = re.search(service['urlpattern'], url)
    if match is not None:
      endpoint = '%s' % re.sub('__urlpattern__', match.group(1), service['endpoint'])
      #try:
      response = urllib2.urlopen(endpoint).read()
      return response
      #except HTTPError, e:
        #return '%s' % e
  return None
  