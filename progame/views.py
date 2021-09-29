from datetime import datetime
import json

import requests
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import DataError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from extra_views import UpdateWithInlinesView, InlineFormSetFactory
from django.contrib.auth import get_user_model

from ausers.forms import ProfessorForm, UserUpdateForm, AlunoForm, LoginForm, CadastroForm
from ausers.models import Professor, Aluno
from ausers.utils import AlunoMixin, ProfessorMixin, AuthBaseMixin, get_next_url, UnauthenticatedBaseMixin
from core.messages import *
from core.utils import generate_random_string
from ausers.templatetags.ausers_tags import check_professor, check_aluno
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DetailView, ListView, DeleteView

from progame.filters import ImportarQuestoesFilter
from progame.forms import ParticiparTurmaForm, TurmaForm, ModuloForm, QuestaoForm, ModuloModalForm
from progame.models import Turma, Questao, Modulo, Alternativa, StatsAlunoModulo, Verbo
from quiz.forms import LinkAjudaForm
from quiz.models import Quiz, LinkAjuda
from sistema.settings import RECAPTCHA_SITE_KEY, STATIC_URL

User = get_user_model()


# Forum - Em breve
class ForumTemplateView(AuthBaseMixin, TemplateView):
    template_name = 'progame/forum/index-forum.html'

    def get_context_data(self, **kwargs):
        context = super(ForumTemplateView, self).get_context_data(**kwargs)
        context['turma'] = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        context['active'] = ['forum']
        return context


# Central de ajuda
def ajuda(request):
    return render(request, 'progame/ajuda/index.html')


def primeiros_passos(request):
    return render(request, 'progame/ajuda/primeiros_passos.html')


def turmas_e_alunos(request):
    return render(request, 'progame/ajuda/turmas_e_alunos.html')


def modulos(request):
    return render(request, 'progame/ajuda/modulos.html')


def quizzes(request):
    return render(request, 'progame/ajuda/quizzes.html')


def rankings(request):
    return render(request, 'progame/ajuda/rankings.html')


def estatisticas(request):
    return render(request, 'progame/ajuda/estatisticas.html')


