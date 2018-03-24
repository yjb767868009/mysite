import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

register = template.Library()
 
# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=48):
    default = "https://example.com/static/images/defaultavatar.jpg"
    return ("//www.gravatar.com/avatar/%s?%s&d=mm" %
            (hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
             urlencode({'s': str(size)})))
 
# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=48):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" width="%d" height="%d">' % (url, size, size))


