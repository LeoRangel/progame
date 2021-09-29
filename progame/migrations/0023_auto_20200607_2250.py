# Generated by Django 3.0.4 on 2020-06-08 01:50

from django.db import migrations


def get_data_back_to_questao(apps, schema_editor):
    Quiz = apps.get_model('quiz', 'Quiz')
    Questao = apps.get_model('progame', 'Questao')

    for quiz in Quiz.objects.all():
        for questao in quiz.questoes.all():
            questao.modulo = quiz.modulo
            questao.save()


class Migration(migrations.Migration):

    dependencies = [
        ('progame', '0022_auto_20200607_2155'),
    ]

    operations = [
        migrations.RunPython(get_data_back_to_questao)
    ]