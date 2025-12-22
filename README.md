# 📝 TODO List Full-Stack avec CI/CD

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)

---

## 🚀 Description

Cette application est une **TODO List full-stack** moderne qui illustre :  

- **Frontend React** interactif et responsive  
- **API REST Flask** robuste et sécurisée  
- **Base de données MongoDB** pour la persistance  
- **Conteneurisation Docker** pour un déploiement simplifié  
- **Pipeline CI/CD Jenkins** pour automatiser build, test et déploiement  

> ⚠️ Actuellement, la gestion des secrets est réalisée via des variables d’environnement et des fichiers de configuration. L’intégration de **HashiCorp Vault** est prévue comme amélioration DevSecOps pour sécuriser les credentials et améliorer l’audit.

---

## 🏗️ Architecture

### Architecture globale

````bash
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Frontend    │  HTTP │   Backend    │  CRUD │   MongoDB    │
│  React:3000  │ <---->│  Flask:5000  │ <---->│  Port:27017  │
└──────────────┘       └──────────────┘       └──────────────┘
````

### Flux de données

1. L’utilisateur interagit avec l’interface React  
2. React envoie des requêtes HTTP à l’API Flask  
3. Flask interagit avec MongoDB pour stocker/récupérer les données  
4. La réponse JSON est renvoyée à React et affichée  

---

## 🛠️ Technologies utilisées

**Frontend** : React.js, Axios, Bootstrap, Yarn  
**Backend** : Flask, Flask-PyMongo, Flask-CORS, Gunicorn  
**Base de données** : MongoDB  
**DevOps / CI/CD** : Docker, Docker Compose, Jenkins  
**Versioning** : Git & GitHub  

---

## ⚙️ Prérequis

- Docker 20.10+  
- Docker Compose 1.29+  
- Git 2.x  
- Node.js 14+ (optionnel pour dev local)  
- Python 3.8+ (optionnel pour dev local)  

```bash
docker --version
docker-compose --version
git --version
````

## 📝 Installation

# Cloner le repository
```bash
git clone https://github.com/Assia-Elguerch/react-flask-mongodb-app.git
cd react-flask-mongodb-app
````
# Arrêter les anciens conteneurs
```bash
docker-compose down -v
````
# Démarrer l'application
```bash
docker-compose up -d
````
# Vérifier les conteneurs
```bash
docker-compose ps
````


## 🌐 Accès aux interfaces

- **Frontend** : [http://localhost:3000](http://localhost:3000)  
- **Backend API** : [http://localhost:5000/api/tasks](http://localhost:5000/api/tasks)  
- **MongoDB** : localhost:27017  

---

## 🖥️ Utilisation

### Commandes Docker principales

```bash
docker-compose up          # Démarrer l'application
docker-compose up -d       # Démarrer en arrière-plan
docker-compose down        # Arrêter
docker-compose up --build  # Rebuild images
docker-compose logs -f api # Voir logs
docker-compose down -v     # Supprimer conteneurs et volumes
````

Tester l’API manuellement
# GET toutes les tâches
```bash
curl http://localhost:5000/api/tasks
````
# POST nouvelle tâche
```bash
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{"title": "Ma nouvelle tâche"}'
````
# PUT modifier tâche
```bash
curl -X PUT http://localhost:5000/api/task/TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"title": "Tâche modifiée"}'
````
# DELETE supprimer tâche
```bash
curl -X DELETE http://localhost:5000/api/task/TASK_ID
````
## 🧩 Pipeline CI/CD

# Le pipeline Jenkins automatise :

- Checkout du code depuis GitHub

- Build des images Docker (frontend & backend)

- Tests de l’application

- Push vers Docker Hub

- Tag des images

## ℹ️ Informations
>  Les étapes de Vault / DevSecOps sont documentées comme perspectives futures pour sécuriser les credentials et améliorer l’audit.

📂 Structure du projet

````bash
react-flask-mongodb-app/
│
├── frontend/                  # React app
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── List.js
│   │   └── ListFunctions.js
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── Jenkinsfile
├── .gitignore
└── README.md
````
## 🔒 Perspectives DevSecOps

- Vault pour la gestion des secrets (MongoDB, Docker Hub, GitHub)

- Rotation automatique des secrets

- Audit complet des accès

- Accès contrôlé par token

---

## ℹ️ Informations

> Actuellement, le projet fonctionne sans Vault, mais cette amélioration est prévue pour sécuriser les credentials et rendre le pipeline CI/CD plus robuste.


## 🌐 Base URL
http://localhost:5000/api


Realisé par assia el guerch

