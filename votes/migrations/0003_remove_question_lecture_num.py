# Generated by Django 2.0.2 on 2018-03-08 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20180227_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='lecture_num',
        ),
    ]
