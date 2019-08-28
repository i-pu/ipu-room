# IPU-ROOM (仮称)
[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu) (大嘘)

[ipu-room](http://34.83.135.173)

## Document
Docs deployed at [here](https://i-pu.github.io/ipu-room/index.html) 🎉🎉🎉 

way to routing of github-pages, see <https://github.blog/2016-12-05-relative-links-for-github-pages/>

## Deploy
### CI
基本的にデプロイはディレクトリ名をbranchとして `push` すれば `ci/cd` 走ります．
```bash
git push origin client
git push origin backend
git push origin web-socket-server
```
### Document
(require `yarn global add now`)

```
$ cd document && now
```

## local development
### run client
```
cd client && docker-compose up --build
```

### server-side
デプロイする前にデータベースのConfigMapを更新する必要がある(煩雑)  
`database-config.yaml`  
デプロイ
