from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

Modulo = apps.get_model(app_label='progame', model_name='Modulo')
StatsAlunoModulo = apps.get_model(app_label='progame', model_name='StatsAlunoModulo')
Quiz = apps.get_model(app_label='quiz', model_name='Quiz')


@receiver(post_save, sender=Modulo)
def criar_quizzes_do_modulo(sender, instance, created, *args, **kwargs):
    modulo = instance

    if created:
        for nivel in range(1, 7):
            Quiz.objects.create(nivel=nivel, modulo=modulo)


@receiver(post_save, sender=Modulo)
def criar_stats_aluno_no_modulo(sender, instance, created, *args, **kwargs):
    modulo = instance

    if created:
        for aluno in modulo.turma.alunos.all():
            StatsAlunoModulo.objects.get_or_create(aluno=aluno, modulo=modulo)
