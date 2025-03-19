from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
    path('home/', views.home_view, name='home'),
    path('form/', views.form_view, name='form'),
    path('registrar_mascota/', views.registrar_mascota, name='registrar_mascota'),
    path('perfil/', views.profile_view, name='perfil'),
    path('mapa/', views.mapa_views, name='mapa'),

    # Password
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Sensor y API
    path('cuidados/', views.cuidados_views, name='cuidados'),
    path('api/cuidados/', views.api_cuidados, name='api_cuidados'),
    path('obtener-datos/', views.obtener_datos_sensores, name='obtener_datos'),

    path('api/resumen/', views.recibir_datos_resumen, name='api_resumen'),

    # Vista de resumen
    path('resumen/', views.resumen_view, name='resumen_view'),
]
