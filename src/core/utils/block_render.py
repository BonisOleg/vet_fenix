from __future__ import annotations

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.block_defaults import BLOCK_DEFAULTS


def get_block_text(page: str, key: str, site_blocks: dict | None = None, fallback: str = '') -> str:
    blocks = site_blocks or {}
    block = blocks.get(f'{page}.{key}')
    if block is not None and block.is_active:
        value = (block.text_html or '').strip()
        if value or value == '0':
            return value
    default = fallback or BLOCK_DEFAULTS.get((page, key), '')
    return default.strip()


def is_section_visible(page: str, visibility_key: str, site_blocks: dict | None = None) -> bool:
    blocks = site_blocks or {}
    block = blocks.get(f'{page}.{visibility_key}')

    if block is not None:
        value = (block.text_html or '').strip()
    else:
        value = str(BLOCK_DEFAULTS.get((page, visibility_key), '1')).strip()

    if value == '':
        return True

    return value.lower() not in {'0', 'false'}


def render_block_html(block) -> str:
    if block is None or not block.is_active:
        return ''

    if block.content_type == block.ContentType.TEXT:
        return mark_safe(block.text_html)

    if block.content_type == block.ContentType.IMAGE and block.image:
        return format_html(
            '<img class="site-block-image" src="{}" alt="{}" loading="lazy" decoding="async">',
            block.image.url,
            block.label or '',
        )

    return ''