class PublicIndexTemplateView(UnauthenticatedBaseMixin, TemplateView):
    template_name = 'progame/public/index.html'

    def get_context_data(self, **kwargs):
        context = super(PublicIndexTemplateView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm(self.request.POST or None)
        context['signup_form'] = CadastroForm(self.request.POST or None)
        context['recaptcha_site_key'] = RECAPTCHA_SITE_KEY

        return context


class EscolherTipoConta(AuthBaseMixin, View):
    def test_func(self):
        req = self.request
        return req.user.is_authenticated and not (req.user.is_professor() or req.user.is_aluno())

    def get(self, request, *args, **kwargs):
        return render(request, 'progame/escolher_tipo_conta.html')

    def post(self, request, *args, **kwargs):
        try:
            data = request.user.socialaccount_set.filter(provider='google')[0].extra_data
            image_url = data.get('picture', None)

            r = requests.get(image_url)

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
            img_name = str(datetime.now()) + str(img_temp) + '.jpg'
        except IndexError:
            img_temp, img_name = None, None

        if 'aluno' in request.POST:
            aluno = Aluno(user=request.user)
            aluno.save()
            if img_temp:
                aluno.imagem.save(img_name, File(img_temp), save=True)
            message_success_custom(self.request, 'Bem vindo(a) ao ProGame!')

        elif 'professor' in request.POST:
            professor = Professor(user=request.user)
            professor.save()
            user = User.objects.get(pk=self.request.user.pk)
            user.is_staff = True
            user.save()
            if img_temp:
                professor.imagem.save(img_name, File(img_temp), save=True)
            message_success_custom(self.request, 'Bem vindo(a) ao ProGame!')

        return get_next_url(self.request)


@login_required
def get_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_professor():
            return HttpResponseRedirect(reverse('progame:professor_dashboard'))
        elif request.user.is_aluno():
            return HttpResponseRedirect(reverse('progame:aluno_dashboard'))

    return HttpResponseRedirect(reverse('ausers:login'))


class AlunoDashboard(AlunoMixin, TemplateView):
    template_name = 'progame/aluno/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AlunoDashboard, self).get_context_data(**kwargs)
        context['turmas'] = self.request.user.aluno.turma_set.order_by('-pk')[:6]
        context['participar_turma_form'] = ParticiparTurmaForm
        return context


class ProfessorDashboard(ProfessorMixin, TemplateView):
    template_name = 'progame/professor/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ProfessorDashboard, self).get_context_data(**kwargs)
        context['turmas'] = Turma.objects.filter(professor=self.request.user.professor).order_by('-atualizado_em')[:6]
        return context


class AlunoParticiparTurma(AlunoMixin, FormView):
    form_class = ParticiparTurmaForm

    def form_valid(self, form):
        codigo = form.cleaned_data.get('codigo', None)
        try:
            turma = Turma.objects.get(codigo=codigo)

            if turma.alunos.filter(pk=self.request.user.aluno.pk).exists():
                return JsonResponse({'message': 'Você já faz parte dessa turma'}, status=400)

            turma.alunos.add(self.request.user.aluno)
        except Turma.DoesNotExist:
            turma = None

        if turma:
            for modulo in turma.modulos.all():
                StatsAlunoModulo.objects.get_or_create(aluno=self.request.user.aluno, modulo=modulo)
            message_success_custom(self.request, 'Agora você faz parte dessa turma')
            return JsonResponse({'url': reverse('progame:turma_detail_view', kwargs={'uuid': turma.uuid})}, status=200)

        return JsonResponse({'message': 'Código inválido'}, status=404)


@login_required
def get_perfil_update(request):
    if request.user.is_authenticated:
        if request.user.is_professor():
            return HttpResponseRedirect(reverse('progame:professor_update_view'))
        elif request.user.is_aluno():
            return HttpResponseRedirect(reverse('progame:aluno_update_view'))

    return HttpResponseRedirect(reverse('ausers:login'))


class ProfessorInline(InlineFormSetFactory):
    model = Professor
    form_class = ProfessorForm
    factory_kwargs = {'can_delete': False}


class ProfessorUpdateView(ProfessorMixin, UpdateWithInlinesView):
    template_name = 'progame/professor/professor_update_view.html'
    model = User
    login_url = reverse_lazy('ausers:login')
    inlines = [ProfessorInline]
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        message_success_custom(self.request, 'Perfil atualizado')
        return reverse('progame:professor_update_view')


class AlunoPerfilDetailView(AuthBaseMixin, DetailView):
    model = Aluno
    template_name = 'progame/perfis/aluno_perfil.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Aluno, uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conquistas = []
        for conquista in self.object.conquistas.all():
            c = {
                'nome': conquista.item_conquista.nome,
                'descricao': conquista.item_conquista.descricao2,
                'imagem': f'{STATIC_URL}progame/img/badges/{conquista.item_conquista.slug}.png',
                'quantidade': 1
            }

            if c in conquistas:
                i = conquistas.index(c)
                conquistas[i]['quantidade'] += 1
            else:
                conquistas.append(c)

        context['conquistas'] = conquistas
        return context


class AlunoInline(InlineFormSetFactory):
    model = Aluno
    form_class = AlunoForm
    factory_kwargs = {'can_delete': False}


class AlunoUpdateView(AlunoMixin, UpdateWithInlinesView):
    template_name = 'progame/aluno/aluno_update_view.html'
    model = User
    login_url = reverse_lazy('ausers:login')
    inlines = [AlunoInline]
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        message_success_custom(self.request, 'Perfil atualizado')
        return reverse('progame:aluno_update_view')


class TurmaDetailView(AuthBaseMixin, DetailView):
    template_name = 'progame/turma/turma_detail_view.html'
    model = Turma

    def get_object(self, queryset=None):
        return get_object_or_404(Turma, uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(TurmaDetailView, self).get_context_data(**kwargs)
        context['active'] = ['turma']

        links_de_ajuda = []
        for modulo in self.object.modulos.all():
            for quiz in modulo.quizzes.all():
                [links_de_ajuda.append(link) for link in quiz.links_ajuda.all() if link.is_new]

        context['links_de_ajuda'] = links_de_ajuda
        return context

    def test_func(self):
        return check_professor(self.get_object(), self.request) or check_aluno(self.get_object(), self.request)


class TurmaCreateView(ProfessorMixin, BSModalCreateView):
    template_name = 'progame/turma/modal/turma_create_modal.html'
    form_class = TurmaForm

    def form_valid(self, form):
        turma = form.save(commit=False)
        turma.professor = self.request.user.professor

        turma_exists = True
        while turma_exists:
            codigo = generate_random_string()
            try:
                Turma.objects.get(codigo=codigo)
            except Turma.DoesNotExist:
                turma_exists = False

        turma.codigo = codigo
        turma.save()

        if turma.pk:
            message_success_custom(self.request, 'Sua turma foi criada')
            return HttpResponseRedirect(reverse('progame:turma_detail_view', kwargs={'uuid': turma.uuid}))

        message_error_custom(self.request, 'Houve um erro ao criar turma. Tente novamente mais tarde')
        return HttpResponseRedirect(reverse('progame:get_dashboard'))


class TurmaDeleteView(ProfessorMixin, DeleteView):
    model = Turma

    def test_func(self):
        return check_professor(self.get_object(), self.request)

    def get_object(self, queryset=None):
        return get_object_or_404(Turma, uuid=self.kwargs['uuid'])

    def get_success_url(self):
        message_deleted_custom(self.request, "Turma excluída")
        return reverse('progame:professor_dashboard')


# class TurmaFinalizarCadastro(ProfessorMixin, CreateView):
#     template_name = 'progame/turma/finalizar_cadastro.html'
#     model = Modulo
#     form_class = ModuloForm
#
#     def test_func(self):
#         turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
#         return check_professor(turma, self.request)
#
#     def form_valid(self, form):
#         modulo = form.save(commit=False)
#         modulo.turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
#         modulo.save()
#
#         if modulo:
#             message_success_custom(self.request, 'Sua turma foi criada')
#
#         return super(TurmaFinalizarCadastro, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('progame:turma_detail_view', kwargs={'uuid': self.object.turma.uuid})


# class PularCadastroModulo(ProfessorMixin, View):
#     def test_func(self):
#         turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
#         return check_professor(turma, self.request)
#
#     def get(self, request, uuid):
#         message_success_custom(request, 'Sua turma foi criada')
#         data = {
#             'redirect_url': reverse('progame:turma_detail_view', kwargs={'uuid': self.kwargs['uuid']})
#         }
#         return JsonResponse(data)


class TurmaUpdateView(ProfessorMixin, BSModalUpdateView):
    template_name = 'progame/turma/modal/turma_update_modal.html'
    form_class = TurmaForm
    model = Turma

    def get_object(self, queryset=None):
        return get_object_or_404(Turma, uuid=self.kwargs['uuid'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['turma'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        message_success_custom(self.request, 'Turma atualizada')
        return super(TurmaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class AlunoModuloDetailView(AlunoMixin, DetailView):
    template_name = 'progame/modulo/aluno/aluno_modulo_detail_view.html'
    model = Modulo

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AlunoModuloDetailView, self).get_context_data(**kwargs)

        context['active'] = ['quiz']
        context['turma'] = self.object.turma
        questoes = Questao.objects.filter(quizzes__modulo=self.object)

        # separa questões por nível
        questoes_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for questao in questoes:
            questoes_dict[int(questao.nivel)].append(questao)

        context['questoes_dict'] = questoes_dict

        return context


class ModuloDetailView(AuthBaseMixin, DetailView):
    template_name = 'progame/modulo/modulo_detail_view.html'
    model = Modulo

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])

    def test_func(self):
        turma = self.get_object().turma
        return check_professor(turma, self.request) or check_aluno(turma, self.request)

    def get_context_data(self, **kwargs):
        context = super(ModuloDetailView, self).get_context_data(**kwargs)
        context['active'] = ['info']
        context['turma'] = self.object.turma
        return context


class ModuloUpdateView(ProfessorMixin, UpdateView):
    template_name = 'progame/modulo/modulo_update_view.html'
    model = Modulo
    form_class = ModuloForm

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])

    def test_func(self):
        return check_professor(self.get_object().turma, self.request)

    def get_context_data(self, **kwargs):
        context = super(ModuloUpdateView, self).get_context_data(**kwargs)
        context['active'] = ['info']
        context['turma'] = self.object.turma
        return context

    def get_success_url(self):
        return reverse('progame:modulo_detail_view', kwargs={'uuid': self.object.uuid})

    def form_valid(self, form):
        message_success_custom(self.request, 'Módulo atualizado')
        return super(ModuloUpdateView, self).form_valid(form)


class ModuloCreateView(ProfessorMixin, BSModalCreateView):
    template_name = 'progame/modulo/modulo_create_modal.html'
    model = Modulo
    form_class = ModuloModalForm

    def test_func(self):
        turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        return check_professor(turma, self.request)

    def form_valid(self, form):
        modulo = form.save(commit=False)
        modulo.turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        message_success_custom(self.request, "Módulo adicionado")
        return super(ModuloCreateView, self).form_valid(form)

    def get_success_url(self):
        # return reverse('progame:turma_detail_view', kwargs={'uuid': self.object.turma.uuid})
        return self.request.META.get('HTTP_REFERER')


class ModuloDeleteView(ProfessorMixin, DeleteView):
    model = Modulo

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])

    def test_func(self):
        return check_professor(self.get_object().turma, self.request)

    def get_success_url(self):
        message_deleted_custom(self.request, "Módulo excluído")
        return reverse('progame:turma_detail_view', kwargs={'uuid': self.object.turma.uuid})


