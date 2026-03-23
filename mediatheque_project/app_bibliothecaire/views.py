from  django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import normalize_newlines

from app_bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau, Emprunt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app_bibliothecaire.forms import *
from django.utils import timezone
from django.db.utils import OperationalError
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q


logger = logging.getLogger('app_bibliothecaire')

choixMedia = {
    'livre': Livre,
    'dvd': Dvd,
    'cd': Cd,
    'jeu': JeuDePlateau,
}


@login_required(login_url="staff/login/")
def pageStaff(request):
    livres = list(Livre.objects.all())
    dvds = list(Dvd.objects.all())
    cds = list(Cd.objects.all())
    jeux = list(JeuDePlateau.objects.all())
    emprunteurs = list(Emprunteur.objects.all())

    try:
        for listeMedia, typeMedia in [(livres, 'livre'), (dvds, 'dvd'), (cds, 'cd')]:
            for media in listeMedia:
                media.empruntActuel = Emprunt.objects.filter(
                    typeMedia=typeMedia,
                    idMedia=media.id,
                    mediaRendu=False
                ).first()
                if media.empruntActuel:
                    media.empruntActuel.retard = media.empruntActuel.dateRetour< timezone.now()
    except OperationalError:
        pass

    context = {
        "livres": livres,
        "dvds": dvds,
        "cds": cds,
        "jeux": jeux,
        "emprunteurs": emprunteurs,
        "nombreLivre": len(livres),
        "nombreDvd": len(dvds),
        "nombreCd": len(cds),
        "nombreJeu": len(jeux)
    }

    return render(request, "pageStaff.html", context)

@login_required(login_url="staff/login/")
def supprimerMedia(request, typeMedia, idMedia):
    model = choixMedia.get(typeMedia)
    if not model:
        messages.error(request, "Type de média invalide.")
        return redirect('pageStaff')

    media = get_object_or_404(model, id=idMedia)
    media.delete()
    messages.success(request, f"{typeMedia.capitalize()} '{media.nom}' bien supprimé !")
    return redirect('pageStaff')

@login_required(login_url="staff/login/")
def ajoutMedia(request):
    if request.method == 'POST':
        form = CreationMediaForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            createur = form.cleaned_data['createur']
            typeMedia = form.cleaned_data['typeMedia']

            media = None

            if typeMedia == 'livre':
                media = Livre.objects.create(nom=nom, auteur=createur)
            elif typeMedia == 'dvd':
                media = Dvd.objects.create(nom=nom, realisateur=createur)
            elif typeMedia == 'cd':
                media = Cd.objects.create(nom=nom, artiste=createur)
            elif typeMedia == 'jeu':
                media = JeuDePlateau.objects.create(nom=nom, createur=createur)

            logger.info("'%s' créé: '%s' de '%s' (id='%s') par l'utilisateur", typeMedia, nom, createur, media.id)
            messages.success(request, f"{typeMedia} '{nom}' créé avec succès !")
            return redirect('ajoutMedia')
    else:
        form = CreationMediaForm()

    return render(request, 'medias/ajoutMedia.html', {'form': form})


def pageLogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("pageStaff")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    return render(request, "login.html")


@login_required(login_url="staff/login/")
def modifierMedia(request, typeMedia, idMedia):
    model = choixMedia.get(typeMedia)
    if not model:
        messages.error(request, "Invalid media type.")
        return redirect('pageStaff')

    media = get_object_or_404(model, id=idMedia)

    if request.method == 'POST':
        form = CreationMediaForm(request.POST)
        if form.is_valid():
            media.nom = form.cleaned_data['nom']
            if typeMedia == 'livre':
                media.auteur = form.cleaned_data['createur']
            elif typeMedia == 'dvd':
                media.realisateur = form.cleaned_data['createur']
            elif typeMedia == 'cd':
                media.artiste = form.cleaned_data['createur']
            elif typeMedia == 'jeu':
                media.createur = form.cleaned_data['createur']
            media.save()
            messages.success(request, f"Média bien modifié !")
            return render(request, 'medias/modifierMedia.html', {'form': form, 'typeMedia': typeMedia})
    else:
        creator_field = getattr(media, 'auteur', None) or getattr(media, 'realisateur', None) \
                        or getattr(media, 'artiste', None) or getattr(media, 'createur', '')
        form = CreationMediaForm(initial={
            'nom': media.nom,
            'createur': creator_field,
            'typeMedia': typeMedia
        })

    return render(request, 'medias/modifierMedia.html', {'form': form, 'typeMedia': typeMedia})

@login_required(login_url="staff/login/")
def ajoutEmprunteur(request):
    if request.method == "POST":
        form = CreationEmprunteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Emprunteur créé avec succès !")
            return redirect('ajoutEmprunteur')

    else:
        form = CreationEmprunteurForm()

    return render(request, 'emprunteurs/ajoutEmprunteur.html', {'form': form})


