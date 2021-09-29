from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.apps import apps
from progame.utils import acertou_tudo
from sistema.settings import CONQUISTA_ACERTAR_TUDO, CONQUISTA_ALCANCAR_NIVEL_6, CONQUISTA_ALCANCAR_100_PONTOS, \
    CONQUISTA_ALCANCAR_500_PONTOS, CONQUISTA_ALCANCAR_1MIL_PONTOS, CONQUISTA_ALCANCAR_2MIL_PONTOS, \
    CONQUISTA_ALCANCAR_5MIL_PONTOS, CONQUISTA_ALCANCAR_10MIL_PONTOS, CONQUISTA_ALCANCAR_20MIL_PONTOS, \
    CONQUISTA_ALCANCAR_50MIL_PONTOS, CONQUISTA_ALCANCAR_100MIL_PONTOS, \
    CONQUISTA_CONCLUIR_3_MODULOS, CONQUISTA_CONCLUIR_10_MODULOS, CONQUISTA_CONCLUIR_20_MODULOS, \
    CONQUISTA_RESPONDE_RAPIDO
from progame.templatetags.progame_tags import get_pontuacao_na_turma, get_qtd_modulos_finalizados_aluno
from stats.templatetags.stats_tags import responde_rapido

ItemConquista = apps.get_model(app_label='progame', model_name='ItemConquista')
Conquista = apps.get_model(app_label='progame', model_name='Conquista')
Resposta = apps.get_model(app_label='progame', model_name='Resposta')
StatsAlunoModulo = apps.get_model(app_label='progame', model_name='StatsAlunoModulo')
Tentativa = apps.get_model(app_label='quiz', model_name='Tentativa')


@receiver(m2m_changed, sender=Tentativa.respostas.through)
def acertar_tudo(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        tentativa = instance
        aluno = tentativa.aluno
        turma = tentativa.quiz.modulo.turma

        try:
            tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ACERTAR_TUDO,
                                                                aluno=aluno, turma=turma)
        except Conquista.DoesNotExist:
            tem_essa_conquista_na_turma = False

        if acertou_tudo(tentativa) and not tem_essa_conquista_na_turma:
            item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ACERTAR_TUDO)
            Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=StatsAlunoModulo)
def alcancar_nivel_6(sender, instance, created, *args, **kwargs):
    stats_aluno_modulo = instance
    aluno = stats_aluno_modulo.aluno
    turma = stats_aluno_modulo.modulo.turma
    nivel = int(stats_aluno_modulo.nivel)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_NIVEL_6,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if nivel == 6 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_NIVEL_6)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


# Conquistas de Pontos ganhos
@receiver(post_save, sender=Resposta)
def alcancar_100_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_100_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 100 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_100_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_500_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_500_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 500 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_500_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_1mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_1MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 1000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_1MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_2mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_2MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 2000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_2MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_5mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_5MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 5000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_5MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_10mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_10MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 10000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_10MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_20mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_20MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 20000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_20MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_50mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_50MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 50000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_50MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=Resposta)
def alcancar_100mil_pontos(sender, instance, created, *args, **kwargs):
    resposta = instance
    aluno = resposta.aluno
    turma = resposta.questao.modulo.turma

    pontuacao = get_pontuacao_na_turma(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_ALCANCAR_100MIL_PONTOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(pontuacao) >= 100000 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_ALCANCAR_100MIL_PONTOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


# Conquistas de Concluir módulos

@receiver(post_save, sender=StatsAlunoModulo)
def concluir_3_modulos(sender, instance, created, *args, **kwargs):
    stats_aluno_modulo = instance
    aluno = stats_aluno_modulo.aluno
    turma = stats_aluno_modulo.modulo.turma
    
    modulos_finalizados = get_qtd_modulos_finalizados_aluno(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_CONCLUIR_3_MODULOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(modulos_finalizados) >= 3 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_CONCLUIR_3_MODULOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=StatsAlunoModulo)
def concluir_10_modulos(sender, instance, created, *args, **kwargs):
    stats_aluno_modulo = instance
    aluno = stats_aluno_modulo.aluno
    turma = stats_aluno_modulo.modulo.turma
    
    modulos_finalizados = get_qtd_modulos_finalizados_aluno(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_CONCLUIR_10_MODULOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(modulos_finalizados) >= 10 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_CONCLUIR_10_MODULOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


@receiver(post_save, sender=StatsAlunoModulo)
def concluir_20_modulos(sender, instance, created, *args, **kwargs):
    stats_aluno_modulo = instance
    aluno = stats_aluno_modulo.aluno
    turma = stats_aluno_modulo.modulo.turma
    
    modulos_finalizados = get_qtd_modulos_finalizados_aluno(aluno, turma)

    try:
        tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_CONCLUIR_20_MODULOS,
                                                            aluno=aluno, turma=turma)
    except Conquista.DoesNotExist:
        tem_essa_conquista_na_turma = False

    if int(modulos_finalizados) >= 20 and not tem_essa_conquista_na_turma:
        item_conquista = ItemConquista.objects.get(slug=CONQUISTA_CONCLUIR_20_MODULOS)
        Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)


# Responder rápido

@receiver(m2m_changed, sender=Tentativa.respostas.through)
def responde_rapido_aluno(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        tentativa = instance
        aluno = tentativa.aluno
        turma = tentativa.quiz.modulo.turma

        try:
            tem_essa_conquista_na_turma = Conquista.objects.get(item_conquista__slug=CONQUISTA_RESPONDE_RAPIDO,
                                                                aluno=aluno, turma=turma)
        except Conquista.DoesNotExist:
            tem_essa_conquista_na_turma = False

        if responde_rapido(aluno, turma) and not tem_essa_conquista_na_turma:
            item_conquista = ItemConquista.objects.get(slug=CONQUISTA_RESPONDE_RAPIDO)
            Conquista.objects.create(item_conquista=item_conquista, aluno=aluno, turma=turma)
