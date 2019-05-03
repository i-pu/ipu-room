FROM node:8.11.3-alpine
# FROM cypress/browsers:node8.9.3-chrome73

WORKDIR /

RUN apk update && \
    yarn global add @vue/cli

RUN vue create -d app
RUN cd app
COPY package.json .
RUN yarn install
COPY . .
CMD ["yarn", "serve"]