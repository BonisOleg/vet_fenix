from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_sitesettings_reassessment_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='reassessment_hours_label',
            field=models.TextField(
                blank=True,
                default='9:30–10:30 та 20:00–21:00 — прийом лише екстрених пацієнтів',
                verbose_name='Час зміни лікарів',
            ),
        ),
    ]
