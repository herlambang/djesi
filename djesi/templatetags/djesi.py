import sys

from django.conf import settings
from django import template
from django.core.urlresolvers import resolve, reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def esi(context, view_name, *args, **kwargs):
    if not 'request' in context:
        raise Exception('ESI template tag requires request context to be activated')

    request     = context['request']
    url         = reverse(view_name, args=args, kwargs=kwargs)

    if getattr(settings, 'USE_ESI', settings.DEBUG):
        url         = request.build_absolute_uri(url)
        content = '<esi:include src="{url}"/>'.format(url=url)
    else:
        viewfunc, viewargs, viewkwargs = resolve(url)
        response    = viewfunc(request, args, kwargs)
        content     = response.content
    return content



