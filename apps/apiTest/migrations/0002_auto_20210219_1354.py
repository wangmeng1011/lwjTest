# Generated by Django 3.1.2 on 2021-02-19 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='host_api', to='apiTest.host', verbose_name='host'),
        ),
    ]