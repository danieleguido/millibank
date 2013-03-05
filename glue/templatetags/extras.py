import re, json
from django import template


register = template.Library()




#
#    bib tex (raw)
#    =============
#
@register.filter
def split( value, pattern=',' ):
	return re.split( pattern, value)