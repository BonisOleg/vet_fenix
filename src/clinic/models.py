from django.db import models


class ServiceIcon(models.TextChoices):
    STEHOSCOPE = 'stethoscope', 'Стетоскоп'
    SYRINGE = 'syringe', 'Шприц'
    SCISSORS = 'scissors', 'Ножиці'
    SCAN = 'scan', 'Діагностика'
    TOOTH = 'tooth', 'Зуб'
    VIDEO = 'video', 'Онлайн'


class AdvantageIcon(models.TextChoices):
    CLOCK = 'clock', 'Годинник'
    SHIELD = 'shield', 'Щит'
    STAR = 'star', 'Зірка'
    HEART = 'heart', 'Серце'


class Service(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    short_description = models.CharField(max_length=120)
    full_description = models.TextField()
    price_hint = models.CharField(max_length=64, blank=True)
    icon = models.CharField(max_length=32, choices=ServiceIcon.choices, default=ServiceIcon.STEHOSCOPE)
    bullets = models.JSONField(default=list, blank=True)
    is_urgent = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'

    def __str__(self) -> str:
        return self.name


class Doctor(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=160)
    experience_years = models.PositiveSmallIntegerField()
    initials = models.CharField(max_length=8, blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True)
    rating = models.DecimalField('Рейтинг', max_digits=2, decimal_places=1, default=4.9)
    patients_label = models.CharField(
        'Пацієнти',
        max_length=32,
        default='1000+ пацієнтів',
        help_text='Наприклад: 2400+ пацієнтів',
    )
    bio = models.TextField('Коротка біографія', blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Лікар'
        verbose_name_plural = 'Лікарі'

    def __str__(self) -> str:
        return self.name

    def display_initials(self) -> str:
        if self.initials:
            return self.initials
        parts = self.name.split()
        return ''.join(p[0].upper() for p in parts[:2])


class ContactMessage(models.Model):
    name = models.CharField('Імʼя', max_length=120)
    phone = models.CharField('Телефон', max_length=32)
    message = models.TextField('Повідомлення')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Звернення з контактів'
        verbose_name_plural = 'Звернення з контактів'

    def __str__(self) -> str:
        return f'{self.name} — {self.phone}'


class Advantage(models.Model):
    icon = models.CharField(max_length=32, choices=AdvantageIcon.choices, default=AdvantageIcon.CLOCK)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)
    order = models.PositiveSmallIntegerField(default=0)
    is_alt = models.BooleanField(default=False, help_text='Помаранчева іконка')
    is_active = models.BooleanField('Показувати на сайті', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self) -> str:
        return self.title
