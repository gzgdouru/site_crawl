# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-15 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('url_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='url唯一标识')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='章节链接')),
                ('index', models.PositiveIntegerField(unique=True, verbose_name='章节顺序')),
                ('name', models.CharField(max_length=128, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repo.Novel', verbose_name='所属小说')),
            ],
            options={
                'db_table': 'tb_chapter',
            },
        ),
    ]