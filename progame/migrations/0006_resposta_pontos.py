# Generated by Django 3.0.4 on 2020-04-15 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progame', '0005_auto_20200414_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='resposta',
            name='pontos',
            field=models.PositiveIntegerField(default=0),
        ),
    ]