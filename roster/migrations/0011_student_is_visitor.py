# Generated by Django 2.0.2 on 2018-03-02 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0010_visitor_temp_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_visitor',
            field=models.BooleanField(default=False),
        ),
    ]