class PularCadastroQuestao(ProfessorMixin, View):
    def test_func(self):
        turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        return check_professor(turma, self.request)

    def post(self, request, *args, **kwargs):
        turma = get_object_or_404(Turma, uuid=self.kwargs['uuid'])
        nome_modulo = request.POST.get('nome_modulo', None)
        descricao_modulo = request.POST.get('descricao_modulo', None)

        if not nome_modulo or nome_modulo.isspace():
            return JsonResponse({'message': 'form_invalid'}, status=400)

        modulo = Modulo.objects.create(turma=turma, nome=nome_modulo, descricao=descricao_modulo)
        if modulo.pk:
            message_success_custom(request, 'Módulo criado')

        data = {
            'redirect_url': reverse('progame:turma_detail_view', kwargs={'uuid': self.kwargs['uuid']})
        }
        return JsonResponse(data)


class ToggleBloqueioQuiz(ProfessorMixin, View):
    def test_func(self):
        modulo = get_object_or_404(Modulo, pk=self.request.POST.get('modulo'))
        return check_professor(modulo.turma, self.request)

    def post(self, request, *args, **kwargs):
        modulo_id = request.POST.get('modulo')
        nivel = request.POST.get('nivel')

        try:
            quiz = Quiz.objects.get(modulo_id=modulo_id, nivel=nivel)
        except Quiz.DoesNotExist:
            quiz = Quiz.objects.create(modulo_id=modulo_id, nivel=nivel)

        quiz.bloqueado = not quiz.bloqueado
        quiz.save()

        return JsonResponse({'bloqueado': quiz.bloqueado})


