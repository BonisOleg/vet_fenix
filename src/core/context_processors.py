from django.conf import settings
from django.core.cache import cache

from core.block_defaults import VISIBILITY_SUFFIX
from core.models import SiteBlock, SiteSettings
from core.site_nav import build_home_body_modifiers, get_visible_nav_items

SITE_BLOCKS_CACHE_KEY = 'vet_site_blocks_v1'
SITE_BLOCKS_CACHE_TTL = 0 if settings.DEBUG else 60


def invalidate_site_blocks_cache() -> None:
    cache.delete(SITE_BLOCKS_CACHE_KEY)


def _load_site_blocks() -> dict[str, SiteBlock]:
    use_cache = not settings.DEBUG and SITE_BLOCKS_CACHE_TTL > 0
    if use_cache:
        cached = cache.get(SITE_BLOCKS_CACHE_KEY)
        if cached is not None:
            return cached

    blocks = {block.cache_key: block for block in SiteBlock.objects.filter(is_active=True)}

    visibility_blocks = SiteBlock.objects.filter(key__endswith=VISIBILITY_SUFFIX)
    for block in visibility_blocks:
        blocks[block.cache_key] = block

    if use_cache:
        cache.set(SITE_BLOCKS_CACHE_KEY, blocks, SITE_BLOCKS_CACHE_TTL)
    return blocks


def site_settings(request):
    return {
        'site': SiteSettings.load(),
        'site_blocks': _load_site_blocks(),
    }


def static_asset_version(request):
    return {'static_version': settings.STATIC_ASSET_VERSION}


def navigation(request):
    active_nav = 'home'
    match = getattr(request, 'resolver_match', None)
    if match and match.namespace == 'clinic' and match.url_name:
        active_nav = match.url_name
    elif match and match.namespace == 'bookings':
        active_nav = 'booking'

    site_blocks = _load_site_blocks()
    is_home = match and match.namespace == 'clinic' and match.url_name == 'home'

    return {
        'active_nav': active_nav,
        'site_nav_primary': get_visible_nav_items(site_blocks),
        'site_nav_bottom': get_visible_nav_items(site_blocks, bottom=True),
        'body_modifiers': build_home_body_modifiers(site_blocks) if is_home else '',
    }
