# Generated by Django 3.1.2 on 2021-02-19 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caseapilist',
            name='reset_expect_data',
        ),
        migrations.AlterField(
            model_name='caseapilist',
            name='reset_expect_code',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='预期状态码'),
        ),
    ]
