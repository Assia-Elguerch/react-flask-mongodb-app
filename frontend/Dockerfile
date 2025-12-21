FROM node:18
WORKDIR /app
# Copier les fichiers de gestion des dépendances
COPY package*.json ./
# Installer les dépendances
RUN npm ci --only=production || npm install
# Copier tout le code source
COPY . .
# Exposer le port
EXPOSE 3000
# Démarrer l'application
CMD ["npm", "start"]