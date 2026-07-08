from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_alter_advantage_description_alter_advantage_icon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='rating',
        ),
    ]
