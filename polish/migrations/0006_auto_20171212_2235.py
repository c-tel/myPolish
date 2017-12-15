# Generated by Django 2.0 on 2017-12-12 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polish', '0005_merge_20171210_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrammarQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.CharField(max_length=64)),
                ('gaps', models.CharField(max_length=64)),
                ('correct', models.CharField(max_length=16)),
                ('trans', models.CharField(max_length=64)),
                ('aab', models.CharField(max_length=1)),
                ('related_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polish.Test')),
            ],
        ),
        migrations.CreateModel(
            name='GrammarRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polish.GrammarQuiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WordRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='wordquiz',
            name='ans',
        ),
        migrations.AddField(
            model_name='wordquiz',
            name='correct',
            field=models.CharField(default=None, max_length=16),
        ),
        migrations.AddField(
            model_name='wordquiz',
            name='related_test',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='polish.Test'),
        ),
        migrations.AddField(
            model_name='wordrecord',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polish.WordQuiz'),
        ),
    ]