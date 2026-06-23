from django.db import migrations, models

HERO_LEAD = 'Сучасна ветеринарна клініка в центрі Києва. Запис онлайн — за 30 секунд.'
HERO_STAT_NUMBER = '12+'
HERO_STAT_LABEL = 'років допомагаємо тваринам Києва'


def align_hero_copy(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        hero_lead=HERO_LEAD,
        hero_stat_number=HERO_STAT_NUMBER,
        hero_stat_label=HERO_STAT_LABEL,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_hero_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_lead',
            field=models.CharField(
                default=HERO_LEAD,
                max_length=255,
                verbose_name='Підзаголовок hero',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_stat_number',
            field=models.CharField(
                default=HERO_STAT_NUMBER,
                max_length=16,
                verbose_name='Hero картка (число)',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_stat_label',
            field=models.CharField(
                default=HERO_STAT_LABEL,
                max_length=120,
                verbose_name='Hero картка (підпис)',
            ),
        ),
        migrations.RunPython(align_hero_copy, migrations.RunPython.noop),
    ]
