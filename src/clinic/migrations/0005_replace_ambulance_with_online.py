from django.db import migrations, models


def replace_ambulance_with_online(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    try:
        service = Service.objects.get(slug='er')
    except Service.DoesNotExist:
        return
    service.slug = 'online'
    service.name = 'Онлайн-консультація'
    service.short_description = 'Дистанційна порада лікаря'
    service.full_description = (
        "Консультація ветеринара по відеозв'язку або телефону. "
        'Оцінка симптомів, рекомендації щодо лікування та необхідності візиту в клініку.'
    )
    service.price_hint = 'від 350 ₴'
    service.icon = 'video'
    service.bullets = [
        'Відео або телефон',
        'Зручний час',
        'Рекомендації лікування',
        'План візиту при потребі',
    ]
    service.is_urgent = False
    service.save()


def restore_ambulance_service(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    try:
        service = Service.objects.get(slug='online')
    except Service.DoesNotExist:
        return
    service.slug = 'er'
    service.name = 'Швидка'
    service.short_description = 'Цілодобовий виклик'
    service.full_description = (
        'Виїзд лікаря додому. Стабілізація і транспортування тварини у клініку.'
    )
    service.price_hint = 'від 700 ₴'
    service.icon = 'ambulance'
    service.bullets = [
        'Приїзд до 30 хв по Києву',
        'Реанімаційний автомобіль',
        'Перша допомога на місці',
        'Транспортування у клініку',
    ]
    service.is_urgent = True
    service.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_contactmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='icon',
            field=models.CharField(
                choices=[
                    ('stethoscope', 'Стетоскоп'),
                    ('syringe', 'Шприц'),
                    ('scissors', 'Ножиці'),
                    ('scan', 'Діагностика'),
                    ('tooth', 'Зуб'),
                    ('video', 'Онлайн'),
                ],
                default='stethoscope',
                max_length=32,
            ),
        ),
        migrations.RunPython(replace_ambulance_with_online, restore_ambulance_service),
    ]
