FROM node:8.11.3-alpine

WORKDIR /app

RUN apk update && \
    npm install -g npm && \
    npm install @vue/cli

COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "serve"]