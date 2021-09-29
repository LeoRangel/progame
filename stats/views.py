from datetime import timezone

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import strftime
from django.views.generic import DetailView, ListView
from django.views import View

from ausers.models import Aluno
from ausers.templatetags.ausers_tags import check_professor
from ausers.utils import ProfessorMixin
from progame.models import Turma, Modulo, StatsAlunoModulo
from progame.templatetags.progame_tags import get_pontuacao_na_turma
from quiz.models import Tentativa, Quiz
from stats.utils import get_questoes_com_dificuldade, get_tentativas_por_aluno, get_historico_de_respostas


class ModuloListView(ProfessorMixin, ListView):
    template_name = 'stats/modulo/modulostats_list_view.html'
    model = Modulo

    def get_context_data(self, **kwargs):
        context = super(ModuloListView, self).get_context_data(**kwargs)
        context['turma'] = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        context['active'] = ['stats', 'modulo']
        return context

    def get_queryset(self):
        return Modulo.objects.filter(turma__uuid=self.kwargs['uuid'])


class ModuloDetailView(ProfessorMixin, DetailView):
    template_name = 'stats/modulo/modulostats_detail_view.html'
    model = Modulo

    def get_context_data(self, **kwargs):
        context = super(ModuloDetailView, self).get_context_data(**kwargs)
        context['turma'] = self.object.turma
        context['active'] = ['stats', 'modulo']
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])


class AlunoListView(ProfessorMixin, ListView):
    template_name = 'stats/aluno/alunostats_list_view.html'
    model = Aluno

    def get_context_data(self, **kwargs):
        context = super(AlunoListView, self).get_context_data(**kwargs)
        context['turma'] = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        context['active'] = ['stats', 'aluno']
        return context

    def get_queryset(self):
        return get_object_or_404(Turma, uuid=self.kwargs['uuid']).alunos.all()


class AlunoDetailView(ProfessorMixin, DetailView):
    template_name = 'stats/aluno/alunostats_detail_view.html'
    model = Aluno

    def get_object(self, queryset=None):
        return get_object_or_404(Aluno, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(AlunoDetailView, self).get_context_data(**kwargs)
        context['turma'] = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        context['active'] = ['stats', 'aluno']
        return context


class GetAlunoModuloInfo(ProfessorMixin, View):

    def test_func(self):
        modulo = get_object_or_404(Modulo, uuid=self.request.GET.get('modulo_uuid'))
        return check_professor(modulo.turma, self.request)

    def get(self, request, *args, **kwargs):
        aluno = get_object_or_404(Aluno, pk=self.kwargs['pk'])
        modulo = get_object_or_404(Modulo, uuid=self.request.GET.get('modulo_uuid'))
        nivel_aluno = StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo).verbose_nivel

        modulo_info = {
            'nome': modulo.nome,
            'descricao': modulo.descricao,
            'nivelAluno': nivel_aluno.nivel,
            'nivelAlunoDescricao': nivel_aluno.nome
        }

        tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo)

        tentativas_por_quiz_dict = {}
        for tentativa in tentativas.order_by('quiz__nivel', 'numero'):
            nivel = tentativa.quiz.verbose_nivel.__str__()
            datetime_local = tentativa.data.replace(tzinfo=timezone.utc).astimezone(tz=None)
            tentativa = {
                'numero': tentativa.numero,
                'data': strftime(datetime_local, "%d/%m/%Y %H:%M"),
                'acertos': tentativa.qtd_acertos,
                'erros': tentativa.respostas.count() - tentativa.qtd_acertos,
                'pontuacao': tentativa.pontuacao
            }

            if nivel not in tentativas_por_quiz_dict:
                tentativas_por_quiz_dict.update({nivel: [tentativa]})
            else:
                tentativas_por_quiz_dict[nivel].append(tentativa)

        response = {
            'moduloInfo': modulo_info,
            'questoesComDificuldade': get_questoes_com_dificuldade(aluno, modulo),
            'questoesQueEsteveComDificuldade': get_questoes_com_dificuldade(aluno, modulo, quizzes_concluidos=True),
            'quizzes': tentativas_por_quiz_dict,
        }

        return JsonResponse(response, safe=False)


