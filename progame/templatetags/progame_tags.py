from django import template
from django.db.models import Sum

from progame.models import StatsAlunoModulo, Resposta
from quiz.models import Tentativa, Quiz

register = template.Library()


@register.filter
def get_verbose_nivel(nivel):
    """
    Retorna nome do nível passado de acordo com a Taxonomia Revisada de Bloom
    """
    nivel = int(nivel)
    if nivel == 1:
        return 'Lembrar'
    elif nivel == 2:
        return 'Entender'
    elif nivel == 3:
        return 'Aplicar'
    elif nivel == 4:
        return 'Analisar'
    elif nivel == 5:
        return 'Avaliar'
    elif nivel == 6:
        return 'Criar'
    else:
        return None


@register.filter
def get_nivel_no_modulo(aluno, modulo):
    try:
        stats_aluno = StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo)
    except StatsAlunoModulo.DoesNotExist:
        stats_aluno = StatsAlunoModulo.objects.create(aluno=aluno, modulo=modulo)
        
    return int(stats_aluno.nivel)


@register.filter
def get_pontuacao_na_turma(aluno, turma):
    pontuacao = Resposta.objects.filter(aluno=aluno, questao__modulo__turma=turma).aggregate(Sum('pontos'))['pontos__sum']
    if pontuacao:
        return pontuacao

    return 0


@register.filter
def get_pontuacao_geral(aluno):
    pontuacao = Resposta.objects.filter(aluno=aluno).aggregate(Sum('pontos'))['pontos__sum']
    if pontuacao:
        return pontuacao

    return 0


@register.filter
def get_qtd_modulos_finalizados_aluno(aluno, turma):
    """
    Retorna quantidade de módulos finalizados pelo aluno na turma
    """
    return StatsAlunoModulo.objects.filter(aluno=aluno, modulo__turma=turma, nivel__exact='6').count()


@register.filter
def get_tentativas_no_modulo(aluno, modulo):
    return Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo).count()


@register.filter
def get_nota_no_modulo(aluno, modulo):
    qtd_questoes = 0
    qtd_questoes_acertadas = 0

    for quiz in Quiz.objects.filter(modulo=modulo):
        qtd_questoes += quiz.questoes.count()

        for questao in quiz.questoes.all():
            if aluno.acertou_questao_em_tentativa_que_foi_aprovado(questao):
                qtd_questoes_acertadas += 1

    try:
        nota = 10 * qtd_questoes_acertadas / qtd_questoes
        nota = float("%.1f" % nota)
    except ZeroDivisionError:
        nota = 0

    return nota


@register.filter
def get_tentativas_no_quiz(aluno, quiz):
    return Tentativa.objects.filter(aluno=aluno, quiz=quiz).count()


@register.filter
def get_porcentagem_de_acertos_no_quiz(aluno, quiz):
    ultima_tentativa = Tentativa.objects.filter(aluno=aluno, quiz=quiz).order_by('-pk')[0]
    questoes_respondidas = 0
    questoes_acertadas = 0

    questoes_respondidas += ultima_tentativa.respostas.count()

    for resposta in ultima_tentativa.respostas.all():
        if resposta.acertou:
            questoes_acertadas += 1

    try:
        porcentagem = 100 * questoes_acertadas / questoes_respondidas
        porcentagem = float("%.1f" % porcentagem)
    except ZeroDivisionError:
        porcentagem = 0

    return int(porcentagem)
