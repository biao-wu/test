# Generated by Django 2.1.4 on 2020-05-06 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200506_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='waterdata',
            old_name='cTime',
            new_name='time',
        ),
    ]
