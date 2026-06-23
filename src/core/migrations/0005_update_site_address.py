from django.db import migrations

NEW_ADDRESS = 'м. Київ, вул. Хрещатик 1'


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(address=NEW_ADDRESS)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        address='м. Київ, вул. Велика Васильківська, 100',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_doctor_bio_and_address'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