class GetQuizInfo(ProfessorMixin, View):

    def test_func(self):
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        return check_professor(modulo.turma, self.request)

    def get(self, request, *args, **kwargs):
        modulo = Modulo.objects.get(uuid=self.kwargs['uuid'])
        quiz = get_object_or_404(Quiz, modulo=modulo, nivel=self.request.GET.get('nivel'))
        stats_modulo = StatsAlunoModulo.objects.filter(modulo=modulo)

        nivel_info = {
            'nivel': quiz.nivel,
            'descricao': quiz.verbose_nivel.nome
        }

        range_niveis = []
        [range_niveis.append(str(nivel)) for nivel in range(int(quiz.nivel), 7)]

        completaram = stats_modulo.filter(nivel__in=range_niveis).count()

        em_andamento = 0
        for stat in stats_modulo.filter(nivel=str(int(quiz.nivel) - 1)):
            qtd_tentativas = Tentativa.objects.filter(aluno=stat.aluno, quiz=quiz).count()
            if qtd_tentativas > 0:
                em_andamento += 1

        range_niveis_pendentes = []
        [range_niveis_pendentes.append(nivel) for nivel in range(int(quiz.nivel))]

        pendentes = 0
        for stat in stats_modulo.filter(nivel__in=range_niveis_pendentes):
            qtd_tentativas = Tentativa.objects.filter(aluno=stat.aluno, quiz=quiz).count()
            if qtd_tentativas == 0:
                pendentes += 1

        alunos = {
            'completaram': completaram,
            'emAndamento': em_andamento,
            'pendentes': pendentes
        }

        response = {
            'nivelInfo': nivel_info,
            'alunos': alunos,
            # 'questoesComMaisDificuldade':
            # 'alunosComMaisDificuldade':
            'tentativasPorAluno': get_tentativas_por_aluno(quiz),
            'historicoDeRespostas': get_historico_de_respostas(quiz)
        }

        return JsonResponse(response, safe=False)


class GetModuloAlunoInfo(ProfessorMixin, View):

    def test_func(self):
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        return check_professor(modulo.turma, self.request)

    def get(self, request, *args, **kwargs):
        aluno = get_object_or_404(Aluno, pk=self.request.GET.get('aluno_pk'))
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        nivel_aluno = StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo).verbose_nivel

        aluno_info = {
            'nome': aluno.__str__(),
            'pontosNaTurma': get_pontuacao_na_turma(aluno, modulo.turma),
            # 'pontosNoModulo': ...
            'nivelAluno': nivel_aluno.nivel,
            'nivelAlunoDescricao': nivel_aluno.nome
        }

        tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo)

        tentativas_por_quiz_dict = {}
        for tentativa in tentativas.order_by('quiz__nivel', 'numero'):
            nivel = tentativa.quiz.verbose_nivel.__str__()
            datetime_local = tentativa.data.replace(tzinfo=timezone.utc).astimezone(tz=None)
            tentativa = {
                'numero': tentativa.numero,
                'data': strftime(datetime_local, "%d/%m/%Y %H:%M"),
                'acertos': tentativa.qtd_acertos,
                'erros': tentativa.respostas.count() - tentativa.qtd_acertos,
                'pontuacao': tentativa.pontuacao
            }

            if nivel not in tentativas_por_quiz_dict:
                tentativas_por_quiz_dict.update({nivel: [tentativa]})
            else:
                tentativas_por_quiz_dict[nivel].append(tentativa)

        response = {
            'alunoInfo': aluno_info,
            'questoesComDificuldade': get_questoes_com_dificuldade(aluno, modulo),
            'questoesQueEsteveComDificuldade': get_questoes_com_dificuldade(aluno, modulo, quizzes_concluidos=True),
            'quizzes': tentativas_por_quiz_dict,
        }

        return JsonResponse(response, safe=False)
