from django import template

from progame.models import Turma, Modulo

register = template.Library()


@register.filter
def check_professor(turma, request):
    """
    Verifica se o usuário está logado, se é um professor
    e se ele é o dono ta turma
    """
    return request.user.is_authenticated and request.user.is_professor() and request.user.professor == turma.professor


@register.filter
def check_professor_with_uuid(uuid, request):
    """
    Verifica se o usuário é o dono ta turma
    Caso seja, retorna o uuid da turma
    Caso contrário, retorna false
    """

    if uuid:
        try:
            turma = Turma.objects.get(uuid=uuid)
        except Turma.DoesNotExist:
            try:
                turma = Modulo.objects.get(uuid=uuid).turma
            except Modulo.DoesNotExist:
                turma = None

        if turma and request.user.professor == turma.professor:
            return turma.uuid

    return False


@register.filter
def check_aluno(turma, request):
    """
    Verifica se o usuário está logado, se é um aluno
    e se ele faz parte da turma
    """
    return request.user.is_authenticated and request.user.is_aluno() and turma.alunos.filter(
        pk=request.user.aluno.pk).exists()
