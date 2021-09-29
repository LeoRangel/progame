from django import forms
from django.shortcuts import get_object_or_404

from core.middleware import RequestMiddleware
from progame.models import *
from bootstrap_modal_forms.forms import BSModalForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ParticiparTurmaForm(forms.Form):
    codigo = forms.CharField(label='Código', max_length=10, required=True)


class TurmaForm(BSModalForm):
    class Meta:
        model = Turma
        fields = ['nome', 'secao', 'sala', 'discord', 'github', 'imagem']

    def __init__(self, *args, **kwargs):
        self.turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)

        if self.turma:
            self.fields['discord'].label = 'Canal do Discord'
            self.fields['github'].label = 'Repositório no GitHub'
        else:
            self.fields.pop('discord')
            self.fields.pop('github')


class ModuloQuestaoForm(forms.Form):
    nome_modulo = forms.CharField(label='Nome do módulo', max_length=255, required=True,
                                  help_text='Módulo da sua turma. Ex: estruturas de repetição, vetores e matrizes, '
                                            'etc.')
    descricao_modulo = forms.CharField(label='Descrição (opcional)', required=False, max_length=1000,
                                       widget=forms.Textarea(attrs={'rows': 6}),
                                       help_text='130 restantes')
    sentenca_questao = forms.CharField(label='Sentença', max_length=255, required=True,
                                       help_text='Ex: Sobre programação estruturada e programação orientada a '
                                                 'objetos, é INCORRETO afirmar que:')
    descricao_questao = forms.CharField(label='Descrição (opcional)', required=False, max_length=1000,
                                        widget=CKEditorUploadingWidget())


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        exclude = ('criado_em', 'atualizado_em', 'turma')
        labels = {
            'nome': 'Nome do módulo',
            'descricao': 'Descrição (opcional)'
        }
        help_texts = {
            'descricao': '130 restantes'
        }


class ModuloModalForm(BSModalForm):
    class Meta:
        model = Modulo
        fields = ['nome', 'descricao']
        labels = {
            'nome': 'Nome do módulo',
            'descricao': 'Descrição'
        }
        help_texts = {
            'descricao': '130 restantes'
        }


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['verbo', 'sentenca', 'descricao', 'tempo_para_responder']
        # help_texts = {
        #     'sentenca': 'Ex: Sobre programação estruturada e programação orientada a objetos, é INCORRETO afirmar '
        #                 'que:'
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = RequestMiddleware(get_response=None).thread_local.current_request

        self.fields['sentenca'].label = 'Enunciado da questão'

        self.fields['tempo_para_responder'].label = 'Tempo de resposta'
        self.fields['tempo_para_responder'].widget.attrs = {'class': 'time'}

        try:
            nivel = self.request.resolver_match.kwargs['nivel']
        except KeyError:
            questao_uuid = self.request.resolver_match.kwargs['uuid']
            questao = get_object_or_404(Questao, uuid=questao_uuid)
            nivel = questao.nivel

        self.fields['verbo'].queryset = Verbo.objects.filter(nivel=nivel)
        self.fields['verbo'].empty_label = None
