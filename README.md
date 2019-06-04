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

## local development
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
localではminikubeとdockerを併用することになるので以下のコマンドを
minikube start の後にすべての開いているpromptで実行する
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

# 目次
- プラグインの構成
  - 概要
  - 構想
  - template部
  - script部
  - アドオン
- プラグインの仕様
  - プラグインパッケージ
  - サーバー側での処理
  - クライアント側での処理
- プラグインの具体例
  - カウンター
  - チャット

## プラグインの構成
### 概要
- `20190514` : スキーマ v1 策定中
- `20190521` : 話し合い中
- `20190521` : スキーマ v2

### 構想 (詳細仕様未定)
* [x] **クライアント側で状態を管理**
* 入室時にメンバーから状態をクローン
* [x] Pluginのサーバー側の return を `{ function_name: string, record: Record<string, any>, to: string }` にする
* [x] `to (default = all)` にソケット通信のレスポンスが返り、クライアント側の `function_name(record)` が呼ばれる
* [ ] `plugin/event` で切断イベントとかをフックしたい

### template部
* `Vue` テンプレートとして記述
* `Vuetify` や独自コンポーネント (`アドオン`) で装飾可能

### script部
* `Javascript function` として記述
* `EMIT <function_name>` 時に呼ばれる

## プラグインの仕様
### プラグインパッケージ
 [#48](https://github.com/i-pu/ipu/issues/48) 参照

### モデル
#### Plugin
プラグインの本体
```ts
export interface Plugin {
  // html template
  template: string,
  // functions
  functions: Record<string, string[]>
}
```

#### PluginMeta
プラグインの名前等の静的な情報
```ts
// static plugin info
export interface PluginMeta {
  // id
  id: string,
  // plugin name
  thumbnail_url: string,
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}
```
#### PluginObject
プラグインのインスタンスID等の環境情報
```ts
// instance info
export interface PluginProperties {
  // instantiate at client side
  record: Record<string, any>,
  env: {
    instanceId: string,
    room: Room
  },
  meta: PluginMeta
}
```

### ペイロード
#### `plugin/register`
```ts
{
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string,
}
```

#### REQ `room/enter`
```ts
{
  room_id: string
}
```

#### RES `room/enter`
```ts
{
  room: Room
}
```

#### REQ `plugin/info`
```ts
{
  room_id: string
}
```

#### RES `plugin/info`
```ts
{ 
  plugin: Plugin,
  properties: PluginProperties
}[]
```

#### REQ `plugin/clone`
```ts
{

}
```

#### RES `plugin/clone`
```
{
  plugins: Array<{ plugin: Plugin, properties: PluginProperties }>
}
```

#### REQ `plugin/trigger`
```ts
{
  room_id: string,
  instance_id: string,
  event_name: string,
  args: any[]
}
```

#### RES `plugin/trigger`
```ts
{
  function_name: string,
  args: any[],
}
```

### サーバー側での処理
* プラグインはサーバー側で解析され `template`, `records`, `events`, `addons`, `python` の5つに分けられる.
* `ON plugin/trigger` でメソッドを動的に呼び出し後、プラグイン内変数の変更を検知し `EMIT plugin/trigger` する.

### クライアント側での処理
* `v-onイベント` に対し、ソケット通信の処理をオーバーラップしている

## プラグインの具体例
### カウンター
#### counter.ipl
```html
<html>
  <div>
    <h3> {{ record.count }} </h3>
    <v-btn @click="plus(1)"> Add </v-btn>
  </div>
</html>
<script>
initialize () {
  return {
    count: 0
  }
}

plus() {
  this.record.count++
}
</script>
```

### チャット
#### chat.ipl
```html
<html>
  <div>
    <v-list id="chat" two-line="two-line" height="50%">
      <v-subheader>チャット</v-subheader>
      <template v-for="comment, i in record.comments">
        <v-list-tile v-if="comment.type === 'comment'" :key="comment.comment_id" avatar="avatar">
          <v-list-tile-avatar>
            <img :src="comment.avatar"/>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ comment.text }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ comment.user_name }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </template>
    </v-list>

    <v-container fluid="fluid" grid-list-md="grid-list-md" text-xs-center="text-xs-center">
      <v-layout row="row" wrap="wrap">
        <v-flex d-flex="d-flex" xs8="xs8" sm8="sm8" md8="md8">
          <v-text-field v-model="record.chatInput" label="コメント"></v-text-field>
        </v-flex>
        <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
          <v-btn color="info" @click="comment(); record.chatInput = ''">送信</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</html>
<script>
initializer () {
  return {
    comments: [],
    chatInput: ''
  }
}

comment () {
  this.record.comments.push({
    type: 'comment',
    avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
    comment_id: 'a',
    user_name: 'John',
    user_id: 'xxxx',
    text: this.record.chatInput
  })
}
</script>
```
