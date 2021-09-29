from ausers.templatetags.ausers_tags import check_aluno
from progame.templatetags.progame_tags import get_nivel_no_modulo


def pode_acessar_pagina_do_quiz(request, quiz):
    nivel_no_modulo = get_nivel_no_modulo(request.user.aluno, quiz.modulo)
    aluno_eh_da_turma = check_aluno(quiz.modulo.turma, request)

    if aluno_eh_da_turma and int(nivel_no_modulo) + 1 >= int(quiz.nivel) and not quiz.bloqueado:
        return True

    return False
