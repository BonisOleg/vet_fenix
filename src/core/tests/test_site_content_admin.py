from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.admin_site_content import load_section_blocks
from core.models import SiteBlock, SiteSettings
from core.site_content_registry import get_section


class SiteContentAdminTests(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username='admin',
            email='admin@test.local',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        SiteSettings.objects.get_or_create(pk=1)

    def test_hero_section_form_renders_visibility_checkbox(self):
        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Показувати секцію на сайті')
        self.assertContains(response, 'hero_title')
        self.assertContains(response, 'bg-base-900')
        self.assertContains(response, 'text-base-100')

    def test_cms_text_inputs_have_no_white_background(self):
        import re

        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.get(url)
        html = response.content.decode()
        matches = re.findall(
            r'name="block__home__hero_title__text_html"[^>]*class="([^"]+)"',
            html,
        )
        self.assertTrue(matches)
        self.assertIn('bg-base-900', matches[0])
        self.assertNotIn('bg-white', matches[0])

    def test_site_settings_form_uses_readable_inputs(self):
        url = reverse('admin:core_sitesettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bg-base-900')
        self.assertContains(response, 'text-base-100')

    def test_hero_section_save_updates_blocks(self):
        section = get_section('home', 'hero')
        blocks = load_section_blocks(section)
        payload = {'section_visible': 'on'}
        for page, key in section.blocks:
            block = blocks[(page, key)]
            if block.content_type == 'text':
                if key == 'hero_title':
                    payload[f'block__{page}__{key}__text_html'] = 'Новий заголовок hero'
                else:
                    payload[f'block__{page}__{key}__text_html'] = block.text_html

        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        block = SiteBlock.objects.get(page='home', key='hero_title')
        self.assertEqual(block.text_html, 'Новий заголовок hero')

    def test_map_section_visibility_only(self):
        url = reverse('admin:core_contactsmapsettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Показувати секцію на сайті')

    def test_visibility_toggle_hides_hero_on_site(self):
        from django.core.cache import cache
        from core.context_processors import SITE_BLOCKS_CACHE_KEY

        section = get_section('home', 'hero')
        blocks = load_section_blocks(section)
        payload = {}
        for page, key in section.blocks:
            block = blocks[(page, key)]
            if block.content_type == 'text':
                payload[f'block__{page}__{key}__text_html'] = block.text_html

        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)

        visibility = SiteBlock.objects.get(page='home', key='hero_section_visible')
        self.assertEqual(visibility.text_html, '0')
        cache.delete(SITE_BLOCKS_CACHE_KEY)

        home = self.client.get('/')
        self.assertNotContains(home, 'class="hero"')

        payload['section_visible'] = 'on'
        self.client.post(url, payload)
        cache.delete(SITE_BLOCKS_CACHE_KEY)
        home_visible = self.client.get('/')
        self.assertContains(home_visible, 'class="hero"')
