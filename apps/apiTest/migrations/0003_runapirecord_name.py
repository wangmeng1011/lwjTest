# Generated by Django 3.1.2 on 2021-03-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiTest', '0002_auto_20210219_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='runapirecord',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='api名称'),
        ),
    ]
