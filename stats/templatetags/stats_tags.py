from django import template

from core.templatetags.core_tags import sectodur
from progame.models import StatsAlunoModulo
from quiz.models import Tentativa
from sistema.settings import TEMPO_BADGE_RESPONDE_RAPIDO, TEMPO_BADGE_RESPONDE_LENTO, PORCENTAGEM_BADGE_ERRA_MUITO, \
    PORCENTAGEM_BADGE_ACERTA_MUITO

register = template.Library()


@register.filter
def get_questoes_respondidas_no_modulo(aluno, modulo):
    questoes_modulo = modulo.questoes.all()
    questoes_respondidas = 0

    for tentativa in Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo):
        for resposta in tentativa.respostas.all():
            if resposta.questao in questoes_modulo:
                questoes_respondidas += 1

    return questoes_respondidas


@register.filter
def get_qtd_modulos_finalizados(aluno, turma):
    """
    Retorna quantidade de módulos finalizados pelo aluno na turma
    """
    return StatsAlunoModulo.objects.filter(aluno=aluno, modulo__turma=turma, nivel__exact='6').count()


@register.filter
def get_qtd_modulos_em_andamento(aluno, turma):
    """
    Retorna quantidade de módulos em andamento do aluno na turma
    """
    stats = StatsAlunoModulo.objects.filter(aluno=aluno, modulo__turma=turma)

    qtd = 0
    for stat in stats:
        num_tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo=stat.modulo).count()
        if 0 <= int(stat.nivel) < 6 and num_tentativas > 0:
            qtd += 1

    return qtd


@register.filter
def get_qtd_modulos_pendentes(aluno, turma):
    """
    Retorna quantidade de módulos pendentes do aluno na turma
    """
    stats = StatsAlunoModulo.objects.filter(aluno=aluno, modulo__turma=turma)

    qtd = 0
    for stat in stats:
        num_tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo=stat.modulo).count()
        if int(stat.nivel) == 0 and num_tentativas == 0:
            qtd += 1

    return qtd


@register.filter
def get_data_ultima_tentativa_modulo(aluno, modulo):
    """
    Retorna data da última tentativa do aluno no módulo
    """
    try:
        return Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo).latest('data').data
    except Tentativa.DoesNotExist:
        return None


@register.filter
def get_nivel_no_modulo(aluno, modulo):
    """
    Retorna nível do aluno no módulo
    """
    return int(StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo).nivel)


@register.filter
def get_status_no_modulo(aluno, modulo):
    """
    Retorna status do aluno no módulo
    1: Não começou
    2: Em andamento
    3: Finalizou o módulo
    """

    stats_aluno = StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo)
    nivel_aluno = int(stats_aluno.nivel)
    tentativas = stats_aluno.aluno.tentativas.count()

    if nivel_aluno == 0 and tentativas == 0:
        return 1
    elif nivel_aluno < 6 and tentativas > 0:
        return 2
    return 3


@register.filter
def get_tempo_medio_de_resposta_na_turma(aluno, turma):
    """
    Retorna o tempo médio de resposta do aluno na turma
    """
    tentativas_na_turma = Tentativa.objects.filter(aluno=aluno, quiz__modulo__turma=turma)

    duracao_total_de_resposta_turma = 0
    duracao_total_de_resposta_tentativa = 0
    qtd_respostas = 0

    for tentativa in tentativas_na_turma:
        duracao_total_de_resposta_turma += duracao_total_de_resposta_tentativa

        for resposta in tentativa.respostas.all():
            duracao_total_de_resposta_tentativa += resposta.tempo_decorrido.total_seconds()
            qtd_respostas += 1

    try:
        tempo_medio = duracao_total_de_resposta_turma / qtd_respostas
        tempo_medio = float("%.1f" % tempo_medio)
    except ZeroDivisionError:
        tempo_medio = 0

    return tempo_medio


@register.filter
def get_tempo_medio_de_resposta_na_turma_formatado(aluno, turma):
    """
    Retorna o tempo médio de resposta do aluno na turma de forma formatada
    """
    return sectodur(get_tempo_medio_de_resposta_na_turma(aluno, turma))


@register.filter
def responde_rapido(aluno, turma):
    """Verifica se aluno merece o badge RESPONDE RÁPIDO na turma"""

    tempo_medio = get_tempo_medio_de_resposta_na_turma(aluno, turma)

    if 0 < tempo_medio <= TEMPO_BADGE_RESPONDE_RAPIDO:
        return True

    return False


@register.filter
def responde_lento(aluno, turma):
    """Verifica se aluno merece o badge RESPONDE LENTO na turma"""

    if get_tempo_medio_de_resposta_na_turma(aluno, turma) >= TEMPO_BADGE_RESPONDE_LENTO:
        return True

    return False


@register.filter
def get_porcentagem_de_acertos_na_turma(aluno, turma):
    """
    Retorna porcentagem de acertos do aluno na turma
    """
    tentativas_na_turma = Tentativa.objects.filter(aluno=aluno, quiz__modulo__turma=turma)

    qtd_respostas = 0
    qtd_respostas_corretas = 0

    for tentativa in tentativas_na_turma:
        qtd_respostas += tentativa.respostas.count()

        for resposta in tentativa.respostas.all():
            if resposta.acertou:
                qtd_respostas_corretas += 1

    try:
        porcentagem = 100 * qtd_respostas_corretas / qtd_respostas
        porcentagem = float("%.1f" % porcentagem)
    except ZeroDivisionError:
        porcentagem = 0

    return porcentagem


@register.filter
def get_porcentagem_de_erros_na_turma(aluno, turma):
    return 100 - get_porcentagem_de_acertos_na_turma(aluno, turma)


@register.filter
def acerta_muito(aluno, turma):
    """Verifica se aluno merece o badge ACERTA MUITO na turma"""

    if get_porcentagem_de_acertos_na_turma(aluno, turma) >= PORCENTAGEM_BADGE_ACERTA_MUITO:
        return True

    return False


@register.filter
def erra_muito(aluno, turma):
    """Verifica se aluno merece o badge ERRA MUITO na turma"""

    tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo__turma=turma)
    porcentagem_de_erros = get_porcentagem_de_erros_na_turma(aluno, turma)

    if tentativas.count() > 0 and porcentagem_de_erros >= PORCENTAGEM_BADGE_ERRA_MUITO:
        return True

    return False
