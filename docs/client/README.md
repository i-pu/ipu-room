
IPU-ROOM (仮称)
=============

[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu) (大嘘)

Change Logs
-----------

Document
--------

Docs deployed at [here](https://i-pu.github.io/ipu/index.html) 🎉🎉🎉

way to routing of github-pages, see [https://github.blog/2016-12-05-relative-links-for-github-pages/](https://github.blog/2016-12-05-relative-links-for-github-pages/)

Deploy
------

[http://35.247.18.78:31421](http://35.247.18.78:31421)  
[google kubernetes engine](https://cloud.google.com/kubernetes-engine/)

### client

#### push

tag: client-cd

### web-socket-server

#### push

tag: web-socket-server-cd

local development
-----------------

### run client

```
cd client && docker-compose up --build
```

### server-side

### build

```
docker build -t kafuhamada/web-socket-server web-socket-server/src
docker build -t kafuhamada/database-controller database-controller
```

### run

kubernetes on `minikube`  
not `docker for mac`

### run server

minikube をインストールする必要がある

```bash
$ brew install minikube
$ minikube start --cpus 2 --memory 4096 <- 3,4分かかる
```

localではminikubeとdockerを併用することになるので以下のコマンドを minikube start の後にすべての開いているpromptで実行する

```bash
$ eval $(minikube docker-env)
```

以下のコマンドでdocker build する．これ以外は許されない．

```bash
$ docker build -t kafuhamada/database_controller database_contoroller
$ docker build -t kafuhamada/web-socket-server web-socket-server 
```

デプロイ

```bash
$ ./helm3-alpha init
$ ./helm3-alpha install -f ./helm/server/values.yaml -f ./helm/server/values.local.yaml server ./helm/server
```

終了する際には，

```bash
$ ./helm3-alpha uninstall server
$ minikube stop
```

### Memo

using modified `typedoc-markdown-plugin` to generate client document because jekyll doesn't recognize files starts with '\_'.

### client/node\_modules/typedoc-plugin-markdown/dist/theme/index.js#L51

```js
- return [mapping.directory, DefaultTheme_1.DefaultTheme.getUrl(reflection) + '.md'].join('/');
+ return [mapping.directory, DefaultTheme_1.DefaultTheme.getUrl(reflection).slice(1) + '.md'].join('/');
```

## Index

### External modules

* ["logic/compiler"](modules/logic_compiler_.md)
* ["main"](modules/main_.md)
* ["mock/simple-server"](modules/mock_simple_server_.md)
* ["plugin_examples/chat"](modules/plugin_examples_chat_.md)
* ["plugin_examples/counter"](modules/plugin_examples_counter_.md)
* ["plugin_examples/paint"](modules/plugin_examples_paint_.md)
* ["plugin_examples/player"](modules/plugin_examples_player_.md)
* ["plugins/vuetify"](modules/plugins_vuetify_.md)
* ["router"](modules/router_.md)
* ["store"](modules/store_.md)

---

