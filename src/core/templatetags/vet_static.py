from django import template
from django.conf import settings
from django.templatetags.static import static as django_static

register = template.Library()


@register.simple_tag
def static_v(path: str) -> str:
    url = django_static(path)
    version = settings.STATIC_ASSET_VERSION
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}v={version}'
