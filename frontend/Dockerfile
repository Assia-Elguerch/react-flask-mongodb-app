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

# Variable d'environnement pour React
ENV NODE_ENV=production

# Démarrer l'application
CMD ["npm", "start"]