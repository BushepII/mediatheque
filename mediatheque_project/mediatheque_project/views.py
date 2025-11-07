from django.db.migrations.operations.base import Operation
from  django.shortcuts import render, redirect, get_object_or_404
from mediatheque_project.models import Livre, Dvd, Cd, JeuDePlateau, Emprunt, Emprunteur
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mediatheque_project.forms import *
from django.utils import timezone
from django.db.utils import OperationalError

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q

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

@login_required(login_url="/login/")
def staff_page(request):
    livres = list(Livre.objects.all())
    dvds = list(Dvd.objects.all())
    cds = list(Cd.objects.all())
    jeux = list(JeuDePlateau.objects.all())
    emprunteurs = list(Emprunteur.objects.all())

    try:
        for media_list, media_type in [(livres, 'livre'), (dvds, 'dvd'), (cds, 'cd')]:
            for media in media_list:
                media.current_emprunt = Emprunt.objects.filter(
                    media_type=media_type,
                    media_id=media.id,
                    returned=False
                ).first()
                if media.current_emprunt:
                    # Calculate if the media is overdue
                    media.current_emprunt.is_overdue = media.current_emprunt.date_retour < timezone.now()
    except OperationalError:
        pass

    context = {
        "livres": livres,
        "dvds": dvds,
        "cds": cds,
        "jeux": jeux,
        "livres_count": len(livres),
        "dvds_count": len(dvds),
        "cds_count": len(cds),
        "jeux_count": len(jeux),
        "emprunteurs": emprunteurs,
    }

    return render(request, "staff_page.html", context)

@login_required(login_url="/login/")
def delete_media(request, media_type, media_id):
    model = MEDIA_MODELS.get(media_type)
    if not model:
        messages.error(request, "Invalid media type.")
        return redirect('staff_page')

    media = get_object_or_404(model, id=media_id)
    media.delete()
    messages.success(request, f"{media_type.capitalize()} '{media.name}' bien supprimé !")
    return redirect('staff_page')

@login_required(login_url="/login/")
def ajoutmedia(request):
    if request.method == 'POST':
        form = CreationMediaForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            createur = form.cleaned_data['createur']
            media_type = form.cleaned_data['media_type']

            if media_type == 'livre':
                Livre.objects.create(name=nom, auteur=createur)
            elif media_type == 'dvd':
                Dvd.objects.create(name=nom, realisateur=createur)
            elif media_type == 'cd':
                Cd.objects.create(name=nom, artiste=createur)
            elif media_type == 'jeu':
                JeuDePlateau.objects.create(name=nom, createur=createur)

            messages.success(request, f"{media_type.capitalize()} '{nom}' bien ajouté !")
            return redirect('ajoutmedia')
    else:
        form = CreationMediaForm()

    return render(request, 'medias/ajoutmedia.html', {'form': form})


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

@login_required(login_url="/login/")
def edit_media(request, media_type, media_id):
    model = MEDIA_MODELS.get(media_type)
    if not model:
        messages.error(request, "Invalid media type.")
        return redirect('staff_page')

    media = get_object_or_404(model, id=media_id)

    if request.method == 'POST':
        form = CreationMediaForm(request.POST)
        if form.is_valid():
            media.name = form.cleaned_data['nom']
            # Set creator field depending on media type
            if media_type == 'livre':
                media.auteur = form.cleaned_data['createur']
            elif media_type == 'dvd':
                media.realisateur = form.cleaned_data['createur']
            elif media_type == 'cd':
                media.artiste = form.cleaned_data['createur']
            elif media_type == 'jeu':
                media.createur = form.cleaned_data['createur']
            media.save()
            messages.success(request, f"{media_type.capitalize()} updated successfully!")
            return redirect('staff_page')
    else:
        # Pre-fill form with existing values
        creator_field = getattr(media, 'auteur', None) or getattr(media, 'realisateur', None) \
                        or getattr(media, 'artiste', None) or getattr(media, 'createur', '')
        form = CreationMediaForm(initial={
            'nom': media.name,
            'createur': creator_field,
            'media_type': media_type
        })

    return render(request, 'medias/editmedia.html', {'form': form, 'media_type': media_type})

@login_required(login_url="/login/")
def ajout_emprunteur(request):
    if request.method == "POST":
        form = CreationEmprunteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Emprunteur créé avec succès !")
            return redirect('ajoutemprunteur')

    else:
        form = CreationEmprunteurForm()

    return render(request, 'borrowers/ajoutemprunteur.html', {'form': form})


