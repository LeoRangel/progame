from django.urls import path
from progame import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'progame'

urlpatterns = [
   
   # Forum - Em breve
   path('turma/<uuid:uuid>/forum/', views.ForumTemplateView.as_view(), name='forum'),
   
   # Perfis
   path('aluno/<uuid:uuid>/perfil/', views.AlunoPerfilDetailView.as_view(), name='aluno_perfil'),


   # Central de ajuda
   path('ajuda/', views.ajuda, name='ajuda'),
   path('ajuda/primeiros-passos/', views.primeiros_passos, name='primeiros_passos'),
   path('ajuda/turmas-e-alunos/', views.turmas_e_alunos, name='turmas_e_alunos'),
   path('ajuda/modulos/', views.modulos, name='modulos'),
   path('ajuda/quizzes/', views.quizzes, name='quizzes'),
   path('ajuda/rankings/', views.rankings, name='rankings'),
   path('ajuda/estatisticas/', views.estatisticas, name='estatisticas'),


   path('', views.PublicIndexTemplateView.as_view(), name='public_index'),


   path('dashboard/', views.get_dashboard, name='get_dashboard'),
   path('perfil_update/', views.get_perfil_update, name='get_perfil_update'),

   path('finalizar_cadastro/', views.EscolherTipoConta.as_view(), name='escolher_tipo_conta'),

   # aluno
   path('aluno/dashboard/', views.AlunoDashboard.as_view(), name='aluno_dashboard'),
   path('aluno/perfil/atualizar/', views.AlunoUpdateView.as_view(), name='aluno_update_view'),
   path('aluno/turma/participar/', views.AlunoParticiparTurma.as_view(), name='aluno_participar_turma'),

   # professor
   path('professor/dashboard/', views.ProfessorDashboard.as_view(), name='professor_dashboard'),
   path('professor/perfil/atualizar/', views.ProfessorUpdateView.as_view(), name='professor_update_view'),

   # turma
   path('turma/criar/', views.TurmaCreateView.as_view(), name='turma_create_view'),
   path('turma/<uuid:uuid>/', views.TurmaDetailView.as_view(), name='turma_detail_view'),
   path('turma/<uuid:uuid>/remover/', views.TurmaDeleteView.as_view(), name='turma_delete_view'),
   # path('turma/<uuid:uuid>/finalizar_cadastro/', views.TurmaFinalizarCadastro.as_view(),
   #      name='turma_finalizar_cadastro'),
   # path('turma/<uuid:uuid>/pular_cadastro_modulo/', views.PularCadastroModulo.as_view(),
   #      name='pular_cadastro_modulo'),
   path('turma/<uuid:uuid>/atualizar/', views.TurmaUpdateView.as_view(), name='turma_update_view'),
   

   # modulo
   path('modulo/<uuid:uuid>/', views.ModuloDetailView.as_view(), name='modulo_detail_view'),
   path('turma/<uuid:uuid>/modulo/adicionar/', views.ModuloCreateView.as_view(), name='modulo_create_view'),
   path('modulo/<uuid:uuid>/atualizar/', views.ModuloUpdateView.as_view(), name='modulo_update_view'),
   path('modulo/<uuid:uuid>/remover/', views.ModuloDeleteView.as_view(), name='modulo_delete_view'),
   path('modulo/<uuid:uuid>/ranking/', views.ModuloRankingDetailView.as_view(), name='modulo_ranking_detail_view'),

   path('aluno/modulo/<uuid:uuid>/', views.AlunoModuloDetailView.as_view(), name='aluno_modulo_detail_view'),

   # questao
   path('modulo/<uuid:uuid>/questoes/', views.QuestaoListView.as_view(), name='questao_list_view'),
   path('modulo/<uuid:uuid>/questao/<int:nivel>/adicionar/', views.QuestaoCreateView.as_view(),
        name='questao_create_view'),
   path('modulo/questao/<uuid:uuid>/atualizar/', views.QuestaoUpdateView.as_view(), name='questao_update_view'),

   # importar questao
   path('modulo/<uuid:uuid>/importar-questoes/<int:nivel>/', views.ImportarQuestoesListView.as_view(),
        name="importar_questoes_list_view"),
   path('importar-questoes/<uuid:uuid>/<int:nivel>/', views.ImportarQuestoesView.as_view(), name="importar_questoes"),

   # quiz
   path('quiz/toggle_bloqueio/', views.ToggleBloqueioQuiz.as_view(), name='quiz_toggle_bloqueio'),

] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
