
FROM node:18

WORKDIR /app

COPY . .

RUN yarn

RUN yarn global add serve

#CMD [ "serve" , "-p" , "80" , "-s" , "."]

# expose locally the app

CMD [ "yarn" , "start"]

