FROM node:18

WORKDIR /app

# Copier package.json et yarn.lock pour installer les dépendances
COPY package*.json ./

# Installer les dépendances
RUN yarn install

# Copier tout le projet
COPY . .

# Build de l'application React
RUN yarn build

# Installer 'serve' pour servir le build
RUN yarn global add serve

# Servir la version buildée
CMD ["serve", "-s", "build", "-l", "3000"]


