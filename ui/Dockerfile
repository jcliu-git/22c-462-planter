FROM node:16-alpine

WORKDIR /ui

#Install bash
RUN apk update && apk add bash

#Install node dependencies 
COPY package*.json ./
RUN npm i

COPY . .

EXPOSE 3000

#  Give permission to wait-for-it.sh - This is to make sure db is ready before connecting to it
RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "db:5432", "--", "npm", "run", "dev"]