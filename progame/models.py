from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from ausers.models import Professor, Aluno
from datetime import datetime, date, timedelta
from django.utils import timezone
import uuid
from django.db.models import Sum

from sistema.settings import PONTUACAO_MAXIMA_POR_ACERTO, TEMPO_MAXIMO_PARA_RESPONDER

from core.utils import arredondar


NIVEL_CHOICES = (
    (0, 'Nenhum'),
    (1, '1 - Lembrar'),
    (2, '2 - Entender'),
    (3, '3 - Aplicar'),
    (4, '4 - Analisar'),
    (5, '5 - Avaliar'),
    (6, '6 - Criar'),
)


class TimestampableMixin(models.Model):
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True)

    @property
    def is_new(self):
        """
        Verifica se o objeto foi criado nas útimas 24 horas
        """
        difference = timezone.now() - self.criado_em
        return difference.days == 0


class Nivel(models.Model):
    class Meta:
        verbose_name = 'nível'
        verbose_name_plural = 'níveis'

    nivel = models.PositiveSmallIntegerField()
    nome = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.nivel} - {self.nome}'


class Verbo(models.Model):

    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='verbos')
    verbo = models.CharField(max_length=50, null=True)
    palavra = models.CharField(max_length=50)

    def __str__(self):
        return self.verbo


class Turma(TimestampableMixin):

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    nome = models.CharField('nome da turma', max_length=255)
    secao = models.CharField('seção', max_length=100, null=True, blank=True)
    sala = models.CharField(max_length=100, null=True, blank=True)
    descricao = RichTextUploadingField(null=True, blank=True)
    discord = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    codigo = models.CharField(max_length=6, null=True, editable=False, unique=True)
    imagem = models.ImageField(blank=True, null=True, upload_to='turmas', max_length=500)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='turmas')
    alunos = models.ManyToManyField(Aluno, blank=True)

    def __str__(self):
        return self.nome

    @property
    def get_info(self):
        if self.sala and self.secao:
            return f'Sala {self.sala}, {self.secao}'
        elif self.sala:
            return f'Sala {self.sala}'
        elif self.secao:
            return self.secao
        return None

    @property
    def lider(self):
        pontuacao_alunos = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo__turma_id=self.pk, aluno__in=self.alunos.all(), pontos__gt=0)

        if not pontuacao_alunos:
            return None

        # pega dict que contém aluno com maior quantidade de pontos
        aluno_dict = max(pontuacao_alunos, key=lambda x: x['total_pontos'])

        aluno = Aluno.objects.get(pk=aluno_dict['aluno'])
        pontos = aluno_dict['total_pontos']

        lider = {
            'aluno': aluno,
            'pontos': pontos
        }

        return lider

    @property
    def ranking(self):
        items = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo__turma_id=self.pk, aluno__in=self.alunos.all()).order_by('-total_pontos')

        ranking = []
        for item in items:
            aluno = Aluno.objects.get(pk=item['aluno'])
            ranking.append({
                'aluno': aluno,
                'pontos': item['total_pontos']
            })

        # caso todos os alunos tenham 0 pontos, não retorne o ranking
        if all(rnk['pontos'] == 0 for rnk in ranking):
            return None

        for aluno in self.alunos.all():
            if not any(rnk['aluno'] == aluno for rnk in ranking):
                ranking.append({
                    'aluno': aluno,
                    'pontos': 0
                })

        return ranking


class Modulo(TimestampableMixin):
    class Meta:
        verbose_name = 'módulo'
        verbose_name_plural = 'módulos'

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    nome = models.CharField('nome do módulo', max_length=50)
    descricao = models.TextField('descrição', null=True, blank=True, max_length=130)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='modulos')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.turma.atualizado_em = datetime.now()
        self.turma.save()
        super(Modulo, self).save(*args, **kwargs)

    def get_estatisticas_url(self):
        return reverse('stats:modulo_detail_view', kwargs={'uuid': self.uuid})

    @property
    def lider(self):
        alunos_turma = self.turma.alunos.all()
        respostas = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo_id=self.pk, aluno__in=alunos_turma, pontos__gt=0)

        if not respostas:
            return None

        # pega dict que contém aluno com maior quantidade de pontos
        aluno_dict = max(respostas, key=lambda x: x['total_pontos'])

        aluno = Aluno.objects.get(pk=aluno_dict['aluno'])
        pontos = aluno_dict['total_pontos']

        lider = {
            'aluno': aluno,
            'pontos': pontos
        }

        return lider

    @property
    def ranking(self):
        alunos_turma = self.turma.alunos.all()
        items = Resposta.objects.values('aluno').order_by('aluno').annotate(total_pontos=Sum('pontos'))\
            .filter(questao__modulo_id=self.pk, aluno__in=alunos_turma).order_by('-total_pontos')

        ranking = []
        for item in items:
            aluno = Aluno.objects.get(pk=item['aluno'])
            ranking.append({
                'aluno': aluno,
                'pontos': item['total_pontos']
            })

        # caso todos os alunos tenham 0 pontos, não retorne o ranking
        if all(rnk['pontos'] == 0 for rnk in ranking):
            return None

        for aluno in alunos_turma:
            if not any(rnk['aluno'] == aluno for rnk in ranking):
                ranking.append({
                    'aluno': aluno,
                    'pontos': 0
                })

        return ranking

    @property
    def qtd_alunos_finalizados(self):
        return StatsAlunoModulo.objects.filter(modulo=self, nivel__exact='6').count()

    @property
    def qtd_alunos_em_andamento(self):
        alunos = StatsAlunoModulo.objects.filter(modulo=self)

        qtd = 0
        for aluno in alunos:
            if 0 < int(aluno.nivel) < 6:
                qtd += 1

        return qtd

    @property
    def qtd_alunos_pendentes(self):
        return StatsAlunoModulo.objects.filter(modulo=self, nivel__exact='0').count()


