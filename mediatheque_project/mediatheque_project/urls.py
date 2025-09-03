from django.urls import path
from django.contrib import admin
from mediatheque_project import views

urlpatterns = [
    path('', views.menumembre),
    path("admin/", admin.site.urls),
]