class QuestaoListView(ProfessorMixin, ListView):
    template_name = 'progame/questao/questao_list_view.html'
    model = Modulo

    def test_func(self):
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        return check_professor(modulo.turma, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuestaoListView, self).get_context_data(**kwargs)
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        context['active'] = ['questoes']
        context['object'] = modulo
        context['turma'] = modulo.turma
        context['link_estudo_form'] = LinkAjudaForm

        questoes = Questao.objects.filter(modulo__uuid=self.kwargs['uuid'])

        # separando questões por nível
        questoes_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for questao in questoes:
            questoes_dict[int(questao.nivel)].append(questao)

        context['questoes_dict'] = questoes_dict

        return context


class QuestaoCreateView(ProfessorMixin, CreateView):
    template_name = 'progame/questao/questao_create_view.html'
    model = Questao
    form_class = QuestaoForm

    def test_func(self):
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        return check_professor(modulo.turma, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuestaoCreateView, self).get_context_data(**kwargs)
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        context['modulo'] = modulo
        context['turma'] = modulo.turma
        context['nivel'] = self.kwargs['nivel']
        return context

    def form_valid(self, form):
        req = self.request.POST

        if not req.get('sentenca') or not req.get('tempo_para_responder'):
            return JsonResponse({'message': 'Preencha todos os campos obrigatórios'}, status=400)

        quiz = Quiz.objects.get(modulo__uuid=req.get('modulo_uuid'), nivel=self.kwargs['nivel'])
        questao = Questao(
            verbo_id=req.get('verbo'), sentenca=req.get('sentenca'), descricao=req.get('descricao', None),
            nivel=self.kwargs['nivel'], modulo=quiz.modulo,
            tempo_para_responder=form.cleaned_data['tempo_para_responder']
        )
        questao.save()
        quiz.questoes.add(questao)

        alternativas = req.getlist('alternativas[]', [])
        alternativas_json = [json.loads(item) for item in alternativas]

        if alternativas_json:
            try:
                Alternativa.objects.bulk_create(
                    [Alternativa(nome=a['nome'], questao=questao, is_correta=a['correta']) for a in alternativas_json]
                )
            except DataError:
                redirect_url = reverse('progame:questao_create_view', kwargs={'uuid': req.get('modulo_uuid')})
                return JsonResponse(
                    {
                        'message': 'Uma alternativa deve conter no máximo 700 caracteres',
                        'redirect_url': redirect_url
                    },
                    status=400
                )

        message_success_custom(self.request, 'Questão cadastrada')

        # if req.get('continuar'):
        #     redirect_url = reverse('progame:questao_create_view', kwargs={'uuid': req.get('modulo_uuid'),
        #                                                                   'nivel': req.get('nivel')})
        #     return JsonResponse({'redirect_url': redirect_url})

        params = '?n=' + str(questao.nivel) + '&q=' + str(questao.pk)
        redirect_url = reverse('progame:questao_list_view', kwargs={'uuid': req.get('modulo_uuid')}) + params
        return JsonResponse({'redirect_url': redirect_url})


