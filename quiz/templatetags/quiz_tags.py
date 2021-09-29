from django import template
from quiz.models import Quiz

register = template.Library()


@register.filter
def get_quiz(modulo, nivel):
    """
    Retorna o quiz passando módulo e nível
    """
    return Quiz.objects.get(nivel=nivel, modulo_id=modulo)
