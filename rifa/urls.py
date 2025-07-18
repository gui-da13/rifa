from django.urls import path
from . import views

urlpatterns = [
    path('', views.rifa_detail, name='rifa_detail'),
    path('rifa/<int:rifa_id>/', views.rifa_detail, name='rifa_detail'),
    path('rifa/<int:rifa_id>/reservar/<int:numero>/', views.reservar_numero, name='reservar_numero'),
]
