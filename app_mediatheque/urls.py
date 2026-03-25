from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app_membre.urls')),
    path('staff/', include('app_bibliothecaire.urls')),
]
