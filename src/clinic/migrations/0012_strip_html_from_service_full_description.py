import html
import re

from django.db import migrations
from django.utils.html import strip_tags


def _strip_full_descriptions(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    for service in Service.objects.all().iterator():
        raw = service.full_description or ''
        cleaned = html.unescape(strip_tags(raw)).strip()
        cleaned = re.sub(r'[ \t]+\n', '\n', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        if cleaned != raw:
            service.full_description = cleaned
            service.save(update_fields=['full_description'])


def _noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('clinic', '0011_update_endoscopy_dermatology_bullets'),
    ]

    operations = [
        migrations.RunPython(_strip_full_descriptions, _noop_reverse),
    ]
