from django.urls import path
from .views import register, user_login, reset_password
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


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
    path('control_painel/', auth_views.LoginView.as_view(template_name='control_painel.html'), name='control_painel'),     # Rota para o painel de controle
    
]