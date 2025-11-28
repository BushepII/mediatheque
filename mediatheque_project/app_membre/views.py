from  django.shortcuts import render
from app_bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau
from django.contrib.auth import logout


MEDIA_MODELS = {
    'livre': Livre,
    'dvd': Dvd,
    'cd': Cd,
    'jeu': JeuDePlateau,
}

def menumembre(request):
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
        "livres_count": len(livres),
        "dvds_count": len(dvds),
        "cds_count": len(cds),
        "jeux_count": len(jeux)
    }

    return render(request, 'home_page.html', context)