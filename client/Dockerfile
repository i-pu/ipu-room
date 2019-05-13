FROM node:8.11.3-alpine as dev
# FROM cypress/browsers:node8.9.3-chrome73
WORKDIR /app
RUN apk update && \
    yarn global add @vue/cli
# RUN vue create -d app && \
#    cd app
COPY package.json .
RUN yarn install
COPY . .
CMD ["yarn", "serve"]

FROM node:8.11.3-alpine as build
ENV API_ORIGIN http://35.187.206.173:31420
WORKDIR /app
RUN apk update && \
    yarn global add @vue/cli
COPY package.json .
RUN yarn install
COPY . .
CMD ["sed", "-i", "-e", "'/^VUE_APP_API_ORIGIN/s/=.*$/=${API_ORIGIN}/'", ".env.production"]
CMD ["yarn", "build"]