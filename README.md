# Commandes pour Django

## Démarrer le serveur
```bash
python manage.py runserver
```

## Installer l'environnement et l'activer

- ``` python -m venv env ```
- ``` venv/Scripts/activate.bat ```

## Ajouter un projet
```bash
python manage.py startapp nom-projet
```
## Créer un super-uitilisateur (pour la base de donnée)
```bash
python manage.py createsuperuser
```

## Effectuer les migrations

- ``` python manage.py makemigrations```
- ``` python manage.py migrate ```