from django.urls import path
from . import views

urlpatterns = [
    path('', views.rifa_detail, name='rifa_detail'),
]
