from django.db import migrations, models

HERO_LEAD = (
    'Ветеринарна клініка «Фенікс» надає широкий спектр послуг для Ваших домашніх улюбленців. '
    'Наші фахівці працюють за актуальними протоколами, спираючись на доказову медицину. '
    'Клініка забезпечена новітнім обладнанням, що допомагає у швидкій діагностиці пацієнтів. '
    'З основних переваг — цілодобовий стаціонар інтенсивної терапії та реанімації. '
    'Постійне навчання, поглиблення знань та навичок персоналу, використання сучасних методів '
    'діагностики — шлях до успіху у лікуванні Ваших хвостиків.'
)

OLD_HERO_LEAD = (
    'Сучасна ветеринарна клініка в центрі Києва. Запис онлайн — за 30 секунд.'
)


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        clinic_name_line1='Ветеринарна клініка',
        clinic_name_line2='«Фенікс»',
        address='м. Київ, вул. Ірпінська, 67б',
        phone_primary='+380933839933',
        phone_secondary='+380983839033',
        email='',
        hero_title='Турбота про ваших улюбленців — цілодобово',
        hero_lead=HERO_LEAD,
        hero_stat_number='24/7',
        hero_stat_label='стаціонар інтенсивної терапії',
        hours_label='Цілодобово',
    )


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        clinic_name_line1='Ветеринарна',
        clinic_name_line2='клініка',
        address='м. Київ, вул. Хрещатик 1',
        phone_primary='+380441234567',
        phone_secondary='',
        email='info@vetclinic.ua',
        hero_title='Турбота про вашого улюбленця цілодобово',
        hero_lead=OLD_HERO_LEAD,
        hero_stat_number='12+',
        hero_stat_label='років допомагаємо тваринам Києва',
        hours_label='24/7 без вихідних',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_update_site_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_lead',
            field=models.TextField(
                default=(
                    'Ветеринарна клініка «Фенікс» надає широкий спектр послуг для Ваших домашніх '
                    'улюбленців. Наші фахівці працюють за актуальними протоколами, спираючись на '
                    'доказову медицину. Клініка забезпечена новітнім обладнанням, що допомагає у '
                    'швидкій діагностиці пацієнтів. З основних переваг — цілодобовий стаціонар '
                    'інтенсивної терапії та реанімації. Постійне навчання, поглиблення знань та '
                    'навичок персоналу, використання сучасних методів діагностики — шлях до успіху '
                    'у лікуванні Ваших хвостиків.'
                ),
                max_length=600,
                verbose_name='Підзаголовок hero',
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
