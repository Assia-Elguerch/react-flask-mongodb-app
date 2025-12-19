FROM node:18

WORKDIR /app

# Copier les fichiers de dépendances
COPY package.json yarn.lock ./

# Installer les dépendances
RUN yarn install --frozen-lockfile

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 3000

# Démarrer l'application
CMD ["yarn", "start"]