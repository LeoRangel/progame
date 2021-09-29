import django_filters as filters
from core.middleware import RequestMiddleware
from progame.models import Questao, Verbo

QUESTAO_NIVEL_CHOICES = (
    (1, '1 - Lembrar'),
    (2, '2 - Entender'),
    (3, '3 - Aplicar'),
    (4, '4 - Analisar'),
    (5, '5 - Avaliar'),
    (6, '6 - Criar'),
)


class ImportarQuestoesFilter(filters.FilterSet):
    questao = filters.CharFilter(label="Questão", lookup_expr='icontains', field_name='sentenca')
    verbo = filters.ModelChoiceFilter(queryset=Verbo.objects.none())
    # nivel = filters.ChoiceFilter(label="Nível", choices=QUESTAO_NIVEL_CHOICES, field_name="quiz__nivel")

    class Meta:
        model = Questao
        fields = ['verbo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = RequestMiddleware(get_response=None).thread_local.current_request
        self.nivel = self.request.resolver_match.kwargs['nivel']

        self.form.fields['verbo'].queryset = Verbo.objects.filter(nivel=self.nivel)