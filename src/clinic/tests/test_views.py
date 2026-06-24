from django.test import TestCase
from django.urls import reverse

from clinic.models import ContactMessage, Service


class HomeViewTests(TestCase):
    fixtures = ['initial_data.json']

    def test_home_returns_200(self):
        response = self.client.get(reverse('clinic:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Послуги')
        self.assertContains(response, 'Лікарі')
        self.assertNotContains(response, '>Переваги</a>')
        self.assertContains(response, 'Чому обирають Фенікс')
        self.assertContains(response, 'Записатись')
        self.assertContains(response, 'trust-strip')
        self.assertContains(response, 'Ветеринарна клініка «Фенікс»')
        self.assertNotContains(response, 'hero__meta')
        self.assertNotContains(response, 'Викликати')
        self.assertContains(response, 'Наші послуги')
        self.assertNotContains(response, 'Швидка')
        self.assertNotContains(response, 'Цілодобовий виклик')
        self.assertContains(response, 'Інтенсивна терапія')
        self.assertContains(response, 'id="likari"')
        self.assertContains(response, 'mobile-menu')
        self.assertContains(response, 'class="icon')
        self.assertContains(response, 'data-reveal')
        self.assertContains(response, 'міжнародними протоколами')
        self.assertNotContains(response, 'Стаж від')
        self.assertNotContains(response, 'р. досвіду')
        self.assertNotContains(response, '2400+ пацієнтів')
        self.assertNotContains(response, '[фото лікаря]')
        self.assertContains(response, 'motion.js')
        self.assertNotContains(response, 'contact-block')
        self.assertNotContains(response, 'contact-block__arc')
        self.assertContains(response, 'Ірпінська')
        self.assertContains(response, 'Детальніше')
        self.assertNotContains(response, 'Спокійно і професійно')
        self.assertNotContains(response, 'class="pulse"')
        self.assertNotContains(response, 'hero-status')
        self.assertNotContains(response, 'hero-stats')

    def test_home_nav_links_to_pages(self):
        response = self.client.get(reverse('clinic:home'))
        self.assertContains(response, reverse('clinic:services'))
        self.assertContains(response, reverse('clinic:doctors'))
        self.assertContains(response, reverse('clinic:contacts'))
        self.assertNotContains(response, '#poslugy">Послуги')

    def test_service_detail_partial(self):
        response = self.client.get(reverse('clinic:service_detail', kwargs={'slug': 'therapy'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Первинний огляд')


class ServicesPageTests(TestCase):
    fixtures = ['initial_data.json']

    def test_services_page_returns_200(self):
        response = self.client.get(reverse('clinic:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'svc-grid--page')
        self.assertContains(response, 'Первинний огляд')
        self.assertContains(response, 'Терапія')
        self.assertNotContains(response, 'Швидка')
        self.assertNotContains(response, 'Цілодобовий виклик')
        self.assertContains(response, 'Інтенсивна терапія')
        self.assertContains(response, reverse('clinic:services'))
        self.assertNotContains(response, 'data-service-toggle')


class DoctorsPageTests(TestCase):
    fixtures = ['initial_data.json']

    def test_doctors_page_returns_200(self):
        response = self.client.get(reverse('clinic:doctors'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'docs-grid--page')
        self.assertContains(response, 'doc-card--page')
        self.assertContains(response, 'Вероніка Володимирівна')
        self.assertContains(response, 'міжнародними протоколами')
        self.assertNotContains(response, 'Стаж від')
        self.assertNotContains(response, 'р. досвіду')
        self.assertNotContains(response, '2400+ пацієнтів')
        self.assertContains(response, reverse('clinic:doctors'))


class ContactsPageTests(TestCase):
    fixtures = ['initial_data.json']

    def test_contacts_page_returns_200(self):
        response = self.client.get(reverse('clinic:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ірпінська')
        self.assertContains(response, '<iframe')
        self.assertContains(response, 'maps.google.com')
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, reverse('clinic:contacts'))

    def test_contacts_form_post_success(self):
        response = self.client.post(
            reverse('clinic:contacts'),
            {
                'name': 'Тест',
                'phone': '+380501234567',
                'message': 'Питання',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Дякуємо')
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, 'Тест')
        self.assertEqual(message.phone, '+380501234567')
        self.assertEqual(message.message, 'Питання')

    def test_contacts_form_post_invalid(self):
        response = self.client.post(
            reverse('clinic:contacts'),
            {'name': 'Тест', 'phone': 'bad', 'message': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'коректний номер')
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contacts_form_post_empty_fields(self):
        response = self.client.post(
            reverse('clinic:contacts'),
            {'name': '', 'phone': '', 'message': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'field-error')
        self.assertContains(response, 'Заповніть це поле')
        self.assertEqual(ContactMessage.objects.count(), 0)


class FooterTests(TestCase):
    fixtures = ['initial_data.json']

    def test_home_contains_footer(self):
        response = self.client.get(reverse('clinic:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'site-footer')
        self.assertContains(response, 'PrometeyLabs')
        self.assertContains(response, 'https://www.prometeylabs.com/')
        self.assertContains(response, reverse('clinic:privacy_policy'))
        self.assertContains(response, reverse('clinic:public_offer'))
        self.assertContains(response, 'Політика конфіденційності')
        self.assertContains(response, 'Договір публічної оферти')
        self.assertContains(response, 'aria-label="Instagram"')
        self.assertContains(response, 'aria-label="Telegram"')


class LegalPageTests(TestCase):
    fixtures = ['initial_data.json']

    def test_privacy_policy_page(self):
        response = self.client.get(reverse('clinic:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="page-heading" data-reveal>Політика конфіденційності</h1>')

    def test_public_offer_page(self):
        response = self.client.get(reverse('clinic:public_offer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="page-heading" data-reveal>Договір публічної оферти</h1>')


class ServiceModelTests(TestCase):
    fixtures = ['initial_data.json']

    def test_services_loaded(self):
        self.assertEqual(Service.objects.filter(is_active=True).count(), 11)
