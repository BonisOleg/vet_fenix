from django.test import TestCase
from django.urls import reverse

from bookings.models import CallbackLead
from clinic.models import Service


class CallbackSubmitTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.service = Service.objects.get(slug='therapy')
        self.url = reverse('bookings:callback_submit')
        self.valid = {
            'name': 'Тест Клієнт',
            'phone': '+380501234567',
            'service': self.service.pk,
            'comment': 'Потрібна консультація',
        }

    def test_callback_submit_valid(self):
        response = self.client.post(self.url, self.valid, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Дякуємо')
        self.assertEqual(CallbackLead.objects.count(), 1)
        lead = CallbackLead.objects.get()
        self.assertEqual(lead.name, 'Тест Клієнт')
        self.assertEqual(lead.service, self.service)
        self.assertEqual(lead.source_page, self.url)

    def test_callback_submit_invalid_phone(self):
        data = {**self.valid, 'phone': '123'}
        response = self.client.post(self.url, data, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(CallbackLead.objects.count(), 0)
        self.assertIn(b'field-error', response.content)

    def test_callback_modal_not_on_booking_page(self):
        response = self.client.get(reverse('bookings:booking'))
        self.assertNotContains(response, 'id="callback-modal"')

    def test_callback_modal_on_home_page(self):
        response = self.client.get(reverse('clinic:home'))
        self.assertContains(response, 'id="callback-modal"')
