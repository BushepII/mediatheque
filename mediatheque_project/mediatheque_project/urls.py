from django.urls import path
from django.contrib import admin
from mediatheque_project import views

urlpatterns = [
    path('', views.menumembre),
    path('ajoutlivre/', views.ajoutlivre, name="ajoutlivre"),
    path("login/", views.login_view, name="login"),
    path('staff/', views.staff_page, name="staff_page"),
    path("admin/", admin.site.urls),
]
