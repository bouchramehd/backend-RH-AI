# Smart HR – Plateforme d’Analyse de CV avec IA

Ce document présente une **application RH intelligente** développée avec **Django** et intégrant une IA via **Ollama** pour analyser les CV, extraire automatiquement le contenu et générer un score de pertinence.

Ce README aide votre équipe à comprendre :

* la structure du projet
* les fonctionnalités
* le fonctionnement de l’IA
* comment lancer et tester l’application

---

## 🚀 Fonctionnalités principales

### 🔹 1. Rôles utilisateurs

* **Admin** – accès complet via `/admin/`
* **Recruteur** – peut consulter toutes les offres et candidatures
* **Candidat** – peut postuler et envoyer son CV

### 🔹 2. Gestion des offres d’emploi

* Création, modification, suppression d’offres
* Activation / désactivation
* Lien direct avec les candidatures

### 🔹 3. Candidatures (upload CV)

Chaque candidature contient :

* Fichier CV en **PDF**
* Lettre de motivation
* Poste visé
* Candidat associé
* Score généré par l’IA (0–100)
* Statut (`new`, `in_review`, `accepted`, `rejected`)

### 🔹 4. Analyse IA (Ollama)

L’IA effectue :

1. Extraction du texte du CV (PDF)
2. Lecture de la description du poste
3. Analyse de pertinence
4. Retourne un **score entre 0 et 100**
5. Enregistre automatiquement le résultat

### 🔹 5. API sécurisée (Django REST Framework)

* Authentification obligatoire
* Candidat : ne voit que ses propres candidatures
* Recruteur / admin : voient toutes les candidatures
* Upload de CV via l’API

---

## 🏗️ Structure du projet

```
projetRH/
│
├── smart_hr/               # Configuration Django
├── accounts/               # Utilisateurs + rôles
├── candidates/             # Offres + candidatures (API)
├── ml_app/                 # IA : extraction PDF + scoring Ollama
├── notifications/          # (à venir : emails, alertes)
├── dashboard/              # (à venir : statistiques)
└── manage.py
```

---

## 🔧 Installation et configuration

### 1. Créer un environnement virtuel

```
python -m venv venv
venv/Scripts/activate
```

### 2. Installer les dépendances

```
pip install django djangorestframework pypdf requests python-dotenv
pip install psycopg2-binary
```

### 3. Migrer la base de données

```
python manage.py makemigrations
python manage.py migrate
```

### 4. Lancer le serveur Django

```
python manage.py runserver
```

Accéder à :
`http://127.0.0.1:8000/admin/`

Créer un superuser si besoin :

```
python manage.py createsuperuser
```

---

## 🤖 Installation d’Ollama

1. Télécharger Ollama :
   [https://ollama.com](https://ollama.com)

2. Installer un modèle IA :

```
ollama pull llama3
```

3. Lancer Ollama :

```
ollama serve
```

---

## 🧠 Fonctionnement du scoring IA

Le cœur de l’analyse se trouve dans :

```
ml_app/ollama_service.py
```

L’IA :

* lit le PDF
* extrait le texte
* compare au poste
* génère un score
* renvoie une valeur 0–100

---

## 🔥 Paramètres importants (API & sécurité)

Dans `settings.py` :

```
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

➡️ Cela garantit que seule une personne **connectée** peut utiliser l’API.

---

## 📡 Endpoints API

### Offres d’emploi

* `GET /api/candidates/offers/` – liste
* `POST /api/candidates/offers/` – création
* `GET /api/candidates/offers/<id>/` – détail

### Candidatures

* `GET /api/candidates/applications/` – liste personnalisée
* `POST /api/candidates/applications/` – envoi d’un CV

Le POST accepte :

* `job` (ID)
* `cv_file` (PDF)
* `cover_letter` (texte)

---

## 🧑‍💻 Rôles et permissions

### Admin

* Accès total
* Gestion utilisateurs / offres / candidatures

### Recruteur

* Peut voir toutes les candidatures
* Peut voir tous les scores

### Candidat

* Ne peut voir que **ses propres candidatures**
* Peut postuler et envoyer un CV

---

## 🧪 Tester le système

1. Aller dans `/admin` et créer une **offre**
2. Aller dans `/api/candidates/applications/`
3. Upload un CV PDF
4. Soumettre
5. Aller dans `/admin/candidates/application/`
6. Vérifier le score et le statut

---

## 🗺️ Améliorations futures

* Tableau de bord recruteur (graphiques)
* Extraction avancée de compétences
* Optimisation du prompt d’analyse
* Ajout d’une interface web dédiée (React ou Bootstrap)
* Déploiement Docker (Django + Ollama)

---

## 👥 Notes pour l’équipe

* `Admin` ≠ compte séparé → c’est un utilisateur avec droits avancés
* Ollama doit être lancé pour que l’analyse fonctionne
* Les candidats ne voient que leurs candidatures
* L’API ne fonctionne que si l’utilisateur est connecté

