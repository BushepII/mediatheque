from  django.shortcuts import render
from app_bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau
from django.contrib.auth import logout


choixMedia = {
    'livre': Livre,
    'dvd': Dvd,
    'cd': Cd,
    'jeu': JeuDePlateau,
}

def menuMembre(request):
    if request.user.is_authenticated:
        logout(request)

    livres = list(Livre.objects.all())
    dvds = list(Dvd.objects.all())
    cds = list(Cd.objects.all())
    jeux = list(JeuDePlateau.objects.all())

    context = {
        "livres": livres,
        "dvds": dvds,
        "cds": cds,
        "jeux": jeux,
        "nombreLivre": len(livres),
        "nombreDvd": len(dvds),
        "nombreCd": len(cds),
        "nombreJeu": len(jeux)
    }

    return render(request, 'homePage.html', context)