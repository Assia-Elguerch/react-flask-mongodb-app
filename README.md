# React + Flask + MongoDB Dockerized App



## 🚀 Description

Cette application est un projet full-stack complet utilisant **React** pour le frontend, **Flask** pour le backend et **MongoDB** comme base de données. L’ensemble est entièrement **dockerisé** et automatisé via un **pipeline CI/CD avec Jenkins**, permettant un déploiement rapide et fiable.

### Le projet illustre :
- La création d’une application web moderne full-stack.
- L’utilisation de Docker pour isoler et déployer les services.
- La mise en place d’un pipeline CI/CD pour automatiser les builds, tests et déploiement.
- L’intégration avec GitHub pour la gestion du code source.

---

### 📚 Concepts clés

- CI/CD (Continuous Integration / Continuous Deployment) : Processus d’intégration continue et déploiement continu     - pour automatiser la compilation, les tests et le déploiement.
- Pipeline Jenkins : Script décrivant toutes les étapes d’un workflow automatisé (build, test, deploy).
- Docker : Technologie de conteneurisation qui permet d’isoler et déployer facilement les applications.
- Docker Compose : Outil pour définir et lancer des applications multi-conteneurs.
- MongoDB Volume : Permet de persister les données entre les redémarrages des conteneurs.

---

## 🧩 Technologies utilisées

| Composant | Technologie |
|-----------|------------|
| Frontend  | React.js, Yarn |
| Backend   | Flask, Python 3.8, Gunicorn |
| Base de données | MongoDB 6 |
| Conteneurisation | Docker, Docker Compose |
| CI/CD     | Jenkins Pipeline |
| Contrôle de version | Git, GitHub |

---

## 📦 Architecture du projet

```text
┌───────────┐       ┌────────────┐       ┌─────────────┐
│  Frontend │ <-->  │   Backend  │ <-->  │   MongoDB   │
│ React App │       │ Flask API  │       │ Database    │
└───────────┘       └────────────┘       └─────────────┘

