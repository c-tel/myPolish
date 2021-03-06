# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polish', '0003_grammarrule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('num', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='WordQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quest', models.CharField(max_length=16)),
                ('vars', models.CharField(max_length=64)),
                ('ans', models.CharField(max_length=16)),
            ],
        ),
        migrations.AlterField(
            model_name='word',
            name='pl',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='word',
            name='transcript',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='word',
            name='uk',
            field=models.CharField(max_length=32),
        ),
    ]
