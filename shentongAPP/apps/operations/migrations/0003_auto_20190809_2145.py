# Generated by Django 2.2.1 on 2019-08-09 21:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('operations', '0002_auto_20190808_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercourse',
            old_name='study_man',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='usercourse',
            unique_together={('user', 'study_course')},
        ),
    ]
