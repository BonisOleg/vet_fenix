from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.admin_site_content import block_field_name, load_section_blocks
from core.context_processors import invalidate_site_blocks_cache
from core.models import SiteBlock, SiteSettings
from core.site_content_registry import CONTENT_SECTIONS, get_section, iter_section_blocks


def _visibility_page_key(section) -> tuple[str, str]:
    for page, key in iter_section_blocks(section):
        if key == section.visibility_key:
            return page, key
    raise KeyError(section.visibility_key)


def _admin_payload(section, *, visible: bool) -> dict[str, str]:
    blocks = load_section_blocks(section)
    payload: dict[str, str] = {}
    if section.visibility_key:
        if visible:
            payload['section_visible'] = 'on'
    for page, key in section.blocks:
        block = blocks[(page, key)]
        if block.content_type == 'text':
            payload[block_field_name(page, key, 'text_html')] = block.text_html or ''
    return payload


class CmsAdminE2ETests(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username='admin',
            email='admin@test.local',
            password='testpass123',
        )
        self.client = Client(HTTP_HOST='127.0.0.1')
        self.client.force_login(self.admin_user)
        SiteSettings.objects.get_or_create(pk=1)

    def test_all_cms_sections_render_admin_form(self) -> None:
        for section in CONTENT_SECTIONS:
            with self.subTest(section=section.admin_model_name):
                url = reverse(f'admin:core_{section.admin_model_name}_change', args=[1])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200, section.admin_model_name)
                html = response.content.decode()
                self.assertIn('Показувати секцію на сайті', html)
                self.assertIn('site-content-visibility__input', html)
                self.assertIn('type="submit"', html)

    def test_all_cms_sections_save_visibility_off(self) -> None:
        for section in CONTENT_SECTIONS:
            with self.subTest(section=section.admin_model_name):
                section_obj = get_section(section.page_slug, section.slug)
                url = reverse(f'admin:core_{section.admin_model_name}_change', args=[1])
                payload = _admin_payload(section_obj, visible=False)
                response = self.client.post(url, payload)
                self.assertEqual(response.status_code, 302, section.admin_model_name)

                page, key = _visibility_page_key(section_obj)
                block = SiteBlock.objects.get(page=page, key=key)
                self.assertEqual(block.text_html, '0', section.admin_model_name)

    def test_hero_visibility_controls_site_and_nav(self) -> None:
        section = get_section('home', 'hero')
        url = reverse('admin:core_homeherosettings_change', args=[1])

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        home = self.client.get('/')
        self.assertNotContains(home, 'class="hero"')

        self.client.post(url, _admin_payload(section, visible=True))
        invalidate_site_blocks_cache()
        home_visible = self.client.get('/')
        self.assertContains(home_visible, 'class="hero"')

    def test_services_preview_hides_home_block_and_nav(self) -> None:
        section = get_section('home', 'services-preview')
        url = reverse('admin:core_homeservicespreviewsettings_change', args=[1])

        SiteBlock.objects.update_or_create(
            page='services',
            key='header_section_visible',
            defaults={'label': 'v', 'content_type': 'text', 'text_html': '1', 'is_active': True},
        )

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        home = self.client.get('/')
        self.assertNotContains(home, 'id="poslugy"')

        html = home.content.decode()
        nav_start = html.find('site-nav-desktop')
        nav_end = html.find('</nav>', nav_start)
        self.assertNotIn('/poslugy/', html[nav_start:nav_end])
        self.assertNotIn('>Послуги<', html[nav_start:nav_end])

    def test_services_preview_visibility_controls_home_block_when_page_off(self) -> None:
        section = get_section('home', 'services-preview')
        url = reverse('admin:core_homeservicespreviewsettings_change', args=[1])

        SiteBlock.objects.update_or_create(
            page='services',
            key='header_section_visible',
            defaults={'label': 'v', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        home = self.client.get('/')
        self.assertNotContains(home, 'id="poslugy"')

        html = home.content.decode()
        nav_start = html.find('site-nav-desktop')
        nav_end = html.find('</nav>', nav_start)
        self.assertNotIn('/poslugy/', html[nav_start:nav_end])

    def test_doctors_page_visibility_controls_page_and_nav(self) -> None:
        section = get_section('doctors', 'header')
        url = reverse('admin:core_doctorspageheadersettings_change', args=[1])

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        page = self.client.get('/likari/')
        self.assertNotContains(page, 'docs-grid')

        home = self.client.get('/')
        html = home.content.decode()
        nav_start = html.find('site-nav-desktop')
        nav_end = html.find('</nav>', nav_start)
        self.assertNotIn('/likari/', html[nav_start:nav_end])

    def test_map_visibility_controls_contacts_map(self) -> None:
        section = get_section('contacts', 'map')
        url = reverse('admin:core_contactsmapsettings_change', args=[1])

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        contacts = self.client.get('/kontakty/')
        self.assertNotContains(contacts, 'map-embed')

    def test_trust_strip_visibility(self) -> None:
        section = get_section('site', 'trust-strip')
        url = reverse('admin:core_truststripsettings_change', args=[1])

        self.client.post(url, _admin_payload(section, visible=False))
        invalidate_site_blocks_cache()

        home = self.client.get('/')
        self.assertNotContains(home, 'trust-strip')
