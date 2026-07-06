from django.test import SimpleTestCase

from core.site_content_registry import (
    CONTENT_SECTIONS,
    PAGE_SIDEBAR_GROUPS,
    all_registry_block_keys,
    build_content_sidebar_items,
    build_content_sidebar_navigation,
)


class SiteContentRegistryTests(SimpleTestCase):
    def test_block_keys_are_unique_per_page(self):
        seen: set[tuple[str, str]] = set()
        duplicates: list[tuple[str, str]] = []
        for page, key in all_registry_block_keys():
            pair = (page, key)
            if pair in seen:
                duplicates.append(pair)
            seen.add(pair)
        self.assertEqual(duplicates, [])

    def test_each_section_has_admin_model(self):
        for section in CONTENT_SECTIONS:
            self.assertTrue(section.admin_model_name)
            self.assertTrue(section.visibility_key)

    def test_section_count(self):
        self.assertEqual(len(CONTENT_SECTIONS), 12)

    def test_sidebar_items_count_matches_sections(self):
        self.assertEqual(len(build_content_sidebar_items()), len(CONTENT_SECTIONS))

    def test_sidebar_navigation_groups(self):
        navigation = build_content_sidebar_navigation()
        self.assertEqual(len(navigation), len(PAGE_SIDEBAR_GROUPS))
        for group in navigation:
            self.assertTrue(group['collapsible'])
            self.assertTrue(group['items'])
        total_items = sum(len(group['items']) for group in navigation)
        self.assertEqual(total_items, len(CONTENT_SECTIONS))
        self.assertTrue(navigation[0]['separator'])
        self.assertFalse(any(group['separator'] for group in navigation[1:]))
