from django.db import models


HERO_LEAD_DEFAULT = (
    'Ветеринарна клініка «Фенікс» надає широкий спектр послуг для Ваших домашніх улюбленців. '
    'Наші фахівці працюють за актуальними протоколами, спираючись на доказову медицину. '
    'Клініка забезпечена новітнім обладнанням, що допомагає у швидкій діагностиці пацієнтів. '
    'З основних переваг — цілодобовий стаціонар інтенсивної терапії та реанімації. '
    'Постійне навчання, поглиблення знань та навичок персоналу, використання сучасних методів '
    'діагностики — шлях до успіху у лікуванні Ваших хвостиків.'
)


class SiteSettings(models.Model):
    clinic_name_line1 = models.CharField('Назва (рядок 1)', max_length=64, default='ветеринарна клініка')
    clinic_name_line2 = models.CharField('Назва (рядок 2)', max_length=64, default='Фенікс')
    tagline = models.CharField('Слоган', max_length=200, blank=True)
    address = models.CharField('Адреса', max_length=255, default='м. Київ, вул. Ірпінська, 67б')
    phone_primary = models.CharField('Телефон', max_length=32, default='+380933839933')
    phone_secondary = models.CharField('Телефон 2', max_length=32, blank=True, default='+380983839033')
    email = models.EmailField('Email', blank=True, default='')
    hero_title = models.CharField(
        'Заголовок hero',
        max_length=255,
        default='Турбота про ваших улюбленців — цілодобово',
    )
    hero_lead = models.TextField(
        'Підзаголовок hero',
        max_length=600,
        default=HERO_LEAD_DEFAULT,
    )
    hero_stat_number = models.CharField('Hero картка (число)', max_length=16, default='24/7')
    hero_stat_label = models.CharField(
        'Hero картка (підпис)',
        max_length=120,
        default='стаціонар інтенсивної терапії',
    )
    is_open_now = models.BooleanField('Працюємо зараз', default=True)
    trust_label = models.CharField('Trust strip', max_length=64, default='Працюємо зараз')
    hours_label = models.CharField('Години роботи', max_length=64, default='Цілодобово')

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
