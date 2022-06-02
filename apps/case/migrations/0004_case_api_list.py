# Generated by Django 3.1.2 on 2021-02-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiTest', '0002_auto_20210219_1354'),
        ('case', '0003_auto_20210219_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='api_list',
            field=models.ManyToManyField(related_name='case_list', through='case.CaseApiList', to='apiTest.Api'),
        ),
    ]