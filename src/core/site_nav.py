from __future__ import annotations

from dataclasses import dataclass

from core.utils.block_render import is_section_visible

HOME_SECTION_VISIBILITY_KEYS = (
    'hero_section_visible',
    'advantages_section_visible',
    'services_preview_section_visible',
    'doctors_preview_section_visible',
)

CONTACTS_SECTION_VISIBILITY_KEYS = (
    'header_section_visible',
    'clinic_section_visible',
    'form_section_visible',
    'map_section_visible',
)

# Кнопка в шапці для Послуги/Лікарі: показати лише якщо увімкнені ВСІ повʼязані CMS-секції.
NAV_SECTION_GATES: dict[str, tuple[tuple[str, str], ...]] = {
    'home': tuple((('home', key) for key in HOME_SECTION_VISIBILITY_KEYS)),
    'services': (
        ('services', 'header_section_visible'),
        ('home', 'services_preview_section_visible'),
    ),
    'doctors': (
        ('doctors', 'header_section_visible'),
        ('home', 'doctors_preview_section_visible'),
    ),
    'contacts': tuple((('contacts', key) for key in CONTACTS_SECTION_VISIBILITY_KEYS)),
}


@dataclass(frozen=True)
class SiteNavItem:
    nav_id: str
    label: str
    url_name: str
    icon: str


PRIMARY_NAV_ITEMS: tuple[SiteNavItem, ...] = (
    SiteNavItem('home', 'Головна', 'clinic:home', 'home'),
    SiteNavItem('services', 'Послуги', 'clinic:services', 'grid'),
    SiteNavItem('doctors', 'Лікарі', 'clinic:doctors', 'user'),
    SiteNavItem('contacts', 'Контакти', 'clinic:contacts', 'pin'),
)

BOTTOM_NAV_ITEMS: tuple[SiteNavItem, ...] = (
    SiteNavItem('home', 'Головна', 'clinic:home', 'home'),
    SiteNavItem('services', 'Послуги', 'clinic:services', 'grid'),
    SiteNavItem('booking', 'Запис', 'bookings:booking', 'calendar'),
    SiteNavItem('doctors', 'Лікарі', 'clinic:doctors', 'user'),
    SiteNavItem('contacts', 'Контакти', 'clinic:contacts', 'pin'),
)


def _any_section_visible(keys: tuple[tuple[str, str], ...], site_blocks: dict | None) -> bool:
    if not keys:
        return False
    return any(is_section_visible(page, key, site_blocks=site_blocks or {}) for page, key in keys)


def _all_sections_visible(keys: tuple[tuple[str, str], ...], site_blocks: dict | None) -> bool:
    if not keys:
        return True
    return all(is_section_visible(page, key, site_blocks=site_blocks or {}) for page, key in keys)


def is_nav_item_visible(nav_id: str, site_blocks: dict | None = None) -> bool:
    if nav_id == 'booking':
        return True

    if nav_id in ('services', 'doctors'):
        return _all_sections_visible(NAV_SECTION_GATES[nav_id], site_blocks)

    gates = NAV_SECTION_GATES.get(nav_id)
    if not gates:
        return True

    return _any_section_visible(gates, site_blocks)


def get_visible_nav_items(
    site_blocks: dict | None = None,
    *,
    bottom: bool = False,
) -> tuple[SiteNavItem, ...]:
    items = BOTTOM_NAV_ITEMS if bottom else PRIMARY_NAV_ITEMS
    return tuple(item for item in items if is_nav_item_visible(item.nav_id, site_blocks))


def build_home_body_modifiers(site_blocks: dict | None = None) -> str:
    blocks = site_blocks or {}
    modifiers: list[str] = []

    if not is_section_visible('home', 'hero_section_visible', site_blocks=blocks):
        modifiers.append('site--no-hero')

    visible_sections = sum(
        1 for key in HOME_SECTION_VISIBILITY_KEYS if is_section_visible('home', key, site_blocks=blocks)
    )
    if 0 < visible_sections < len(HOME_SECTION_VISIBILITY_KEYS):
        modifiers.append('site--sections-compact')

    return ' '.join(modifiers)
