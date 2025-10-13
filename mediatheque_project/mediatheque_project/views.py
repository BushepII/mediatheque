from  django.shortcuts import render, redirect
from mediatheque_project.models import Livre, Dvd, Cd, JeuDePlateau
from django.contrib import messages
from django.contrib.auth import authenticate, login
from mediatheque_project.forms import *

def menumembre(request):
    livres = list(Livre.objects.all())
    dvds = list(Dvd.objects.all())
    cds = list(Cd.objects.all())
    jeux = list(JeuDePlateau.objects.all())

    context = {
        "livres": livres,
        "dvds": dvds,
        "cds": cds,
        "jeux": jeux,
    }

    return render(request, 'medias/lists.html', context)

def staff_page(request):
    return render(request, "staff_page.html")


def ajoutlivre(request):
    if request.method == 'POST':
        creationlivre = Creationlivre(request.POST)
        if creationlivre.is_valid():
            livre = Livre()
            livre.name = creationlivre.cleaned_data['nom']
            livre.auteur = creationlivre.cleaned_data['auteur']
            livre.save()
            messages.success(request, f"Book '{livre.name}' added successfully!")
            return redirect('ajoutlivre')
    else:
        creationlivre = Creationlivre()

    livres = Livre.objects.all()
    return render(request, 'medias/ajoutmedia.html', {'creationlivres': creationlivre})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("staff_page")  # redirect to user page
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    return render(request, "login.html")