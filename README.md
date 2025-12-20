# Application TODO List - Full Stack avec CI/CD 

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)

## Table des matières
- [Description](#description)
- [Architecture](#architecture)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Pipeline CI/CD](#pipeline-cicd)
- [Structure du projet](#structure-du-projet)


## Description

Cette application est une **TODO List full-stack** moderne qui démontre l'intégration complète d'un workflow de développement professionnel avec :

- **Frontend React** interactif et responsive
- **API REST Flask** robuste et sécurisée
- **Base de données MongoDB** pour la persistance des données
- **Conteneurisation Docker** pour un déploiement simplifié
- **Pipeline CI/CD Jenkins** pour l'automatisation complète
- **HashiCorp Vault** pour la gestion sécurisée des secrets
- **Déploiement sur Docker Hub** pour la distribution

### Objectifs du projet

Ce projet illustre les compétences suivantes :
1. **Développement Full-Stack** : Maîtrise de React, Flask et MongoDB
2. **DevOps** : Conteneurisation avec Docker et orchestration avec Docker Compose
3. **CI/CD** : Automatisation des builds, tests et déploiements avec Jenkins
4. **Sécurité** : Gestion des secrets avec HashiCorp Vault
5. **Gestion de version** : Utilisation de Git et GitHub
6. **Bonnes pratiques** : Code propre, architecture modulaire, sécurité

## Architecture

### Architecture globale

```
┌─────────────────────────────────────────────────────────────┐
│                      ARCHITECTURE GLOBALE                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│   Frontend   │   HTTP   │   Backend    │   CRUD   │   MongoDB    │
│              │  <-----> │              │  <-----> │              │
│  React:3000  │  REST    │  Flask:5000  │  Query   │   Port:27017 │
└──────────────┘   API    └──────────────┘          └──────────────┘
      │                           │                         │
      │                           │                         │
      │                    ┌──────▼───────┐                │
      │                    │    Vault     │                │
      │                    │   :8200      │                │
      │                    └──────────────┘                │
      │                      Secrets:                      │
      │                      - MongoDB credentials         │
      │                      - Docker Hub token            │
      │                      - GitHub token                │
      │                                                     │
      └──────────────────────┬──────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   Docker Network │
                    │   (Bridge Mode)  │
                    └──────────────────┘
```

### Flux de données

1. **User** → Interaction avec l'interface React
2. **React** → Envoie requête HTTP à l'API Flask
3. **Flask** → Récupère les credentials depuis Vault
4. **Flask** → Communique avec MongoDB de manière sécurisée
5. **MongoDB** → Stocke/récupère les données
6. **Flask** → Renvoie la réponse JSON à React
7. **React** → Affiche les données à l'utilisateur

## Technologies utilisées

### Frontend
- **React.js 17+** - Bibliothèque JavaScript pour l'interface utilisateur
- **Axios** - Client HTTP pour les appels API
- **Bootstrap** - Framework CSS pour le design responsive
- **Yarn** - Gestionnaire de paquets

### Backend
- **Flask 2.0.3** - Micro-framework Python pour l'API REST
- **Flask-PyMongo** - Extension pour l'intégration MongoDB
- **Flask-CORS** - Gestion des requêtes cross-origin
- **Gunicorn** - Serveur WSGI de production


### Base de données
- **MongoDB 4.4** - Base de données NoSQL orientée documents


### DevOps
- **Docker** - Conteneurisation des services
- **Docker Compose** - Orchestration multi-conteneurs
- **Jenkins** - Automatisation CI/CD
- **Git/GitHub** - Contrôle de version


## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29+)
- [Git](https://git-scm.com/downloads)
- [Node.js](https://nodejs.org/) (version 14+) - optionnel pour dev local
- [Python](https://www.python.org/) (version 3.8+) - optionnel pour dev local

### Vérification des installations

```bash
docker --version          # Docker version 20.10.x
docker-compose --version  # docker-compose version 1.29.x
git --version            # git version 2.x.x
```

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/Assia-Elguerch/react-flask-mongodb-app.git
cd react-flask-mongodb-app
```

### 2. Rendre le script Vault exécutable

```bash
chmod +x vault-init.sh
```

### 3. Configurer les secrets Vault

Éditez `vault-init.sh` et remplacez les valeurs par défaut :

```bash
# Remplacer ces valeurs
YOUR_DOCKERHUB_USERNAME    # Votre username Docker Hub
YOUR_DOCKER_ACCESS_TOKEN   # Token d'accès Docker Hub
YOUR_GITHUB_PERSONAL_ACCESS_TOKEN  # Token GitHub
YOUR_GITHUB_USERNAME       # Votre username GitHub
```

### 4. Lancer l'application 

```bash
# Arrêter les anciens conteneurs
docker-compose down -v

# Démarrer tous les services 
docker-compose up -d

# Vérifier que tous les conteneurs sont actifs
docker-compose ps
```

```
### 6. Accéder aux interfaces

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000/api/tasks
- **MongoDB** : localhost:27017

## Utilisation

### Commandes Docker principales

```bash
# Démarrer l'application
docker-compose up

# Démarrer en arrière-plan
docker-compose up -d

# Arrêter l'application
docker-compose down

# Reconstruire les images
docker-compose up --build

# Voir les logs en temps réel
docker-compose logs -f api


# Supprimer tous les conteneurs et volumes
docker-compose down -v
```

### Tester l'API manuellement

```bash
# GET - Récupérer toutes les tâches
curl http://localhost:5000/api/tasks

# POST - Ajouter une tâche
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{"title": "Ma nouvelle tâche"}'

# PUT - Modifier une tâche
curl -X PUT http://localhost:5000/api/task/TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"title": "Tâche modifiée"}'

# DELETE - Supprimer une tâche
curl -X DELETE http://localhost:5000/api/task/TASK_ID

# Health check avec statut Vault
curl http://localhost:5000/api/health
```

### Accéder à MongoDB

```bash
# Entrer dans le conteneur MongoDB
docker exec -it mongo bash

# Se connecter à MongoDB
mongosh -u assia -p test --authenticationDatabase admin

# Voir les bases de données
show dbs

# Utiliser la base flaskdb
use flaskdb

# Voir les collections
show collections

# Voir les tâches
db.tasks.find().pretty()
```




## Pipeline CI/CD

### Workflow Jenkins avec Vault a ajouter pour DevSecOps

Le pipeline Jenkins automatise entièrement le processus de déploiement avec sécurité Vault :

```
┌──────────────────┐
│  1. Setup Vault  │  Installation Vault CLI
└────────┬─────────┘
         │
┌────────▼─────────┐
│  2. Get Secrets  │  Récupération des credentials depuis Vault
└────────┬─────────┘  - Docker Hub token
         │            - MongoDB credentials
         │            - GitHub token
┌────────▼─────────┐
│   3. Checkout    │  Clone du code depuis GitHub
└────────┬─────────┘
         │
┌────────▼─────────┐
│   4. Build       │  Construction des images Docker
└────────┬─────────┘  - Frontend (React)
         │            - Backend (Flask)
┌────────▼─────────┐
│   5. Test        │  Lancement et test de l'application
└────────┬─────────┘  - docker-compose up
         │            - Test API avec Vault
┌────────▼─────────┐
│   6. Push        │  Publication sur Docker Hub
└────────┬─────────┘  - Authentification par token Vault
         │            - sia21/react-frontend:latest
         │            - sia21/flask-backend:latest
┌────────▼─────────┐
│   7. Tag         │  Tag des images avec numéro de build
└────────┬─────────┘
         │
┌────────▼─────────┐
│   8. Cleanup     │  Nettoyage sécurisé
└──────────────────┘  - Suppression des fichiers .env
                      - Logout Docker
```

### Étapes du pipeline (Jenkinsfile)

1. **Setup Vault CLI** : Installation de l'outil Vault
2. **Get Secrets from Vault** : Récupération sécurisée des credentials
3. **Checkout** : Clone le repository GitHub
4. **Build Images** : Construction des images Docker
5. **Test & Run Locally** : Lance et teste l'application avec Vault
6. **Push to Docker Hub** : Publie les images avec token Vault
7. **Tag Images** : Tag avec numéro de build
8. **Cleanup** : Nettoyage sécurisé (suppression .env, logout)

### Configuration Jenkins

#### 1. Installer Jenkins avec Docker

```bash
docker run -d \
  --name jenkins \
  --network host \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

#### 2. Installer les plugins nécessaires

Dans Jenkins : **Manage Jenkins** → **Manage Plugins** → **Available**
- Docker Pipeline
- GitHub Integration
- Pipeline

#### 3. Créer les credentials

**Manage Jenkins** → **Manage Credentials** → **Add Credentials**



**Credential 2 : Docker Hub (optionnel, fallback)**
- Kind: Username with password
- Username: votre username
- Password: votre password
- ID: `docker_hub`

#### 4. Créer le pipeline

1. Nouveau Job → Pipeline
2. Nom: `react-flask-mongodb-pipeline`
3. Pipeline script from SCM
4. SCM: Git
5. Repository URL: `https://github.com/Assia-Elguerch/react-flask-mongodb-app.git`
6. Branch: `*/main`
7. Script Path: `Jenkinsfile`

## Structure du projet

```
react-flask-mongodb-app/
│
├── frontend/                  # Application React
│   ├── public/               # Fichiers publics
│   ├── src/
│   │   ├── App.js           # Composant principal
│   │   ├── List.js          # Composant liste de tâches
│   │   └── ListFunctions.js # Fonctions API
│   ├── Dockerfile           # Image Docker frontend
│   └── package.json         # Dépendances Node.js
│
├── backend/                   # API Flask
│   ├── app.py               # Application Flask avec Vault
│   ├── requirements.txt     # Dépendances Python (incluant hvac)
│   └── Dockerfile           # Image Docker backend
│
├── vault-init.sh             # Script d'initialisation Vault a ajouer pour DevSecOps
├── docker-compose.yml        # Orchestration (incluant Vault)
├── Jenkinsfile              # Pipeline CI/CD avec Vault
├── .gitignore               # Fichiers à ignorer
└── README.md                # Ce fichier
```


### Base URL
```
http://localhost:5000/api
```


### Bonnes pratiques implémentées

- **Vault pour les secrets DEVSECOPS** : Tous les credentials stockés de manière chiffrée
- **Token-based authentication** : Pas de mots de passe en clair
- **CORS configuré** : Protection contre les requêtes cross-origin malveillantes
- **Authentification MongoDB** : Base de données protégée
- **Network isolation** : Séparation des réseaux frontend/backend
- **Audit logging** : Vault log tous les accès aux secrets
- **No secrets in code** : Aucun credential dans le code source
- **Environment variables** : Configuration via variables d'environnement

### Comparaison : Avant DEVOPS / Après Vault DEVSECOPS

| Aspect | Sans Vault | Avec Vault |
|--------|------------|------------|
| **Stockage des secrets** | Fichiers en clair | Chiffrés dans Vault |
| **Rotation des secrets** | Manuelle et risquée | Automatisable |
| **Audit** | Aucun | Logs complets |
| **Révocation** | Difficile | Immédiate |
| **Accès** | Tout le monde | Contrôlé par token |
| **Sécurité** | Faible | Élevée |


