from django.test import SimpleTestCase

from core.site_content_registry import CONTENT_SECTIONS, all_registry_block_keys


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
