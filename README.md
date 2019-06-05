# IPU-ROOM (仮称)
[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu) (大嘘)

## Change Logs

## Document
(準備中)

## Deploy
http://35.247.18.78:31421  
[google kubernetes engine](https://cloud.google.com/kubernetes-engine/)
### client
#### push
tag: client-cd

### web-socket-server
#### push
tag: web-socket-server-cd

## Development
### run client
```
cd client && docker-compose up --build
```

### run web-socket-server
```
cd server && docker-compose up --build
```

### run plugin_market
あらかじめ `diesel_cli` をインストールする必要がある
```bash
// diesel cli インストール
cargo install diesel_cli --no-default-features --features postgres

```
diesel_cliがインストールされている状態で
```bash
cd plugin_market
./setup.local.sh
```
サーバ動かすときは `cargo run` 
8888をバインドしてる
`ctr-c`で止める
```bash
// 終わるときは
./teardown.local.sh
```
