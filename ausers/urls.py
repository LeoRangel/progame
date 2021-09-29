from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from ausers import views

app_name = 'ausers'

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('aluno/cadastro/', views.CadastroAluno.as_view(), name='aluno_cadastro'),
    # path('professor/cadastro/', views.CadastroProfessor.as_view(), name='professor_cadastro'),

] + static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)