class StatsAlunoModulo(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='niveis_modulos')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='niveis_alunos')
    nivel = models.CharField(choices=NIVEL_CHOICES, max_length=1, default=0)

    @property
    def verbose_nivel(self):
        return Nivel.objects.get(nivel=int(self.nivel))


class ItemConquista(models.Model):
    class Meta:
        verbose_name_plural = 'itens conquista'

    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=100, null=True)
    descricao2 = models.TextField(max_length=100, null=True)
    slug = models.SlugField(unique=True, editable=False, null=True)

    def __str__(self):
        return self.nome


class Conquista(models.Model):

    aluno = models.ForeignKey('ausers.Aluno', on_delete=models.CASCADE, related_name='conquistas', null=True)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, related_name='conquistas', null=True)
    item_conquista = models.ForeignKey(ItemConquista, on_delete=models.CASCADE)
    visualizado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item_conquista} - {self.timestamp}'


class Questao(models.Model):
    class Meta:
        verbose_name = 'questão'
        verbose_name_plural = 'questões'

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    sentenca = models.CharField('sentença', max_length=500)
    descricao = RichTextUploadingField('descrição da questão', null=True, blank=True)
    professor = models.ForeignKey('ausers.Professor', related_name='questoes', on_delete=models.CASCADE, null=True)
    tempo_para_responder = models.DurationField(default=timedelta(minutes=1))
    verbo = models.ForeignKey(Verbo, on_delete=models.SET_NULL, null=True)
    nivel = models.CharField('nível', max_length=1, choices=NIVEL_CHOICES, null=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True, related_name='questoes')

    def __str__(self):
        return self.sentenca

    def save(self, *args, **kwargs):
        self.modulo.atualizado_em = datetime.now()
        self.modulo.save()
        super(Questao, self).save(*args, **kwargs)

    
class Alternativa(models.Model):

    nome = models.TextField(max_length=700)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')
    is_correta = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.nome


class Resposta(models.Model):

    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='respostas_questao')
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, related_name='respostas_alternativa')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='respostas_aluno')
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    pontos = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        respostas_existentes = Resposta.objects.filter(aluno=self.aluno, questao=self.questao)
        respostas_existentes_com_ponto = respostas_existentes.filter(pontos__gt=0)
        qtd_tentativas = respostas_existentes.count()
        qtd_alternativas = self.questao.alternativas.count()

        if qtd_tentativas >= qtd_alternativas - 1 or respostas_existentes_com_ponto.count() > 0 or not self.acertou:
            """
            Caso tenha atingido o limite de tentativas, ou seja, 
            a qtd de tentativas é maior ou igual a qtd de alternativas da questão
            OU
            Já pontuou anteriormente nessa questão
            OU
            Não acertou
            """
            self.pontos = 0
        else:
            self.pontos = self.pontuacao_calculada

        super(Resposta, self).save(*args, **kwargs)

    @property
    def tempo_decorrido(self):
        if self.hora_fim and self.hora_inicio:
            return datetime.combine(date.min, self.hora_fim) - datetime.combine(date.min, self.hora_inicio)

        return 0

    @property
    def acertou(self):
        alternativas_corretas = self.questao.alternativas.filter(is_correta=True)
        return self.alternativa in alternativas_corretas

    @property
    def pontuacao_calculada(self):
        nivel_questao = int(self.questao.nivel)
        qtd_alternativas = self.questao.alternativas.count()
        qtd_tentativas = Resposta.objects.filter(aluno=self.aluno, questao=self.questao).count() + 1
        valor_questao = PONTUACAO_MAXIMA_POR_ACERTO[nivel_questao]

        porcentagem = 1 / (qtd_alternativas - 1)
        multiplicador = (qtd_alternativas - qtd_tentativas) * porcentagem

        pontuacao_por_tentativa = multiplicador * valor_questao

        r = self.tempo_decorrido.total_seconds()               # tempo decorrido
        q = self.questao.tempo_para_responder.total_seconds()  # tempo máx. para responder
        p = pontuacao_por_tentativa                            # pontuação máx. da questão

        if r > q:
            return 0

        pontuacao = arredondar((1 - (r / q / 2)) * p)

        if pontuacao < 0:
            return 0

        return pontuacao

    @property
    def pontuacao_acerto(self):
        qtd_alternativas = self.questao.alternativas.count()
        qtd_tentativas = Resposta.objects.filter(aluno=self.aluno, questao=self.questao).count() + 1
        valor_questao = PONTUACAO_MAXIMA_POR_ACERTO[int(self.questao.nivel)]

        porcentagem = 1 / (qtd_alternativas - 1)
        multiplicador = (qtd_alternativas - qtd_tentativas) * porcentagem

        pontuacao = multiplicador * valor_questao

        return pontuacao

    @property
    def pontuacao_tempo(self):
        """
        Para calcular a pontuação por tempo, é utilizada a equação: [1-(r/q/2)]p,
        onde r é o tempo (em segundos) após a questão iniciar, q é o tempo (em segundos) 
        total para responder a questão, e p é o número de pontos que você ganha 
        por responder a questão corretamente
        """
        nivel_questao = int(self.questao.nivel)

        r = self.tempo_decorrido.total_seconds()               # tempo decorrido
        q = self.questao.tempo_para_responder.total_seconds()  # tempo máx. para responder
        p = PONTUACAO_MAXIMA_POR_ACERTO[nivel_questao]         # pontuação máx. da questão

        pontuacao = (1 - (r / q / 2)) * p

        return int(pontuacao)
