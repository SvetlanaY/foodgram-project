from django import template
from django.http import QueryDict

register = template.Library()


@register.filter(name='tag_values')
def tag_values(value):
    return value.getlist('filters')


@register.filter(name='tag_link')
def tag_link(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)
    return new_request.urlencode()
