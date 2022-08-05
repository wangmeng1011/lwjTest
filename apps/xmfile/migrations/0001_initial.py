# Generated by Django 3.1.2 on 2022-08-05 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apiTest', '0006_auto_20220711_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='XmFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='文件名称')),
                ('path', models.CharField(max_length=300, verbose_name='oss文件地址')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('suffix_name', models.CharField(max_length=50, verbose_name='文件名称')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apiTest.project', verbose_name='关联的项目')),
            ],
            options={
                'verbose_name': 'xmind文件',
                'verbose_name_plural': 'xmind文件',
                'db_table': 'fusion_xm_file',
                'ordering': ['-create_time'],
            },
        ),
    ]
