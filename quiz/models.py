from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.text import Truncator

from ausers.models import Aluno
from core.utils import arredondar
from progame.models import Alternativa, Resposta, Modulo, StatsAlunoModulo, Questao, Nivel, NIVEL_CHOICES, TimestampableMixin
import uuid

from progame.utils import get_questoes_corretas
from sistema.settings import QUESTOES_SUFICIENTES_PARA_LIBERAR_QUIZ, MEDIA_DE_APROVACAO


class LinkAjuda(TimestampableMixin):
    class Meta:
        verbose_name = 'link de ajuda'
        verbose_name_plural = 'links de ajuda'

    nome = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(max_length=300)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        if self.nome:
            return self.nome

        return Truncator(self.url).chars(45)

    @property
    def quiz(self):
        try:
            quiz = Quiz.objects.get(links_ajuda=self)
        except Quiz.DoesNotExist:
            quiz = None

        return quiz


class Quiz(models.Model):
    class Meta:
        verbose_name_plural = 'quizzes'

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    nivel = models.CharField(choices=NIVEL_CHOICES, max_length=1, default=0)
    questoes = models.ManyToManyField(Questao, related_name='quizzes')
    modulo = models.ForeignKey(Modulo, related_name='quizzes', on_delete=models.CASCADE, null=True)
    links_ajuda = models.ManyToManyField(LinkAjuda, related_name='quizzes')
    bloqueado = models.BooleanField('bloquear', default=False)

    def __str__(self):
        return f'Nível {self.nivel} - {self.modulo}'

    @property
    def verbose_nivel(self):
        return Nivel.objects.get(nivel=int(self.nivel))

    @property
    def min_questoes(self):
        return QUESTOES_SUFICIENTES_PARA_LIBERAR_QUIZ

    @property
    def has_questoes_suficientes(self):
        qtd_questoes = self.modulo.questoes.filter(nivel=self.nivel).count()

        if qtd_questoes >= self.min_questoes:
            return True
        return False

    @property
    def porcentagem_de_acertos(self):
        tentativas = self.tentativas.all()

        qtd_respostas = 0
        qtd_respostas_corretas = 0

        for tentativa in tentativas:
            qtd_respostas += tentativa.respostas.count()

            for resposta in tentativa.respostas.all():
                if resposta.acertou:
                    qtd_respostas_corretas += 1

        try:
            porcentagem = 100 * qtd_respostas_corretas / qtd_respostas
            porcentagem = "%.1f" % porcentagem
        except ZeroDivisionError:
            porcentagem = 0

        return porcentagem

    @property
    def qtd_alunos_finalizados(self):
        alunos_stats = StatsAlunoModulo.objects.filter(modulo=self.modulo)
        qtd_finalizados = 0
        for aluno in alunos_stats:
            if int(aluno.nivel) >= int(self.nivel):
                qtd_finalizados += 1

        return qtd_finalizados

    @property
    def qtd_alunos_em_andamento(self):
        alunos_stats = StatsAlunoModulo.objects.filter(modulo=self.modulo)
        qtd_em_andamento = 0
        for aluno in alunos_stats:
            qtd_tentativas = Tentativa.objects.filter(aluno=aluno.aluno, quiz=self).count()
            if int(aluno.nivel) == int(self.nivel)-1 and qtd_tentativas > 0:
                qtd_em_andamento += 1

        return qtd_em_andamento

    @property
    def qtd_alunos_pendentes(self):
        alunos_stats = StatsAlunoModulo.objects.filter(modulo=self.modulo)
        qtd_pendentes = 0
        for aluno in alunos_stats:
            qtd_tentativas = Tentativa.objects.filter(aluno=aluno.aluno, quiz=self).count()
            if int(aluno.nivel) <= int(self.nivel)-1 and qtd_tentativas == 0:
                qtd_pendentes += 1

        return qtd_pendentes


class Tentativa(models.Model):

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    numero = models.PositiveIntegerField()
    respostas = models.ManyToManyField(Resposta, blank=True)
    quiz = models.ForeignKey(Quiz, related_name='tentativas', on_delete=models.CASCADE, null=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, null=True, related_name='tentativas')
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Aluno: {self.aluno} - Tentativa: {self.numero}'

    def save(self, *args, **kwargs):
        numero_existente = Tentativa.objects.filter(aluno=self.aluno, quiz=self.quiz)\
            .aggregate(Max('numero'))['numero__max']

        if numero_existente is None:
            self.numero = 1
        else:
            self.numero = numero_existente + 1

        super(Tentativa, self).save(*args, **kwargs)

    @property
    def qtd_acertos(self):
        counter = 0
        for resposta in self.respostas.all():
            if resposta.acertou:
                counter += 1

        return counter

    @property
    def pontuacao(self):
        pontos = 0
        for resposta in self.respostas.all():
            pontos += resposta.pontuacao_calculada

        return pontos

    @property
    def questoes(self):
        return Questao.objects.filter(pk__in=[resposta.questao.pk for resposta in self.respostas.all()])

    @property
    def aprovado(self):
        if self.questoes.count() == 2 and MEDIA_DE_APROVACAO == 0.7:
            media_de_aprovacao_quiz = 2
        else:
            media_de_aprovacao_quiz = arredondar(self.questoes.count() * MEDIA_DE_APROVACAO)

        respostas_corretas = Alternativa.objects.filter(
            id__in=[resposta.alternativa.pk for resposta in self.respostas.all()],
            is_correta=True
        )

        aprovado_no_quiz = False
        if respostas_corretas.count() >= media_de_aprovacao_quiz:
            aprovado_no_quiz = True

        return aprovado_no_quiz
