# Generated by Django 3.1.2 on 2022-07-11 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiTest', '0005_auto_20220629_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameterization',
            options={'ordering': ['create_time'], 'verbose_name': '参数化表达式', 'verbose_name_plural': '参数化表达式'},
        ),
    ]
