from django.db import models


class SiteSettings(models.Model):
    clinic_name_line1 = models.CharField('Назва (рядок 1)', max_length=64, default='ветеринарна клініка')
    clinic_name_line2 = models.CharField('Назва (рядок 2)', max_length=64, default='Фенікс')
    logo = models.ImageField('Логотип', upload_to='brand/', blank=True)
    tagline = models.CharField('Слоган', max_length=200, blank=True)
    address = models.CharField('Адреса', max_length=255, default='м. Київ, вул. Ірпінська, 67б')
    phone_primary = models.CharField('Телефон', max_length=32, default='+380933839933')
    phone_secondary = models.CharField('Телефон 2', max_length=32, blank=True, default='+380983839033')
    email = models.EmailField('Електронна пошта', blank=True, default='')
    is_open_now = models.BooleanField('Працюємо зараз', default=True)
    trust_label = models.CharField('Смуга довіри', max_length=64, default='Працюємо зараз')
    hours_label = models.CharField('Години роботи', max_length=64, default='Цілодобово')
    reassessment_hours_label = models.TextField(
        'Години переоцінки',
        blank=True,
        default='9:30–10:30 та 20:00–21:00 — прийом лише екстрених пацієнтів',
    )

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self) -> str:
        return f'{self.clinic_name_line1} {self.clinic_name_line2}'

    def save(self, *args, **kwargs) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        pass

    @classmethod
    def load(cls) -> 'SiteSettings':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteBlock(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'

    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        SERVICES = 'services', 'Послуги'
        DOCTORS = 'doctors', 'Лікарі'
        CONTACTS = 'contacts', 'Контакти'
        SITE = 'site', 'Сайт'

    page = models.CharField(max_length=32, choices=Page.choices, verbose_name='Сторінка')
    key = models.CharField(max_length=64, verbose_name='Ключ блоку')
    label = models.CharField(max_length=128, verbose_name='Назва в адмінці')
    content_type = models.CharField(
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
        verbose_name='Тип контенту',
    )
    text_html = models.TextField(blank=True, verbose_name='Текст')
    image = models.ImageField(upload_to='blocks/', blank=True, verbose_name='Зображення')
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    class Meta:
        ordering = ['page', 'sort_order', 'key']
        verbose_name = 'Блок контенту'
        verbose_name_plural = 'Блоки контенту'
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='unique_site_block_page_key'),
        ]

    def __str__(self) -> str:
        return f'{self.get_page_display()} · {self.label}'

    @property
    def cache_key(self) -> str:
        return f'{self.page}.{self.key}'


class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Банер'
        verbose_name_plural = 'Головна — Банер'


class HomeAdvantagesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Переваги'
        verbose_name_plural = 'Головна — Переваги'


class HomeServicesPreviewSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Послуги'
        verbose_name_plural = 'Головна — Послуги'


class HomeDoctorsPreviewSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Лікарі'
        verbose_name_plural = 'Головна — Лікарі'


class ServicesPageHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — Заголовок'
        verbose_name_plural = 'Послуги — Заголовок'


class DoctorsPageHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Лікарі — Заголовок'
        verbose_name_plural = 'Лікарі — Заголовок'


class ContactsPageHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти — Заголовок'
        verbose_name_plural = 'Контакти — Заголовок'


class ContactsClinicInfoSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти — Клініка'
        verbose_name_plural = 'Контакти — Клініка'


class ContactsFormSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти — Форма'
        verbose_name_plural = 'Контакти — Форма'


class ContactsMapSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти — Карта'
        verbose_name_plural = 'Контакти — Карта'


class TrustStripSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Смуга довіри'
        verbose_name_plural = 'Смуга довіри'


class FooterSocialSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Футер — Соцмережі'
        verbose_name_plural = 'Футер — Соцмережі'
