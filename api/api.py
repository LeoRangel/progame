import json

from django.utils.text import Truncator
from rest_framework.exceptions import PermissionDenied

from core.utils import arredondar
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from progame.utils import get_questoes_corretas, get_tempo_medio_por_questao
from rest_framework import permissions
from collections import namedtuple
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from progame.models import Turma, Modulo, Questao, Alternativa, Resposta, StatsAlunoModulo
from sistema.settings import MEDIA_DE_APROVACAO, QUESTOES_SUFICIENTES_PARA_LIBERAR_QUIZ
from .permissions import pode_acessar_pagina_do_quiz
from .serializers import TurmaSerializer, ModuloSerializer, QuizSerializer, QuestaoSerializer, AlternativaSerializer, \
    RespostaSerializer, AlunoSerializer
from ausers.models import Aluno as AlunoModel
from quiz.models import Tentativa, Quiz as QuizModel


Quiz = namedtuple('Quiz', ('turma', 'modulo'))
Aluno = namedtuple('Aluno', ('id', 'user'))


class AlunoRetrieve(RetrieveAPIView):
    """
    Retorna informações do aluno juntamente com o user
    """
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        aluno_obj = AlunoModel.objects.get(pk=request.user.aluno.pk)
        aluno = Aluno(
            id=aluno_obj.pk,
            user=aluno_obj.user
        )
        serializer = AlunoSerializer(aluno)
        return Response(serializer.data)


class QuizRetrieve(RetrieveAPIView):
    """
    Retorna informações do quiz: turma e módulo
    """

    def retrieve(self, request, *args, **kwargs):
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['modulo_uuid'])
        quiz = get_object_or_404(QuizModel, modulo=modulo, nivel=self.kwargs['nivel'])

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            quiz = Quiz(
                turma=modulo.turma,
                modulo=modulo
            )
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)

        raise PermissionDenied


class TurmaRetrieve(RetrieveAPIView):
    serializer_class = TurmaSerializer

    def get_object(self):
        return get_object_or_404(Turma, uuid=self.kwargs['uuid'])


class ModuloList(ListAPIView):
    serializer_class = ModuloSerializer

    def get_queryset(self):
        return Modulo.objects.filter(turma__uuid=self.kwargs['turma_uuid'])


class ModuloRetrieve(RetrieveAPIView):
    serializer_class = ModuloSerializer

    def get_object(self):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])


class QuestaoRetrieve(RetrieveAPIView):
    serializer_class = QuestaoSerializer

    def get_object(self):
        questao = get_object_or_404(Questao, uuid=self.kwargs['uuid'])
        quiz = get_object_or_404(QuizModel, modulo=questao.modulo, nivel=questao.nivel)

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            return questao

        raise PermissionDenied()


class QuestaoList(ListAPIView):
    serializer_class = QuestaoSerializer

    def get_queryset(self):
        quiz = get_object_or_404(QuizModel, modulo__uuid=self.kwargs['modulo_uuid'], nivel=self.kwargs['nivel'])

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            return Questao.objects.filter(modulo__uuid=self.kwargs['modulo_uuid'], nivel=self.kwargs['nivel'])\
                .order_by('?')

        raise PermissionDenied()


class AlternativaQuestaoList(ListAPIView):
    serializer_class = AlternativaSerializer

    def get_queryset(self):
        alternativas = Alternativa.objects.filter(questao__uuid=self.kwargs['questao_uuid'])
        questao = alternativas.first().questao
        quiz = get_object_or_404(QuizModel, modulo=questao.modulo, nivel=questao.nivel)

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            return alternativas

        raise PermissionDenied()


class AlternativaModuloNivelList(ListAPIView):
    serializer_class = AlternativaSerializer

    def get_queryset(self):
        quiz = get_object_or_404(QuizModel, modulo__uuid=self.kwargs['modulo_uuid'], nivel=self.kwargs['questao_nivel'])

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            return Alternativa.objects.filter(questao__modulo__uuid=self.kwargs['modulo_uuid'],
                                              questao__nivel=self.kwargs['questao_nivel'])

        raise PermissionDenied()


class AlternativaCorretaList(ListAPIView):
    serializer_class = AlternativaSerializer

    def get_queryset(self):
        alternativas = Alternativa.objects.filter(questao__uuid=self.kwargs['questao_uuid'], is_correta=True)
        questao = alternativas.first().questao
        quiz = get_object_or_404(QuizModel, modulo=questao.modulo, nivel=questao.nivel)

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            return alternativas

        return PermissionDenied()


