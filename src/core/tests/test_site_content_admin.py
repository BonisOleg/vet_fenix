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
        self.assertContains(response, 'bg-white')
        self.assertContains(response, 'text-font-default-light')
        self.assertContains(response, 'dark:bg-base-900')
        self.assertContains(response, 'site-content-fieldset__summary')
        self.assertContains(response, '<details')

    def test_cms_text_inputs_use_light_theme_classes(self):
        import re

        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.get(url)
        html = response.content.decode()
        matches = re.findall(
            r'name="block__home__hero_title__text_html"[^>]*class="([^"]+)"',
            html,
        )
        self.assertTrue(matches)
        classes = matches[0]
        self.assertIn('bg-white', classes)
        self.assertIn('dark:bg-base-900', classes)
        # Forced always-dark bg without dark: prefix must not appear alone as theme lock
        tokens = classes.split()
        self.assertIn('bg-white', tokens)
        self.assertNotIn('text-base-100', tokens)

    def test_site_settings_form_uses_readable_inputs(self):
        url = reverse('admin:core_sitesettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bg-white')
        self.assertContains(response, 'text-font-default-light')
        self.assertContains(response, 'dark:bg-base-900')

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

    def test_clinic_info_section_renders_contact_settings(self):
        url = reverse('admin:core_contactsclinicinfosettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'setting__reassessment_hours_label')
        self.assertContains(response, 'Години переоцінки')

    def test_clinic_info_section_saves_contact_settings(self):
        section = get_section('contacts', 'clinic-info')
        blocks = load_section_blocks(section)
        payload = {'section_visible': 'on'}
        for page, key in section.blocks:
            block = blocks[(page, key)]
            payload[f'block__{page}__{key}__text_html'] = block.text_html

        payload.update(
            {
                'setting__address': 'м. Київ, тест',
                'setting__phone_primary': '+380933839933',
                'setting__phone_secondary': '',
                'setting__email': '',
                'setting__hours_label': 'Цілодобово',
                'setting__reassessment_hours_label': '10:00–11:00 — тест',
            }
        )

        url = reverse('admin:core_contactsclinicinfosettings_change', args=[1])
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)

        site = SiteSettings.load()
        self.assertEqual(site.reassessment_hours_label, '10:00–11:00 — тест')
        self.assertEqual(site.address, 'м. Київ, тест')

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
