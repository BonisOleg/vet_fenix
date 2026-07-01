from django import template
from django.templatetags.static import static
from django.utils.html import format_html

from core.block_defaults import BLOCK_DEFAULTS
from core.utils.block_render import get_block_text, is_section_visible, render_block_html

register = template.Library()


@register.simple_tag(takes_context=True)
def render_block(context, page: str, key: str, fallback: str = '') -> str:
    blocks = context.get('site_blocks', {})
    block = blocks.get(f'{page}.{key}')
    rendered = render_block_html(block)
    if rendered:
        return rendered
    return get_block_text(page, key, site_blocks=blocks, fallback=fallback)


@register.simple_tag(takes_context=True)
def block_plain(context, page: str, key: str, fallback: str = '') -> str:
    blocks = context.get('site_blocks', {})
    return get_block_text(page, key, site_blocks=blocks, fallback=fallback)


@register.simple_tag(takes_context=True)
def section_visible(context, page: str, visibility_key: str) -> bool:
    blocks = context.get('site_blocks', {})
    return is_section_visible(page, visibility_key, site_blocks=blocks)


@register.simple_tag(takes_context=True)
def block_image(context, page: str, key: str, css_class: str = '', fallback_static: str = '') -> str:
    blocks = context.get('site_blocks', {})
    block = blocks.get(f'{page}.{key}')
    alt_key = 'hero_image_alt' if key == 'hero_image' else f'{key}_alt'
    alt = get_block_text(page, alt_key, site_blocks=blocks)

    if block is not None and block.is_active and block.image:
        if css_class:
            return format_html(
                '<img class="{}" src="{}" alt="{}" loading="eager" decoding="async">',
                css_class,
                block.image.url,
                alt,
            )
        return format_html(
            '<img src="{}" alt="{}" loading="eager" decoding="async">',
            block.image.url,
            alt,
        )

    if fallback_static:
        src = static(fallback_static)
        if css_class:
            return format_html(
                '<img class="{}" src="{}" alt="{}" loading="eager" decoding="async">',
                css_class,
                src,
                alt or BLOCK_DEFAULTS.get((page, alt_key), ''),
            )
        return format_html(
            '<img src="{}" alt="{}" loading="eager" decoding="async">',
            src,
            alt or BLOCK_DEFAULTS.get((page, alt_key), ''),
        )
    return ''
