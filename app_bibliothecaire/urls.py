from django.urls import path
from app_bibliothecaire import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.pageStaff, name="pageStaff"),
    path("login/", views.pageLogin, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ajoutmedia/', views.ajoutMedia, name="ajoutMedia"),
    path('recherchemedia/', views.rechercheMedia, name='rechercheMedia'),
    path('modifier/<str:typeMedia>/<int:idMedia>/', views.modifierMedia, name='modifierMedia'),
    path('return/<str:typeMedia>/<int:idMedia>/', views.retourMedia, name='retourMedia'),
    path('delete/<str:typeMedia>/<int:idMedia>/', views.supprimerMedia, name='supprimerMedia'),
    path('ajoutEmprunteur/', views.ajoutEmprunteur, name='ajoutEmprunteur'),
    path('emprunt/', views.pageEmprunt, name='pageEmprunt'),
    path('rechercheEmprunteur/', views.rechercheEmprunteur, name='rechercheEmprunteur'),
    path('edit/<int:idEmprunteur>/', views.modifierEmprunteur, name='modifierEmprunteur'),
    path('delete/<int:idEmprunteur>/', views.supprimerEmprunteur, name='supprimerEmprunteur'),
]