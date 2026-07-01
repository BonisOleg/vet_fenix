from django.test import TestCase

from core.models import SiteBlock
from core.site_nav import (
    PRIMARY_NAV_ITEMS,
    get_visible_nav_items,
    is_nav_item_visible,
)


class SiteNavVisibilityTests(TestCase):
    def test_primary_nav_shows_all_by_default(self):
        items = get_visible_nav_items({})
        self.assertEqual(len(items), len(PRIMARY_NAV_ITEMS))

    def test_services_nav_hidden_when_home_preview_off(self):
        SiteBlock.objects.update_or_create(
            page='services',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '1', 'is_active': True},
        )
        SiteBlock.objects.update_or_create(
            page='home',
            key='services_preview_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('services', blocks))

    def test_services_nav_shown_when_both_sections_on(self):
        SiteBlock.objects.update_or_create(
            page='services',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '1', 'is_active': True},
        )
        SiteBlock.objects.update_or_create(
            page='home',
            key='services_preview_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '1', 'is_active': True},
        )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertTrue(is_nav_item_visible('services', blocks))

    def test_services_nav_hidden_when_page_off(self):
        SiteBlock.objects.update_or_create(
            page='services',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('services', blocks))

    def test_doctors_nav_hidden_when_home_preview_off(self):
        SiteBlock.objects.update_or_create(
            page='doctors',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '1', 'is_active': True},
        )
        SiteBlock.objects.update_or_create(
            page='home',
            key='doctors_preview_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('doctors', blocks))

    def test_doctors_nav_hidden_when_page_off(self):
        SiteBlock.objects.update_or_create(
            page='doctors',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('doctors', blocks))

    def test_services_nav_hidden_when_both_gates_off(self):
        for page, key in (
            ('services', 'header_section_visible'),
            ('home', 'services_preview_section_visible'),
        ):
            SiteBlock.objects.update_or_create(
                page=page,
                key=key,
                defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
            )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('services', blocks))

    def test_doctors_nav_hidden_when_both_gates_off(self):
        for page, key in (
            ('doctors', 'header_section_visible'),
            ('home', 'doctors_preview_section_visible'),
        ):
            SiteBlock.objects.update_or_create(
                page=page,
                key=key,
                defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
            )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('doctors', blocks))

    def test_bottom_nav_keeps_booking_when_home_hidden(self):
        for page, key in (
            ('home', 'hero_section_visible'),
            ('home', 'advantages_section_visible'),
            ('home', 'services_preview_section_visible'),
            ('home', 'doctors_preview_section_visible'),
        ):
            SiteBlock.objects.update_or_create(
                page=page,
                key=key,
                defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
            )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        nav_ids = [item.nav_id for item in get_visible_nav_items(blocks, bottom=True)]
        self.assertNotIn('home', nav_ids)
        self.assertIn('booking', nav_ids)

    def test_home_nav_hidden_when_all_home_sections_hidden(self):
        for key in (
            'hero_section_visible',
            'advantages_section_visible',
            'services_preview_section_visible',
            'doctors_preview_section_visible',
        ):
            SiteBlock.objects.update_or_create(
                page='home',
                key=key,
                defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
            )
        blocks = {block.cache_key: block for block in SiteBlock.objects.all()}
        self.assertFalse(is_nav_item_visible('home', blocks))

    def test_header_hides_doctors_link_when_page_hidden(self):
        from django.test import Client

        SiteBlock.objects.update_or_create(
            page='doctors',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )
        SiteBlock.objects.update_or_create(
            page='home',
            key='doctors_preview_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )

        response = Client(HTTP_HOST='127.0.0.1').get('/')
        html = response.content.decode()
        nav_start = html.find('site-nav-desktop')
        nav_end = html.find('</nav>', nav_start)
        nav_html = html[nav_start:nav_end]
        self.assertNotIn('/likari/', nav_html)

    def test_doctors_page_empty_when_section_hidden(self):
        from django.test import Client

        SiteBlock.objects.update_or_create(
            page='doctors',
            key='header_section_visible',
            defaults={'label': 'Visible', 'content_type': 'text', 'text_html': '0', 'is_active': True},
        )

        response = Client(HTTP_HOST='127.0.0.1').get('/likari/')
        self.assertNotContains(response, 'docs-grid')
