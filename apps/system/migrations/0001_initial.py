# Generated by Django 3.1.2 on 2021-02-25 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apiTest', '0002_auto_20210219_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyetemQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000, verbose_name='问题')),
                ('handle', models.CharField(max_length=1000, verbose_name='如何处理')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.project', verbose_name='所属的项目')),
            ],
            options={
                'verbose_name': '系统问题',
                'verbose_name_plural': '系统问题',
                'db_table': 'fusion_question',
            },
        ),
        migrations.CreateModel(
            name='FormalBug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000, verbose_name='问题')),
                ('reason', models.CharField(max_length=1000, verbose_name='原因')),
                ('discoverer', models.CharField(max_length=10, null=True, verbose_name='发现人')),
                ('solve_time', models.CharField(max_length=100, verbose_name='解决时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.project', verbose_name='所属的项目')),
            ],
            options={
                'verbose_name': '现网漏侧问题',
                'verbose_name_plural': '现网漏侧问题',
                'db_table': 'fusion_formal_bug',
            },
        ),
    ]
