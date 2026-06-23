from datetime import date

from django.test import TestCase
from django.urls import reverse

from bookings.models import AppointmentRequest
from clinic.models import Service


class BookingViewTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.service = Service.objects.get(slug='therapy')
        self.url = reverse('bookings:booking_submit')
        self.valid = {
            'service': self.service.pk,
            'doctor': '',
            'owner_name': 'Тест Клієнт',
            'phone': '+380501234567',
            'pet_name': 'Барсик',
            'pet_type': 'cat',
            'preferred_date': date.today().isoformat(),
            'preferred_time': '10:00',
            'comment': '',
        }

    def test_booking_page_200(self):
        response = self.client.get(reverse('bookings:booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запис на прийом')

    def test_valid_post_creates_appointment(self):
        response = self.client.post(self.url, self.valid)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заявку прийнято')
        self.assertEqual(AppointmentRequest.objects.count(), 1)

    def test_invalid_post_returns_errors(self):
        data = {**self.valid, 'phone': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(AppointmentRequest.objects.count(), 0)
        self.assertIn(b'field-error', response.content)

    def test_empty_required_fields_show_validation(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(AppointmentRequest.objects.count(), 0)
        self.assertContains(response, 'Заповніть це поле', status_code=422)
        self.assertContains(response, 'field-error', status_code=422)
