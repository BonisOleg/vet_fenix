import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    'stethoscope': (
        '<path d="M6 3v6a5 5 0 0010 0V3"/>'
        '<path d="M6 3h2M14 3h2"/>'
        '<path d="M11 14v2a4 4 0 008 0v-2"/>'
        '<circle cx="19" cy="11" r="2"/>'
    ),
    'syringe': (
        '<path d="M17 3l4 4"/><path d="M14 6l4 4"/>'
        '<path d="M18 8l-9 9-3 4-3-3 4-3 9-9"/>'
        '<path d="M10 12l3 3"/>'
    ),
    'scissors': (
        '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>'
        '<path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/>'
    ),
    'scan': (
        '<path d="M3 7V5a2 2 0 012-2h2M17 3h2a2 2 0 012 2v2M21 17v2a2 2 0 01-2 2h-2M7 21H5a2 2 0 01-2-2v-2"/>'
        '<path d="M7 12h10M9 8h6M9 16h6"/>'
    ),
    'tooth': (
        '<path d="M12 3c-3 0-7 1-7 5 0 3 1.2 5 1.8 9 .3 2 .9 3 1.7 3 '
        '1.2 0 1.5-3 2-5 .3-1.2.8-2 1.5-2s1.2.8 1.5 2c.5 2 .8 5 2 5 '
        '.8 0 1.4-1 1.7-3 .6-4 1.8-6 1.8-9 0-4-4-5-7-5z"/>'
    ),
    'video': (
        '<rect x="2" y="6" width="14" height="12" rx="2"/>'
        '<path d="M16 10l6-3v10l-6-3"/>'
    ),
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'star': '<path d="M12 2l3 6.5 7 1-5 5 1 7-6-3.5L6 21.5l1-7-5-5 7-1z"/>',
    'shield': (
        '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5l8-3z"/>'
        '<path d="M9 12l2 2 4-4"/>'
    ),
    'heart': '<path d="M3 12h4l2-5 3 9 2-4h7"/>',
    'phone': (
        '<path d="M22 16.92v3a2 2 0 01-2.18 2 19.86 19.86 0 01-8.63-3.07 '
        '19.5 19.5 0 01-6-6A19.86 19.86 0 012.13 4.18 2 2 0 014.11 2h3a2 2 0 '
        '012 1.72c.13 1.05.37 2.07.72 3.06a2 2 0 01-.45 2.11L8.09 10.91a16 16 '
        '0 006 6l2.02-2.02a2 2 0 012.11-.45c.99.35 2.01.59 3.06.72A2 2 0 0122 16.92z"/>'
    ),
    'caret': '<path d="M6 9l6 6 6-6"/>',
    'arrow-right': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'arrow-left': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'check': '<path d="M5 12l5 5L20 7"/>',
    'home': (
        '<path d="M3 10l9-7 9 7v10a2 2 0 01-2 2h-4v-7H9v7H5a2 2 0 01-2-2V10z"/>'
    ),
    'grid': (
        '<rect x="3" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="3" width="7" height="7" rx="1"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1"/>'
        '<rect x="14" y="14" width="7" height="7" rx="1"/>'
    ),
    'calendar': (
        '<rect x="3" y="5" width="18" height="16" rx="2"/>'
        '<path d="M3 10h18M8 3v4M16 3v4"/>'
    ),
    'pin': (
        '<path d="M12 22s-7-7-7-12a7 7 0 0114 0c0 5-7 12-7 12z"/>'
        '<circle cx="12" cy="10" r="2.5"/>'
    ),
    'user': (
        '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    'menu': (
        '<path d="M4 7h16M4 12h16M4 17h16"/>'
    ),
    'instagram': (
        '<rect x="2" y="2" width="20" height="20" rx="5"/>'
        '<circle cx="12" cy="12" r="4"/>'
        '<circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>'
    ),
    'telegram': (
        '<path d="M22 4L2 11l7 3 3 7 4-8 6-9z"/>'
        '<path d="M9 14l3 3"/>'
    ),
    'file': (
        '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/>'
        '<path d="M14 2v6h6"/>'
    ),
    'wallet': (
        '<rect x="2" y="6" width="20" height="14" rx="2"/>'
        '<path d="M2 10h20"/>'
        '<path d="M16 14h2"/>'
    ),
}


@register.simple_tag
def icon(name: str, size: int = 22, stroke: float = 2) -> str:
    del stroke  # stroke via .icon CSS
    paths = ICONS.get(name, '')
    if name == 'star':
        inner = '<path d="M12 2l3 6.5 7 1-5 5 1 7-6-3.5L6 21.5l1-7-5-5 7-1z"/>'
    else:
        inner = paths
    svg = (
        f'<svg class="icon icon--{name}" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" aria-hidden="true">{inner}</svg>'
    )
    return mark_safe(svg)


@register.filter
def address_short(value: str) -> str:
    """Short address for trust-strip, e.g. м. Київ, вул. X -> Київ, вул. X."""
    if not value:
        return ''
    text = str(value).strip()
    if text.lower().startswith('м. '):
        return text[3:]
    return text


@register.filter
def format_phone(value: str) -> str:
    """Format UA phone for display, e.g. +380441234567 -> +380 44 123 45 67."""
    if not value:
        return ''
    digits = re.sub(r'\D', '', str(value))
    if digits.startswith('380') and len(digits) == 12:
        return f'+{digits[:3]} {digits[3:5]} {digits[5:8]} {digits[8:10]} {digits[10:12]}'
    if len(digits) >= 10:
        return f'+{digits}'
    return str(value)
