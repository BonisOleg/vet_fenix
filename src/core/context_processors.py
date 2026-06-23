from django.conf import settings

from core.models import SiteSettings


def site_settings(request):
    return {'site': SiteSettings.load()}


def static_asset_version(request):
    return {'static_version': settings.STATIC_ASSET_VERSION}


def navigation(request):
    active_nav = 'home'
    match = getattr(request, 'resolver_match', None)
    if match and match.namespace == 'clinic' and match.url_name:
        active_nav = match.url_name
    elif match and match.namespace == 'bookings':
        active_nav = 'booking'
    return {'active_nav': active_nav}
