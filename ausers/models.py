from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.apps import apps
import uuid

User = get_user_model()


class Aluno(models.Model):

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    imagem = models.ImageField(null=True, blank=True, upload_to='alunos', max_length=500)
    turmas_favoritas = models.ManyToManyField('progame.Turma')

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.username:
            return self.user.username
        else:
            return self.user.email

    def get_posicao_na_turma(self, turma):
        """
        Retorna a posição do aluno na turma
        """
        Resposta = apps.get_model(app_label='progame', model_name='Resposta')
        ranking_alunos = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo__turma=turma).order_by('-total_pontos')

        if not ranking_alunos:
            return None

        aluno = [item for item in ranking_alunos if item['aluno'] == self.pk]

        posicao = list(ranking_alunos).index(aluno[0]) + 1
        return posicao

    def get_posicao_no_modulo(self, modulo):
        """
        Retorna posição do aluno no módulo
        """
        Resposta = apps.get_model(app_label='progame', model_name='Resposta')
        ranking_alunos = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo=modulo).order_by('-total_pontos')

        if not ranking_alunos:
            return None

        aluno = [item for item in ranking_alunos if item['aluno'] == self.pk]

        posicao = list(ranking_alunos).index(aluno[0]) + 1
        return posicao

    def acertou_questao_em_tentativa_que_foi_aprovado(self, questao):
        """
        Retorna se aluno já acertou a questão especificada
        em uma tentativa que ele foi aprovado
        """
        Tentativa = apps.get_model(app_label='quiz', model_name='Tentativa')
        for tentativa in Tentativa.objects.filter(aluno=self):
            if tentativa.aprovado:
                for resposta in tentativa.respostas.all():
                    if resposta.questao.pk == questao.pk and resposta.acertou:
                        return True

        return False


class Professor(models.Model):
    class Meta:
        verbose_name_plural = 'professores'

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')
    imagem = models.ImageField(null=True, blank=True, upload_to='professores', max_length=500)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.username:
            return self.user.username
        else:
            return self.user.email


def is_aluno(self):
    try:
        if self.aluno:
            return True
        return False

    except ObjectDoesNotExist:
        return False


def is_professor(self):
    try:
        if self.professor:
            return True
        return False

    except ObjectDoesNotExist:
        return False


User.add_to_class("is_aluno", is_aluno)
User.add_to_class("is_professor", is_professor)