@require_GET
def search_media(request):
    media_type = request.GET.get('media_type')
    query = request.GET.get('q', '').strip()  # empty string if no input

    model = MEDIA_MODELS.get(media_type)
    if not model:
        return JsonResponse({'results': []})

    # If query is empty, return all available media
    if query:
        # Filter by existing fields per media type
        filters = Q(name__icontains=query)
        if media_type == 'livre':
            filters |= Q(auteur__icontains=query)
        elif media_type == 'dvd':
            filters |= Q(realisateur__icontains=query)
        elif media_type == 'cd':
            filters |= Q(artiste__icontains=query)
        elif media_type == 'jeu':
            filters |= Q(createur__icontains=query)

        results = model.objects.filter(disponible=True).filter(filters)
    else:
        results = model.objects.filter(disponible=True)  # return all available media

    data = [{
        'id': m.id,
        'text': f"{m.name} ({getattr(m, 'auteur', '') or getattr(m, 'realisateur', '') or getattr(m, 'artiste', '') or getattr(m, 'createur', '')})"
    } for m in results]

    return JsonResponse({'results': data})

@require_GET
def search_borrowers(request):
    query = request.GET.get('q', '')

    borrowers = Emprunteur.objects.all()
    if query:
        borrowers = borrowers.filter(name__icontains=query)

    data = [{'id': b.id, 'text': b.name} for b in borrowers]

    return JsonResponse({'results': data})


@login_required(login_url="/login/")
def borrow_page(request):
    error_message = None

    if request.method == 'POST':
        form = BorrowMediaForm(request.POST)
        if form.is_valid():
            borrower = form.cleaned_data['borrower']
            media_id = form.cleaned_data['media_id']
            media_type = form.cleaned_data['media_type']

            # Check if borrower can borrow
            active_borrows = Emprunt.objects.filter(borrower=borrower, returned=False)
            now = timezone.localtime(timezone.now())
            overdue = active_borrows.filter(date_retour__lt=now).exists()

            if overdue:
                error_message = messages.error(request, f"{borrower.name} has overdue media and cannot borrow more.")
                return redirect('borrow_page')

            if active_borrows.count() >= 3:
                error_message = messages.error(request, f"{borrower.name} already has 3 borrowed media.")
                return redirect('borrow_page')

            model = MEDIA_MODELS.get(media_type)
            media = get_object_or_404(model, id=media_id)

            if media.disponible:
                # Create borrow record
                Emprunt.objects.create(
                    borrower=borrower,
                    media_type=media_type,
                    media_id=media.id,
                    date_emprunt=now,
                    date_retour=now + timezone.timedelta(days=7),  # example loan duration
                    returned=False
                )
                media.disponible = False
                media.save()
                error_message = messages.success(request, f"{media.name} emprunté par {borrower.name} !")
            else:
                error_message = messages.error(request, "Ce média n'est pas disponible.")

            return redirect('borrow_page')
    else:
        form = BorrowMediaForm()

    return render(request, 'medias/borrow_media.html', {'form': form, 'error_message': error_message})


def can_borrow(borrower):
    active_borrows = Emprunt.objects.filter(
        emprunteur=borrower,
        returned=False
    )

    # Check if any is overdue
    now = timezone.localtime(timezone.now())
    overdue = active_borrows.filter(date_retour__lt=now).exists()

    if overdue or active_borrows.count() >= 3:
        return False
    return True

@login_required(login_url="/login/")
def return_media(request, media_type, media_id):
    model = MEDIA_MODELS.get(media_type)
    media = get_object_or_404(model, id=media_id)

    # Find the current active borrow (not yet returned)
    emprunt = Emprunt.objects.filter(
        media_type=media_type,
        media_id=media.id,
        returned=False
    ).first()

    if emprunt:
        emprunt.returned = True
        emprunt.date_retour_effective = timezone.now()  # optional, if you want to track return date
        emprunt.save()

        media.disponible = True
        media.save()

        messages.success(request, f"{media.name} a été rendu avec succès.")
    else:
        messages.warning(request, f"Aucun emprunt actif trouvé pour {media.name}.")

    return redirect('staff_page')

@login_required(login_url="/login/")
def edit_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)

    if request.method == 'POST':
        form = CreationEmprunteurForm(request.POST, instance=emprunteur)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'emprunteur {emprunteur.name} a été modifié avec succès !")
            return redirect('staff_page')
    else:
        form = CreationEmprunteurForm(instance=emprunteur)

    return render(request, 'borrowers/edit_emprunteur.html', {
        'form': form,
        'emprunteur': emprunteur,
    })

@login_required(login_url="/login/")
def delete_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)
    emprunteur.delete()
    messages.success(request, f"L'emprunteur {emprunteur.name} {emprunteur.firstname} a bien été supprimé !")
    return redirect('staff_page')