class QuestaoUpdateView(ProfessorMixin, UpdateView):
    template_name = 'progame/questao/questao_update_view.html'
    model = Questao
    form_class = QuestaoForm

    def get_object(self, queryset=None):
        return get_object_or_404(Questao, uuid=self.kwargs['uuid'])

    def test_func(self):
        questao = get_object_or_404(Questao, uuid=self.kwargs['uuid'])
        return check_professor(questao.modulo.turma, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turma'] = self.get_object().modulo.turma
        return context

    def form_valid(self, form):
        req = self.request.POST

        if not req.get('sentenca') or not req.get('tempo_para_responder'):
            return JsonResponse({'message': 'Preencha todos os campos obrigatórios'}, status=400)

        questao = Questao.objects.get(uuid=self.get_object().uuid)
        questao.verbo = get_object_or_404(Verbo, pk=req.get('verbo'))
        questao.sentenca = req.get('sentenca')
        questao.descricao = req.get('descricao', None)
        questao.tempo_para_responder = form.cleaned_data['tempo_para_responder']
        questao.save()

        alternativas = req.getlist('alternativas[]', [])
        alternativas_json = [json.loads(item) for item in alternativas]

        alternativas_to_remove = []
        for a in alternativas_json:
            if a['pk']:
                alternativas_to_remove.append(a['pk'])

        # remove do banco alternativas que foram removidas da questão
        self.get_object().alternativas.all().exclude(id__in=alternativas_to_remove).delete()

        for a in alternativas_json:
            # se a alternativa possuir pk, ela existe no banco e será atualizada
            if a['pk']:
                alternativa = Alternativa.objects.get(pk=a['pk'])
                alternativa.nome = a['nome']
                alternativa.is_correta = a['correta']
                alternativa.save()

            # caso contrário, uma nova alternativa será criada para essa questão
            elif not a['pk']:
                nova_alternativa = Alternativa(nome=a['nome'], is_correta=a['correta'], questao=questao)
                nova_alternativa.save()

        message_success_custom(self.request, 'Questão atualizada')

        # if req.get('continuar'):
        #     redirect_url = reverse('progame:questao_update_view', kwargs={'pk': self.get_object().pk})
        #     return JsonResponse({'redirect_url': redirect_url})

        params = '?n=' + str(questao.nivel) + '&q=' + str(questao.pk)
        redirect_url = reverse('progame:questao_list_view', kwargs={'uuid': self.get_object().modulo.uuid}) + \
                       params
        return JsonResponse({'redirect_url': redirect_url})


class ImportarQuestoesListView(ProfessorMixin, ListView):
    model = Questao
    template_name = 'progame/importar_questoes/importar_questoes_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
        context['filter'] = ImportarQuestoesFilter(self.request.GET)
        context['modulo'] = modulo
        context['turma'] = modulo.turma
        context['nivel'] = self.kwargs['nivel']
        return context

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, nivel=str(self.kwargs['nivel']), modulo__uuid=self.kwargs['uuid'])
        # quiz = Quiz.objects.get(nivel=str(self.kwargs['nivel']), modulo__uuid=self.kwargs['uuid'])
        qs = super().get_queryset().filter(nivel=self.kwargs['nivel'])\
            .exclude(sentenca__in=[questao.sentenca for questao in quiz.questoes.all()])

        sentencas_unicas = set()
        questoes_repetidas = []
        for questao in qs:
            if questao.sentenca not in sentencas_unicas:
                sentencas_unicas.add(questao.sentenca)
            else:
                questoes_repetidas.append(questao.pk)

        qs = qs.exclude(pk__in=questoes_repetidas).exclude(modulo__turma__professor=self.request.user.professor,
                                                           modulo__uuid=self.kwargs['uuid'])

        # todo: Remover questões exatamente duplicadas

        filter = ImportarQuestoesFilter(self.request.GET, qs)
        return filter.qs


