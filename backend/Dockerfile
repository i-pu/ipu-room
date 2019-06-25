FROM node:10.15-alpine as builder
COPY package.json ./
COPY src/ src/
COPY tsconfig.json ./
RUN npm install

FROM alpine:3.9
ADD package.json .
COPY --from=builder dist/bundle.min.js dist/bundle.min.js
RUN apk update && ``\
    apk add nodejs nodejs-npm
CMD [ "npm", "start" ]