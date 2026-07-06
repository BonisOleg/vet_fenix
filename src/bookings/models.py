from django.conf import settings
from django.db import models

from clinic.models import Doctor, Service


class AppointmentStatus(models.TextChoices):
    NEW = 'new', 'Нова'
    CONFIRMED = 'confirmed', 'Підтверджена'
    DONE = 'done', 'Завершена'
    CANCELLED = 'cancelled', 'Скасована'


class AppointmentRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments', verbose_name='Послуга')
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name='Лікар',
    )
    owner_name = models.CharField('Імʼя власника', max_length=120)
    phone = models.CharField('Телефон', max_length=32)
    pet_name = models.CharField('Кличка тварини', max_length=80, blank=True)
    pet_type = models.CharField('Вид тварини', max_length=32, choices=settings.PET_TYPE_CHOICES)
    preferred_date = models.DateField('Бажана дата')
    preferred_time = models.CharField('Бажаний час', max_length=8)
    comment = models.TextField('Коментар', blank=True)
    status = models.CharField(
        'Статус',
        max_length=16,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.NEW,
    )
    source_page = models.CharField('Джерело', max_length=32, default='booking')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на запис'
        verbose_name_plural = 'Заявки на запис'

    def __str__(self) -> str:
        return f'{self.owner_name} — {self.service.name} ({self.preferred_date})'


class CallbackLead(models.Model):
    name = models.CharField('Імʼя', max_length=120)
    phone = models.CharField('Телефон', max_length=32)
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='callback_leads',
        verbose_name='Послуга',
    )
    comment = models.TextField('Коментар', blank=True)
    source_page = models.CharField('Джерело', max_length=64, default='popup')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запит на передзвінок'
        verbose_name_plural = 'Запити на передзвінок'

    def __str__(self) -> str:
        service_name = self.service.name if self.service else '—'
        return f'{self.name} — {service_name}'
