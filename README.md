# Commandes pour Django

## Installer l'environnement et l'activer

- ``` python -m venv env```
- ``` env/Scripts/activate.bat```

## Installer Django
```bash
pip install django
```

## Ajouter un projet
```bash
python manage.py startapp nom-projet
```

## Démarrer le serveur
```bash
python manage.py runserver
```

## Créer un super-uitilisateur (pour la base de donnée)
```bash
python manage.py createsuperuser
```

## Effectuer les migrations

- ``` python manage.py makemigrations```
- ``` python manage.py migrate ```