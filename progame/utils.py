# from progame.models import Alternativa
from datetime import datetime, date, timedelta
from django.apps import apps


def get_diff_between_two_times(time1, time2):
    """
    :param time1: Hora inicial (datetime.time)
    :param time2: Hora final (datetime.time)
    :return: Diferença entre dois datetime.time
    """
    return datetime.combine(date.min, time2) - datetime.combine(date.min, time1)


def get_quiz_duration_time(respostas):
    """
    Recebe respostas do quiz e retorna duração do quiz
    :param respostas: Respostas de um aluno em um quiz
    :return: Tempo de duração da tentativa do aluno
    """
    total_segundos = 0
    for r in respostas:
        segundos_resposta = get_diff_between_two_times(r.hora_inicio, r.hora_fim).total_seconds()
        total_segundos += segundos_resposta

    return timedelta(seconds=total_segundos)


def get_questoes_corretas(respostas_quiz):
    Alternativa = apps.get_model(app_label='progame', model_name='Alternativa')
    respostas_corretas = Alternativa.objects.filter(id__in=[a['alternativa'] for a in respostas_quiz], is_correta=True)
    return respostas_corretas


def acertou_tudo(tentativa):
    """
    Retorna True caso todas as respostas da tentativa estejam corretas
    False caso contrário
    """
    if all(resposta.acertou for resposta in tentativa.respostas.all()):
        return True

    return False


def get_tempo_medio_por_questao(respostas):
    """
    Recebe respostas do quiz e retorna a duração média por questão
    :param respostas: Respostas de um aluno em um quiz
    :return: Duração média por questão no quiz (em segundos)
    """
    duracoes = [str(get_diff_between_two_times(r.hora_inicio, r.hora_fim)).split('.', 1)[0] for r in
                respostas]

    tempo_medio = timedelta(seconds=sum(map(lambda f: int(f[0]) * 3600 + int(f[1]) * 60 + int(f[2]),
                                            map(lambda f: f.split(':'), duracoes))) / len(duracoes))

    tempo_medio_sec = "%.1f" % tempo_medio.total_seconds()

    return tempo_medio_sec


def get_pontuacao_tempo_resposta(tempo_decorrido, tempo_max_para_responder, pontuacao_total_questao):
    """
    Para calcular a pontuação por tempo, é utilizada a equação: [1-(r/q/2)]p,
    onde r é o tempo (em segundos) após a questão iniciar, q é o tempo (em segundos)
    total para responder a questão, e p é o número de pontos que você ganha
    por responder a questão corretamente
    """

    pontuacao = (1 - (tempo_decorrido / tempo_max_para_responder / 2)) * pontuacao_total_questao
    return int(pontuacao)
