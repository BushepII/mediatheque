from django.urls import path
from django.contrib import admin
from app_bibliothecaire import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ajoutmedia/', views.ajoutmedia, name="ajoutmedia"),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.staff_page, name="staff_page"),
    path('delete/<str:media_type>/<int:media_id>/', views.delete_media, name='delete_media'),
    path('edit/<str:media_type>/<int:media_id>/', views.edit_media, name='edit_media'),
    path('ajoutemprunteur/', views.ajout_emprunteur, name='ajoutemprunteur'),
    path('borrow/', views.borrow_page, name='borrow_page'),
    path('search_media/', views.search_media, name='search_media'),
    path('search_borrowers/', views.search_borrowers, name='search_borrowers'),
    path('return/<str:media_type>/<int:media_id>/', views.return_media, name='return_media'),
    path('edit/<int:emprunteur_id>/', views.edit_emprunteur, name='edit_emprunteur'),
    path('delete/<int:emprunteur_id>/', views.delete_emprunteur, name='delete_emprunteur'),
]
