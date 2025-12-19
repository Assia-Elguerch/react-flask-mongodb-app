# React + Flask + MongoDB Dockerized App

![Project Logo](<img width="2048" height="970" alt="image" src="https://github.com/user-attachments/assets/cd078f10-4df4-4169-ae82-4a93fb0c1289" />)

## 🚀 Description

Cette application est un projet full-stack complet utilisant **React** pour le frontend, **Flask** pour le backend et **MongoDB** comme base de données. L’ensemble est entièrement **dockerisé** et automatisé via un **pipeline CI/CD avec Jenkins**, permettant un déploiement rapide et fiable.

Le projet illustre :
- La création d’une application web moderne full-stack.
- L’utilisation de Docker pour isoler et déployer les services.
- La mise en place d’un pipeline CI/CD pour automatiser les builds, tests et déploiement.
- L’intégration avec GitHub pour la gestion du code source.

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
