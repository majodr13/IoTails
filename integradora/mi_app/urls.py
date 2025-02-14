from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),  
]
