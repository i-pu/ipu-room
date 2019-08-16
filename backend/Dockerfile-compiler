FROM node:10.15-alpine as builder
COPY package.json ./
COPY src/ src/
COPY tsconfig.json ./
RUN npm install

RUN apk update && \
    apk add nodejs nodejs-npm
CMD [ "npm", "start" ]