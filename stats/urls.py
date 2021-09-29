from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from stats import views

app_name = 'stats'

urlpatterns = [

    path('turma/<uuid:uuid>/modulos/', views.ModuloListView.as_view(), name='modulo_list_view'),
    path('modulo/<uuid:uuid>/', views.ModuloDetailView.as_view(), name='modulo_detail_view'),

    path('turma/<uuid:uuid>/alunos/', views.AlunoListView.as_view(), name='aluno_list_view'),
    path('turma/<uuid:uuid>/aluno/<int:pk>/', views.AlunoDetailView.as_view(), name='aluno_detail_view'),

    # Modais
    path('get-aluno-modulo-info/aluno/<int:pk>/', views.GetAlunoModuloInfo.as_view(), name='get_aluno_modulo_info'),
    path('get-quiz-info/nivel/<uuid:uuid>/', views.GetQuizInfo.as_view(), name='get_modulo_info'),
    path('get-modulo-aluno-info/modulo/<uuid:uuid>/', views.GetModuloAlunoInfo.as_view(), name='get_modulo_aluno_info'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
