# IPU-ROOM (仮称)
[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu) (大嘘)

## Change Logs

## Document
Docs deployed at [here](https://i-pu.github.io/ipu/index.html) 🎉🎉🎉 

way to routing of github-pages, see <https://github.blog/2016-12-05-relative-links-for-github-pages/>

## Deploy
http://35.247.18.78:31421  
[google kubernetes engine](https://cloud.google.com/kubernetes-engine/)
### client
#### push
tag: client-cd

### web-socket-server
#### push
tag: web-socket-server-cd

## local development
### run client
```
cd client && docker-compose up --build
```

### server-side
デプロイする前にデータベースのConfigMapを更新する必要がある(煩雑)  
`database-config.yaml`  
デプロイ


### Memo
using modified `typedoc-markdown-plugin` to generate client document
because jekyll doesn't recognize files starts with '_'.

### client/node_modules/typedoc-plugin-markdown/dist/theme/index.js#L51
```js
- return [mapping.directory, DefaultTheme_1.DefaultTheme.getUrl(reflection) + '.md'].join('/');
+ return [mapping.directory, DefaultTheme_1.DefaultTheme.getUrl(reflection).slice(1) + '.md'].join('/');
```
