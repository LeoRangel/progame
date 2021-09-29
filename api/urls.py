from django.urls import path
from rest_framework import routers
from . import api


router = routers.DefaultRouter()

urlpatterns = [
    # aluno e user
    path('aluno/', api.AlunoRetrieve.as_view()),

    # quiz
    path('quiz/<uuid:modulo_uuid>/<int:nivel>/', api.QuizRetrieve.as_view()),

    # turma
    path('turma/<uuid:uuid>/', api.TurmaRetrieve.as_view()),

    # modulo
    path('modulo/<uuid:uuid>/', api.ModuloRetrieve.as_view()),
    path('modulo/turma/<uuid:turma_uuid>/', api.ModuloList.as_view()),

    # questao
    path('questao/<uuid:uuid>/', api.QuestaoRetrieve.as_view()),
    path('questao/modulo/<uuid:modulo_uuid>/<int:nivel>/', api.QuestaoList.as_view()),

    # alternativa
    path('alternativa/questao/<uuid:questao_uuid>/', api.AlternativaQuestaoList.as_view()),
    path('alternativa/modulo/<uuid:modulo_uuid>/<int:questao_nivel>/', api.AlternativaModuloNivelList.as_view()),
    path('alternativa_correta/questao/<uuid:questao_uuid>/', api.AlternativaCorretaList.as_view()),

    # resposta
    path('resposta/', api.RespostaCreate.as_view()),

    # resultado
    path('resultado/', api.ResultadoView.as_view()),
]


urlpatterns += router.urls
