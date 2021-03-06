# Generated by Django 3.0.4 on 2020-07-18 22:30

from django.db import migrations


def adicionar_questoes(apps, schema_editor):
    Quiz = apps.get_model('quiz', 'Quiz')
    Questao = apps.get_model('progame', 'Questao')

    for questao in Questao.objects.all():
        quiz = Quiz.objects.get(nivel=questao.nivel, modulo_id=questao.modulo.pk)
        quiz.questoes.add(questao)


class Migration(migrations.Migration):

    dependencies = [
        ('progame', '0026_auto_20200713_1832'),
    ]

    operations = [
    ]
