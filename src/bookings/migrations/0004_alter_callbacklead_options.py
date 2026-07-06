# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_alter_appointmentrequest_comment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='callbacklead',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Запит на передзвінок',
                'verbose_name_plural': 'Запити на передзвінок',
            },
        ),
    ]
