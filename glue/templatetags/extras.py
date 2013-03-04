import re, json
from django import template

register = template.Library()




#
#    bib tex (raw)
#    =============
#
@register.filter
def bibtex( reference ):
	reference = re.sub('(\w+)\s*=\s*\{+',r'"\1":"', reference )
	reference = re.sub('\}+(?=\s*[,\}+])','"', reference )
	reference = re.sub('@(\w+)\s*\{([^,]*)',r'{"bibtext_key":"\2","\1": "\2"', reference )
	return json.loads( reference )