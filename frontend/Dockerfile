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
# Variable d'environnement pour React - API en Docker utilise le hostname 'api'
ENV NODE_ENV=production
ENV REACT_APP_API_URL=http://api:5000
# Démarrer l'application
CMD ["npm", "start"]