# Generated by Django 2.1.4 on 2020-05-20 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200519_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterdata',
            name='status',
        ),
        migrations.AddField(
            model_name='site',
            name='status',
            field=models.IntegerField(choices=[(1, '正常'), (2, '异常'), (0, '离线')], default=1, verbose_name='站点状态'),
        ),
    ]
