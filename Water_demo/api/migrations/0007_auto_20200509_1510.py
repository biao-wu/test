# Generated by Django 2.1.4 on 2020-05-09 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200509_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlogs',
            name='opa',
            field=models.CharField(max_length=200, null=True, verbose_name='操作记录'),
        ),
    ]
