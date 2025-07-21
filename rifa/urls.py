from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rifa/<int:raffle_id>/', views.raffle_detail, name='raffle-detail'),
    path('rifa/<int:raffle_id>/reservar/<int:number_id>/', views.reservar_numero, name='raffle-reserve'),
    path('premios/', views.premios, name='premios'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]
