from django import template
from django.contrib.auth.models import Group, Permission

register = template.Library()

@register.filter(name='is_editor')
def is_editor(user):
    """Check if user is an editor (staff member)"""
    if not hasattr(user, 'is_authenticated'):
        return False
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@register.filter(name='is_superuser')
def is_superuser(user):
    """Check if user is an admin (superuser)"""
    if not hasattr(user, 'is_authenticated'):
        return False
    return user.is_authenticated and (user.is_superuser)

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
