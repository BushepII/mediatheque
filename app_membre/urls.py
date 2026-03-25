from django.urls import path
from app_membre import views

urlpatterns = [
    path('', views.menuMembre, name='home'),
]
