from django import template
from groups.models import Group

register = template.Library()


@register.simple_tag
def get_groups():
    return Group.objects.filter(is_published=True)
