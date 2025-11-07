from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Livre, Dvd, Cd, JeuDePlateau, Emprunteur, Emprunt


admin.site.register(Livre)
admin.site.register(Dvd)
admin.site.register(Cd)
admin.site.register(JeuDePlateau)
admin.site.register(Emprunteur)
admin.site.register(Emprunt)