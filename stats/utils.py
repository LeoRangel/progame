from django.utils.text import Truncator

from progame.models import StatsAlunoModulo, Questao
from quiz.models import Tentativa
from sistema.settings import QTD_ERROS_ALUNO_COM_DIFICULDADE


def get_questoes_com_dificuldade(aluno, modulo, quizzes_concluidos=False):
    tentativas = Tentativa.objects.filter(aluno=aluno, quiz__modulo=modulo)
    stats_no_modulo = StatsAlunoModulo.objects.get(aluno=aluno, modulo=modulo)
    nivel_no_modulo = int(stats_no_modulo.nivel)

    if quizzes_concluidos:
        # mostra apenas tentativas de quizzes já concluídos
        niveis_concluidos = []

        for nivel in range(1, nivel_no_modulo + 1):
            niveis_concluidos.append(str(nivel))

        tentativas = tentativas.filter(quiz__nivel__in=niveis_concluidos)
    else:
        # mostra apenas tentativas do quiz atual
        tentativas = tentativas.filter(quiz__nivel=str(nivel_no_modulo + 1))

    erros = []
    for tentativa in tentativas:
        [erros.append(r.questao.pk) for r in tentativa.respostas.all() if not r.acertou]

    questoes_com_erros = {}
    for questao_pk in erros:
        questao_obj = Questao.objects.get(pk=questao_pk)

        if questao_pk not in questoes_com_erros:
            dados = {
                'sentenca': questao_obj.sentenca,
                'sentencaTruncated': Truncator(questao_obj.sentenca).words(8),
                'nivel': questao_obj.nivel,
                'qtdErros': 1
            }
            questoes_com_erros.update({questao_pk: dados})
        else:
            qtd_erros = questoes_com_erros[questao_pk]['qtdErros']
            questoes_com_erros[questao_pk]['qtdErros'] = qtd_erros + 1

    questoes_com_dificuldade = []
    [questoes_com_dificuldade.append(dados) for pk, dados in questoes_com_erros.items() if dados['qtdErros'] >=
     QTD_ERROS_ALUNO_COM_DIFICULDADE]

    return questoes_com_dificuldade


def get_tentativas_por_aluno(quiz):
    pass


def get_porcentagem_de_selecao(alternativa, tentativas):
    qtd_selecao = 0
    qtd_tentativas = 0
    for tentativa in tentativas:
        for resposta in tentativa.respostas.all():
            if resposta.alternativa == alternativa:
                qtd_selecao += 1

        for questao in tentativa.quiz.questoes.all():
            if alternativa in questao.alternativas.all():
                qtd_tentativas += 1

    try:
        porcentagem = 100 * qtd_selecao / tentativas.count()
    except ZeroDivisionError:
        porcentagem = 0
    # porcentagem = 100 * qtd_selecao / qtd_tentativas
    return '%.1f' % porcentagem


def get_historico_de_respostas(quiz):
    questoes = quiz.questoes.all()

    historico_de_respostas = {}

    if quiz.tentativas.count() == 0:
        return historico_de_respostas

    for questao in questoes:
        alternativas = []
        for a in questao.alternativas.all():
            alternativas.append({
                'alternativa': a.nome,
                'alternativaTruncated': Truncator(a.nome).words(7),
                'questao': a.questao.sentenca,
                'questaoTruncated': Truncator(a.questao.sentenca).words(12),
                'isCorreta': a.is_correta,
                'quantosSelecionaram': get_porcentagem_de_selecao(a, quiz.tentativas.all())
            })

        historico_de_respostas.update({questao.sentenca: alternativas})

    return historico_de_respostas
