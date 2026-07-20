from django.db import migrations

ENDOSCOPY_BULLETS = [
    'Гастроскопія',
    'Отоскопія',
    'Ріноскопія',
    'Бронхоскопія',
    'Мінімально інвазивно',
]
ENDOSCOPY_BULLETS_OLD = [
    'Гастроскопія',
    'Колоноскопія',
    'Бронхоскопія',
    'Мінімально інвазивно',
]

DERMATOLOGY_BULLETS = [
    'Огляд шкіри',
    'Дерматологічні дослідження',
    'Алергологічні тести',
    'План лікування',
]
DERMATOLOGY_BULLETS_OLD = [
    'Огляд шкіри',
    'Соскопи',
    'Алергологічні тести',
    'План лікування',
]


def update_bullets(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Service.objects.filter(slug='endoscopy').update(bullets=ENDOSCOPY_BULLETS)
    Service.objects.filter(slug='dermatology').update(bullets=DERMATOLOGY_BULLETS)


def restore_bullets(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Service.objects.filter(slug='endoscopy').update(bullets=ENDOSCOPY_BULLETS_OLD)
    Service.objects.filter(slug='dermatology').update(bullets=DERMATOLOGY_BULLETS_OLD)


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0010_remove_doctor_rating'),
    ]

    operations = [
        migrations.RunPython(update_bullets, restore_bullets),
    ]
