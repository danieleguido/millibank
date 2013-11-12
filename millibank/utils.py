import csv, re

from django.conf import settings
from django.utils.text import slugify


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