# Generated by Django 3.0.4 on 2020-05-01 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200426_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkAjuda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'link de ajuda',
                'verbose_name_plural': 'links de ajuda',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='links_ajuda',
            field=models.ManyToManyField(related_name='quizzes', to='quiz.LinkAjuda'),
        ),
    ]