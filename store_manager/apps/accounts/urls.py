from django.urls import path
from .views import register, user_login, logoff

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logoff, name='logout'),
]
