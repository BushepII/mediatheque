from  django.shortcuts import render
from mediatheque_project.models import Livre, Dvd, Cd, JeuDePlateau

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

"""
def ajoutlivre(request):
    if request.method == 'POST':
        creationlivre = Creationlivre(request.POST)
        if creationlivre.is_valid():
            livre = Livre()
            livre.nom = creationlivre.cleaned_data['nom']
            livre.auteur = creationlivre.cleaned_data['auteur']
            livre.save()
            livres = Livre.objects.all()
            return render(request, 'medias/lists.html', {'medias': livres})
    else:
        creationlivre = Creationlivre()
        return render(request, 'medias/ajoutmedia.html', {'creationlivres': creationlivre})
"""