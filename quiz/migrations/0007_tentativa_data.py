# Generated by Django 3.0.4 on 2020-05-18 23:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20200509_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='tentativa',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]