@require_GET
def rechercheMedia(request):
    typeMedia = request.GET.get('typeMedia')
    query = request.GET.get('q', '').strip()  # empty string if no input

    model = choixMedia.get(typeMedia)
    if not model:
        return JsonResponse({'results': []})

    # If query is empty, return all available media
    if query:
        # Filter by existing fields per media type
        filters = Q(nom__icontains=query)
        if typeMedia == 'livre':
            filters |= Q(auteur__icontains=query)
        elif typeMedia == 'dvd':
            filters |= Q(realisateur__icontains=query)
        elif typeMedia == 'cd':
            filters |= Q(artiste__icontains=query)
        elif typeMedia == 'jeu':
            filters |= Q(createur__icontains=query)

        results = model.objects.filter(disponible=True).filter(filters)
    else:
        results = model.objects.filter(disponible=True)  # return all available media

    data = [{
        'id': m.id,
        'text': f"{m.nom} ({getattr(m, 'auteur', '') or getattr(m, 'realisateur', '') or getattr(m, 'artiste', '') or getattr(m, 'createur', '')})"
    } for m in results]

    return JsonResponse({'results': data})

@require_GET
def rechercheEmprunteur(request):
    query = request.GET.get('q', '')

    emprunteurs = Emprunteur.objects.all()
    if query:
        emprunteurs = emprunteurs.filter(nom__icontains=query)

    data = [{'id': b.id, 'text': f"{b.nom} {b.prenom}"} for b in emprunteurs]

    return JsonResponse({'results': data})


@login_required(login_url="staff/login/")
def pageEmprunt(request):
    erreurMessage = None

    if request.method == 'POST':
        form = BorrowMediaForm(request.POST)
        if form.is_valid():
            emprunteur = form.cleaned_data['emprunteur']
            idMedia = form.cleaned_data['idMedia']
            typeMedia = form.cleaned_data['typeMedia']

            if not peutEmprunter(emprunteur):
                messages.error(request, "L'emprunteur est bloqué.")
                return redirect("pageEmprunt")

            model = choixMedia.get(typeMedia)
            media = get_object_or_404(model, id=idMedia)

            if typeMedia == 'jeu':
                messages.error(request, 'Un jeu de plateau ne peut pas être emprunté.')
                return redirect("pageEmprunt")

            if media.disponible:
                Emprunt.objects.create(
                    emprunteur=emprunteur,
                    typeMedia=typeMedia,
                    idMedia=idMedia,
                    dateEmprunt=timezone.now(),
                    dateRetour=timezone.now() + timezone.timedelta(days=7),  # example loan duration
                    mediaRendu=False
                )
                media.disponible = False
                media.save()
                messages.success(request, f"{media.nom} emprunté par {emprunteur.prenom} {emprunteur.nom} !")
            else:
                messages.error(request, "Ce média n'est pas disponible.")

            return redirect('pageEmprunt')
    else:
        form = BorrowMediaForm()

    return render(request, 'medias/empruntMedia.html', {'form': form, 'erreurMessage': erreurMessage})


def peutEmprunter(emprunteur):
    empruntActif = Emprunt.objects.filter(
        emprunteur=emprunteur,
        mediaRendu=False
    )

    overdue =  empruntActif.filter(dateRetour__lt=timezone.now()).exists()

    if overdue or  empruntActif.count() >= 3:
        emprunteur.bloque = True
        emprunteur.save(update_fields=['bloque'])
        return False
    else:
        emprunteur.bloque = False
        emprunteur.save(update_fields=['bloque'])
        return True

@login_required(login_url="staff/login/")
def retourMedia(request, typeMedia, idMedia):
    model = choixMedia.get(typeMedia)
    media = get_object_or_404(model, id=idMedia)

    emprunt = Emprunt.objects.filter(
        typeMedia=typeMedia,
        idMedia=media.id,
        mediaRendu=False
    ).first()

    if emprunt:
        emprunt.mediaRendu = True
        emprunt.save()

        media.disponible = True
        media.save()

        messages.success(request, f"{media.nom} a été rendu avec succès.")
    else:
        messages.warning(request, f"Aucun emprunt actif trouvé pour {media.nom}.")

    return redirect('pageStaff')

@login_required(login_url="staff/login/")
def modifierEmprunteur(request, idEmprunteur):
    emprunteur = get_object_or_404(Emprunteur, id=idEmprunteur)

    if request.method == 'POST':
        form = CreationEmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'emprunteur {emprunteur.prenom} {emprunteur.nom} a été modifié avec succès !")
            return render(request, 'emprunteurs/modifierEmprunteur.html', {
                'form': form,
                'emprunteur': emprunteur,
            })
    else:
        form = CreationEmprunteurForm(instance=emprunteur)

    return render(request, 'emprunteurs/modifierEmprunteur.html', {
        'form': form,
        'emprunteur': emprunteur,
    })

@login_required(login_url="staff/login/")
def supprimerEmprunteur(request, idEmprunteur):
    emprunteur = get_object_or_404(Emprunteur, id=idEmprunteur)
    emprunteur.delete()
    messages.success(request, f"L'emprunteur {emprunteur.nom} {emprunteur.prenom} a bien été supprimé !")
    return redirect('pageStaff')