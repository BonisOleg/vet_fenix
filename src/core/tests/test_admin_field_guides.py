from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import SiteSettings


class AdminFieldGuidesTests(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username='admin',
            email='admin@test.local',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        SiteSettings.objects.get_or_create(pk=1)

    def test_doctor_change_form_shows_photo_guide(self):
        url = reverse('admin:clinic_doctor_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квадратне фото')
        self.assertContains(response, 'можуть зламати верстку')

    def test_advantage_change_form_shows_icon_choices(self):
        url = reverse('admin:clinic_advantage_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Лапа')
        self.assertContains(response, 'Нагорода')

    def test_admin_layout_warning_visible(self):
        url = reverse('admin:clinic_doctor_add')
        response = self.client.get(url)
        self.assertContains(response, 'admin-layout-warning')
        self.assertContains(response, 'автоматично конвертуються в WebP')
