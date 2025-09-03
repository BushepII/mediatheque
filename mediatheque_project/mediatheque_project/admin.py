from django.contrib import admin
from .models import Livre, Dvd, Cd, JeuDePlateau, Emprunteur

admin.site.register(Livre)
admin.site.register(Dvd)
admin.site.register(Cd)
admin.site.register(JeuDePlateau)
admin.site.register(Emprunteur)