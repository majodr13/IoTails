from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
    path('home/', views.home_view, name='home'),
    path('form/', views.form_view, name='form'),
    path("registrar/", views.registrar_mascota, name="registrar_mascota"),
]
