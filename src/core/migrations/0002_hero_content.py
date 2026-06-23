from django.db import migrations, models


def update_hero_content(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        hero_lead=(
            'Сучасна ветеринарна клініка в центрі Києва. Досвідчені лікарі, '
            'своя лабораторія, виклик додому. Запис онлайн за 30 секунд.'
        ),
        hero_stat_number='30 хв',
        hero_stat_label='виклик додому по Києву',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_lead',
            field=models.CharField(
                default=(
                    'Сучасна ветеринарна клініка в центрі Києва. Досвідчені лікарі, '
                    'своя лабораторія, виклик додому. Запис онлайн за 30 секунд.'
                ),
                max_length=255,
                verbose_name='Підзаголовок hero',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_stat_number',
            field=models.CharField(
                default='30 хв',
                max_length=16,
                verbose_name='Hero картка (число)',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_stat_label',
            field=models.CharField(
                default='виклик додому по Києву',
                max_length=120,
                verbose_name='Hero картка (підпис)',
            ),
        ),
        migrations.RunPython(update_hero_content, migrations.RunPython.noop),
    ]