class ImportarQuestoesView(ProfessorMixin, View):

    def post(self, request, *args, **kwargs):
        questoes_pk = request.POST.get('questoes')
        questoes_pk = json.loads(questoes_pk)
        nivel = self.kwargs['nivel']
        questoes = Questao.objects.filter(pk__in=questoes_pk)

        if all(int(questao.nivel) == nivel for questao in questoes):
            modulo = get_object_or_404(Modulo, uuid=self.kwargs['uuid'])
            for questao in questoes:
                alternativas = questao.alternativas.all()
                nova_questao = Questao.objects.create(sentenca=questao.sentenca, descricao=questao.descricao,
                                                      nivel=nivel, professor=self.request.user.professor, modulo=modulo,
                                                      verbo=questao.verbo)
                novas_alternativas = []
                for a in alternativas:
                    novas_alternativas.append(
                        Alternativa.objects.create(nome=a.nome, questao=nova_questao, is_correta=a.is_correta)
                    )
                nova_questao.alternativas.add(*novas_alternativas)
                quiz = Quiz.objects.get(modulo=modulo, nivel=nivel)
                quiz.questoes.add(nova_questao)
                quiz.save()

            qtd_questoes_importadas = questoes.count()

            redirect_url = reverse('progame:questao_list_view', kwargs={'uuid': self.kwargs['uuid']}) + f"?n={nivel}"

            if qtd_questoes_importadas == 1:
                message_success_custom(request, f"1 questão importada para o nível {nivel}")
            else:
                message_success_custom(request,
                                       f"{qtd_questoes_importadas} questões importadas para o nível {nivel}")

            return JsonResponse({'redirect_url': redirect_url})

        return JsonResponse({"message": f"As questões não correspondem ao nível {nivel}"}, status=400)


class ModuloRankingDetailView(AuthBaseMixin, DetailView):
    template_name = 'progame/modulo/modulo_ranking_detail_view.html'
    model = Modulo

    def get_object(self, queryset=None):
        return get_object_or_404(Modulo, uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(ModuloRankingDetailView, self).get_context_data(**kwargs)
        context['active'] = ['ranking']
        context['turma'] = self.object.turma
        return context
