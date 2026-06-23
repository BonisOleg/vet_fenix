from django.test import SimpleTestCase

from core.templatetags.vet_icons import address_short


class AddressShortFilterTests(SimpleTestCase):
    def test_strips_m_prefix(self):
        self.assertEqual(
            address_short('м. Київ, вул. Велика Васильківська, 100'),
            'Київ, вул. Велика Васильківська, 100',
        )

    def test_passthrough_without_prefix(self):
        self.assertEqual(address_short('Київ, вул. Test'), 'Київ, вул. Test')
