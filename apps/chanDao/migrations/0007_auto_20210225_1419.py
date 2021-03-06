# Generated by Django 3.1.2 on 2021-02-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chanDao', '0006_auto_20210224_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chandaocase',
            name='case_priority',
            field=models.IntegerField(choices=[[1, 1], [2, 2], [3, 3], [4, 4]], verbose_name='优先级'),
        ),
        migrations.AlterField(
            model_name='chandaocasestep',
            name='expect',
            field=models.CharField(max_length=3000, verbose_name='预期'),
        ),
        migrations.AlterField(
            model_name='chandaocasestep',
            name='remarks',
            field=models.CharField(max_length=3000, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='chandaocasestep',
            name='step',
            field=models.CharField(max_length=3000, verbose_name='步骤'),
        ),
    ]
