from django.test import TestCase

from core.models import SiteBlock
from core.utils.block_render import get_block_text, is_section_visible


class BlockRenderTests(TestCase):
    def test_fallback_to_defaults_when_block_missing(self):
        text = get_block_text('home', 'hero_title', site_blocks={})
        self.assertIn('Турбота', text)

    def test_section_visible_defaults_to_true(self):
        self.assertTrue(is_section_visible('home', 'hero_section_visible', site_blocks={}))

    def test_section_visible_false_when_zero(self):
        block, _ = SiteBlock.objects.update_or_create(
            page='home',
            key='hero_section_visible',
            defaults={
                'label': 'Visible',
                'content_type': 'text',
                'text_html': '0',
                'is_active': False,
            },
        )
        blocks = {block.cache_key: block}
        self.assertFalse(is_section_visible('home', 'hero_section_visible', site_blocks=blocks))

    def test_get_block_text_from_database(self):
        SiteBlock.objects.update_or_create(
            page='home',
            key='hero_title',
            defaults={
                'label': 'Title',
                'content_type': 'text',
                'text_html': 'Custom hero',
                'is_active': True,
            },
        )
        blocks = {b.cache_key: b for b in SiteBlock.objects.filter(is_active=True)}
        self.assertEqual(get_block_text('home', 'hero_title', site_blocks=blocks), 'Custom hero')
