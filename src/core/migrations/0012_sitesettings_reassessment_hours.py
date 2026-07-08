from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_update_proxy_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='reassessment_hours_label',
            field=models.TextField(
                blank=True,
                default='9:30–10:30 та 20:00–21:00 — прийом лише екстрених пацієнтів',
                verbose_name='Години переоцінки',
            ),
        ),
    ]
