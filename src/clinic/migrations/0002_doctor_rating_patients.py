from decimal import Decimal

from django.db import migrations, models


def set_doctor_stats(apps, schema_editor):
    Doctor = apps.get_model('clinic', 'Doctor')
    stats = {
        'shevchuk': (Decimal('4.9'), '2400+ пацієнтів'),
        'kovalenko': (Decimal('4.8'), '1800+ пацієнтів'),
        'lytvyn': (Decimal('4.9'), '1200+ пацієнтів'),
        'bilyk': (Decimal('4.9'), '1600+ пацієнтів'),
    }
    for slug, (rating, patients_label) in stats.items():
        Doctor.objects.filter(slug=slug).update(
            rating=rating,
            patients_label=patients_label,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='patients_label',
            field=models.CharField(
                default='1000+ пацієнтів',
                help_text='Наприклад: 2400+ пацієнтів',
                max_length=32,
                verbose_name='Пацієнти',
            ),
        ),
        migrations.AddField(
            model_name='doctor',
            name='rating',
            field=models.DecimalField(
                decimal_places=1,
                default=4.9,
                max_digits=2,
                verbose_name='Рейтинг',
            ),
        ),
        migrations.RunPython(set_doctor_stats, migrations.RunPython.noop),
    ]
