from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView

from ausers.forms import CadastroForm, LoginForm
from ausers.models import Professor, Aluno
from core.messages import *
from django.urls import reverse
from ausers.auth import EmailBackend
from ausers.utils import validate_recaptcha, UnauthenticatedBaseMixin
from sistema.settings import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY, LOGOUT_REDIRECT_URL
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


User = get_user_model()


class LoginView(UnauthenticatedBaseMixin, FormView):
    template_name = 'ausers/login_form_view.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['recaptcha_site_key'] = RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        if not validate_recaptcha(self.request, RECAPTCHA_SECRET_KEY):
            form.add_error(None, _('Falha ao verificar reCaptcha, por favor tente novamente'))
            return super(LoginView, self).form_invalid(form)

        next = self.request.GET.get('next', None)
        cleaned_data = form.cleaned_data
        user = EmailBackend.authenticate(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
        login(self.request, user)

        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('progame:get_dashboard'))


class CadastroView(UnauthenticatedBaseMixin, FormView):
    template_name = 'ausers/cadastro_form_view.html'
    form_class = CadastroForm

    def get_context_data(self, **kwargs):
        context = super(CadastroView, self).get_context_data(**kwargs)
        context['recaptcha_site_key'] = RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        if not validate_recaptcha(self.request, RECAPTCHA_SECRET_KEY):
            form.add_error(None, _('Falha ao verificar reCaptcha, por favor tente novamente'))
            return super(CadastroView, self).form_invalid(form)

        cleaned_data = form.cleaned_data

        new_user = User(email=cleaned_data['email'])
        new_user.set_password(cleaned_data['password'])
        new_user.is_staff = True
        new_user.save()

        user = EmailBackend.authenticate(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
        login(self.request, user)

        return HttpResponseRedirect(reverse('progame:get_dashboard'))


class LogoutView(RedirectView):
    url = LOGOUT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class CadastroProfessor(UnauthenticatedBaseMixin, FormView):
    template_name = 'ausers/cadastro_professor_form_view.html'
    form_class = CadastroForm

    def get_context_data(self, **kwargs):
        context = super(CadastroProfessor, self).get_context_data(**kwargs)
        context['recaptcha_site_key'] = RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        if not validate_recaptcha(self.request, RECAPTCHA_SECRET_KEY):
            form.add_error(None, _('Falha ao verificar reCaptcha, por favor tente novamente'))
            return super(CadastroProfessor, self).form_invalid(form)

        new_user = User(email=form.cleaned_data['email'])
        new_user.set_password(form.cleaned_data['password'])
        new_user.is_staff = True
        new_user.save()

        Professor.objects.create(user=new_user)

        user = EmailBackend.authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('progame:professor_dashboard'))

        return HttpResponseRedirect(reverse('ausers:professor_cadastro'))


class CadastroAluno(UnauthenticatedBaseMixin, FormView):
    template_name = 'ausers/cadastro_aluno_form_view.html'
    form_class = CadastroForm

    def get_context_data(self, **kwargs):
        context = super(CadastroAluno, self).get_context_data(**kwargs)
        context['recaptcha_site_key'] = RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        if not validate_recaptcha(self.request, RECAPTCHA_SECRET_KEY):
            form.add_error(None, _('Falha ao verificar reCaptcha, por favor tente novamente'))
            return super(CadastroAluno, self).form_invalid(form)

        new_user = User(email=form.cleaned_data['email'])
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()

        Aluno.objects.create(user=new_user)

        user = EmailBackend.authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('progame:get_dashboard'))

        return HttpResponseRedirect(reverse('ausers:aluno_cadastro'))

