# Generated by Django 2.0.2 on 2018-02-27 03:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='answer',
            new_name='answer_1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_active',
        ),
        migrations.AddField(
            model_name='question',
            name='question_state',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
        migrations.AddField(
            model_name='response',
            name='answer_2',
            field=models.IntegerField(default=0),
        ),
    ]