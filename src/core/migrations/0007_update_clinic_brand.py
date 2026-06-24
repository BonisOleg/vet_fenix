from django.db import migrations


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        clinic_name_line1='ветеринарна клініка',
        clinic_name_line2='Фенікс',
    )


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        clinic_name_line1='Ветеринарна клініка',
        clinic_name_line2='«Фенікс»',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_phoenix_site_content'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
