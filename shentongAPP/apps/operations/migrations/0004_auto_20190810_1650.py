# Generated by Django 2.2.1 on 2019-08-10 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_auto_20190809_2145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercomment',
            old_name='comment_man',
            new_name='user',
        ),
    ]
