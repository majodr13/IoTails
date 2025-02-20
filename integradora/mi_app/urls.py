from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='home'),  # Agrega esta línea para que la vista main_view sea la raíz
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
]
