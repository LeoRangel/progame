import requests
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.messages import display_conquista_message
from progame.models import Conquista, Turma, Modulo


def get_next_url(request):
    """
    :param request:
    :return: Url que o usuário tenha permissão de acessar
    """
    if request.user.is_authenticated and not (request.user.is_professor() or request.user.is_aluno()):
        # retornar para url de escolher se é aluno ou professor
        return HttpResponseRedirect(reverse('progame:escolher_tipo_conta'))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('progame:get_dashboard'))
    else:
        next = request.path
        return HttpResponseRedirect(reverse('ausers:login') + '?next=' + next)


class AuthBaseMixin(UserPassesTestMixin, LoginRequiredMixin):
    """
    Mixin para usuários autenticados
    """
    def test_func(self):
        return self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        """
        Mostra novas conquistas caso aluno esteja em uma página da turma
        """
        uuid = kwargs.get('uuid', None)
        if request.user.is_aluno() and uuid:
            try:
                turma = Turma.objects.get(uuid=uuid)
            except Turma.DoesNotExist:
                try:
                    turma = Modulo.objects.get(uuid=uuid).turma
                except Modulo.DoesNotExist:
                    turma = None

            if turma:
                novas_conquistas = Conquista.objects.filter(aluno=request.user.aluno, turma=turma, visualizado=False)
                for conquista in novas_conquistas:
                    display_conquista_message(request, conquista.pk)
                    conquista.visualizado = True
                    conquista.save()

        return super(AuthBaseMixin, self).dispatch(request, *args, **kwargs)

    def get_login_url(self):
        return reverse('ausers:login')

    def handle_no_permission(self):
        return get_next_url(self.request)


class UnauthenticatedBaseMixin(UserPassesTestMixin):
    """
    Mixin para usuários NÃO autenticados
    """
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return get_next_url(self.request)


class AlunoMixin(AuthBaseMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_aluno()


class ProfessorMixin(AuthBaseMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_professor()


def validate_recaptcha(request, secret_key):
    """
    Valida reCaptcha através do token passado pela requisição e chave da API
    """
    data = {
        'response': request.POST.get('g-recaptcha-response'),
        'secret': secret_key
    }

    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()

    if not result_json.get('success'):
        return False

    return True
