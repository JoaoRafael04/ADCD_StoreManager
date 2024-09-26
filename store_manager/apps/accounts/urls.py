from django.urls import path
from .views import register, user_login, cadastrar_filial, listar_filiais
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views


class CustomLoginView(LoginView):
    template_name = 'control_painel.html'  # O template que será renderizado após login

    def get_success_url(self):
        return '/control_painel/'  # Redireciona para a página do painel de controle

urlpatterns = [
    path('register/', register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # Rota de logout
    path('control_painel/', listar_filiais , name='control_painel'),     # Rota para o painel de controle
    
    
    
    path('cadastrar_empresa/', cadastrar_filial, name='cadastrar_empresa'),
    # rota para listar todas as filiais cadastradas
    # path('lista_filiais/', listar_filiais, name='lista_filiais'),
    # rota para o formulÃ¡rio de cadastro de nova filial
    path('filiais/cadastrar/', views.cadastrar_filial, name='cadastrar_filial'),
    
]