FROM node:8.11.3-alpine

WORKDIR /app

RUN apk update && \
    npm install -g yarn && \
    yarn global add @vue/cli && \
    yarn install

COPY . .
RUN ls -l -a

CMD ["yarn", "serve"]