class RespostaCreate(CreateAPIView):
    serializer_class = RespostaSerializer

    def perform_create(self, serializer):
        questao = get_object_or_404(Questao, pk=self.request.data['questao'])
        quiz = get_object_or_404(QuizModel, modulo=questao.modulo, nivel=questao.nivel)

        if self.request.user.is_aluno() and pode_acessar_pagina_do_quiz(self.request, quiz):
            serializer.save(aluno=self.request.user.aluno)
            return Response(serializer.data)

        raise PermissionDenied()


class ResultadoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        """
        data = {
           aluno: 1,
           modulo: 1,
           respostas: []
        }
        """

        respostas = Resposta.objects.filter(id__in=[r['id'] for r in data['respostas']])  # respostas do quiz

        nivel_quiz = int(respostas.first().questao.nivel)  # nivel do quiz
        quiz = QuizModel.objects.get(modulo_id=data['modulo'], nivel=nivel_quiz)

        if not pode_acessar_pagina_do_quiz(request, quiz):
            raise PermissionDenied()

        # questoes_quiz = quiz.questoes.all()
        questoes_quiz = Questao.objects.filter(nivel=nivel_quiz, modulo_id=data['modulo'])
        questoes_corretas = get_questoes_corretas(data['respostas']).values()

        if questoes_quiz.count() == 2 and MEDIA_DE_APROVACAO == 0.7:
            media_de_aprovacao_quiz = 2
        else:
            media_de_aprovacao_quiz = arredondar(questoes_quiz.count() * MEDIA_DE_APROVACAO)

        pontos = respostas.aggregate(Sum('pontos'))['pontos__sum']

        # salva tentativa do aluno
        tentativa = Tentativa(quiz=quiz, aluno_id=data['aluno'])
        tentativa.save()
        tentativa.respostas.add(*respostas)

        aprovado_no_quiz = False
        if questoes_corretas.count() >= media_de_aprovacao_quiz:
            aprovado_no_quiz = True

        # recupera stats do aluno no modulo caso ja tenha
        # caso contrario, cria
        try:
            stats_aluno_modulo = StatsAlunoModulo.objects.get(aluno_id=data['aluno'], modulo_id=data['modulo'])
        except StatsAlunoModulo.DoesNotExist:
            stats_aluno_modulo = StatsAlunoModulo.objects.create(aluno_id=data['aluno'], modulo_id=data['modulo'])

        aluno, modulo = stats_aluno_modulo.aluno, stats_aluno_modulo.modulo
        turma = modulo.turma

        # subir nível do aluno caso ele acertou questões suficientes
        # e esteja um nível abaixo do quiz
        subiu_de_nivel = False
        if (int(stats_aluno_modulo.nivel) == nivel_quiz - 1) and aprovado_no_quiz:
            stats_aluno_modulo.nivel = int(stats_aluno_modulo.nivel) + 1
            stats_aluno_modulo.save()
            subiu_de_nivel = True

        try:
            proximo_quiz = QuizModel.objects.get(modulo_id=data['modulo'], nivel=nivel_quiz + 1)
            questoes = proximo_quiz.questoes.all()

            if questoes.count() >= QUESTOES_SUFICIENTES_PARA_LIBERAR_QUIZ:
                proximo_nivel_bloqueado = proximo_quiz.bloqueado
            else:
                proximo_nivel_bloqueado = True

        except QuizModel.DoesNotExist:
            proximo_nivel_bloqueado = True

        links = []
        for link in quiz.links_ajuda.order_by('-pk'):
            links.append({
                'id': link.pk,
                'nome': link.nome,
                'url': link.url,
                'nome_trunc': Truncator(link.nome).words(8),
                'url_trunc': Truncator(link.url).chars(45)
            })

        media_min_de_aprovacao = str(int(MEDIA_DE_APROVACAO * 100)) + '%'

        response_data = {
            'respostas': list(respostas.values()),
            'subiuDeNivel': subiu_de_nivel,
            'aprovadoNoQuiz': aprovado_no_quiz,
            'proximoNivelBloqueado': proximo_nivel_bloqueado,
            'nivelAlunoModulo': stats_aluno_modulo.nivel,
            'posicaoAlunoModulo': aluno.get_posicao_no_modulo(modulo=modulo),
            'posicaoAlunoTurma': aluno.get_posicao_na_turma(turma=turma),
            'questoesCorretas': list(questoes_corretas),
            'pontos': pontos,
            'tempoMedioPorQuestao': get_tempo_medio_por_questao(respostas),
            'linksDeEstudo': links,
            'mediaMinDeAprovacao': media_min_de_aprovacao
        }

        return JsonResponse(response_data)
