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

### server
#### push
tag: server-cd

## Development
### run client
```
cd client && docker-compose up --build
```

### run server
```
cd server && docker-compose up --build
```

# 目次
- プラグインの構成
  - 概要
  - template部
  - python部
  - アドオン
- プラグインの仕様
  - プラグインパッケージ
  - サーバー側での処理
  - クライアント側での処理
- プラグインの具体例
  - カウンター
  - チャット
  - Youtubeプレイヤー

## プラグインの構成
### 概要
`20190514` : スキーマ v1 策定中

### template部
* `Vue` テンプレートとして記述
* `Vuetify` や独自コンポーネント (`アドオン`) で装飾可能
* 任意のソケット通信を行うことはできない

### python部
* Pythonクラス `class Plugin()` として記述
* インスタンス内の変数がクライアントと同期される
* `イベント` (ソケット通信)でクライアントとやり取り

### アドオン
* 任意のVueコンポーネントを追加できるようにする予定
* `Vuetify` コンポーネント等を動的に読み込めるようにしたい

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
  // trigger functions' name
  funtions: string[],
  // custom component that be used in
  addons: Record<string, string>
}
```

#### PluginMeta
プラグインの名前等の静的な情報
```ts
// static plugin info
export interface PluginMeta {
  // plugin id
  plugin_id: string,
  // plugin name
  name: string,
  description: string,
  author: string,
  tags: string[],
  content: string
}
```
#### PluginObject
プラグインのインスタンスID等の環境情報
```ts
// instance info
export interface PluginObject {
  room_id: string,
  enabled: boolean,
  // plugin unique instance id
  id: string,
  // variable
  record: Record<string, any>
}
```

### ペイロード
#### `plugin/register`
```ts
{
  name: string,
  description: string,
  author: string,
  tags: string[],
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
  instance: Plugin, 
  meta: PluginMeta, 
  object: PluginObject
}[]
```

#### REQ `plugin/trigger`
```ts
{
  room_id: string,
  instance_id: string,
  function_name: string,
  args: any[]
}
```

#### RES `plugin/trigger`
```ts
{
  record: Record<string, any>,
  function_name: string
}
```

### サーバー側での処理
* プラグインはサーバー側で解析され `template`, `records`, `events`, `addons`, `python` の5つに分けられる.
* `ON plugin/trigger` でメソッドを動的に呼び出し後、プラグイン内変数の変更を検知し `EMIT plugin/trigger` する.

### クライアント側での処理
* `v-onイベント` に対し、ソケット通信の処理をオーバーラップしている

## プラグインの具体例
### カウンター
```html
<html>
  <div>
    <h3> {{ v.count }} </h3>
    <v-btn @click="plus(1)"> Add </v-btn>
  </div>
</html>
<python>
class Plugin():
  def __init__(self):
    self.events = ['plus']
    self.count = 0

  def constructor(self):
    return { 'count': self.count }

  def plus(self, data):
    self.count += data
    return { 'count': self.count }
</python>
```

### チャット
```html
<html>
  <div>
    <v-list id="chat" two-line="two-line" height="50%">
      <v-subheader>チャット</v-subheader>
      <template v-for="comment, i in comments">
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
          <v-text-field v-model="chatInput" label="コメント"></v-text-field>
        </v-flex>
        <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
          <v-btn color="info" @click="comment(chatInput); chatInput = ''">送信</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</html>
<python>
class Plugin():
  def __init__(self):
    self.comments = []
    self.chatInput = ''
  def comment(self, comment_text):
    comment = {
      type: 'comment',
      avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
      comment_id: uuidv4(),
      user_name: 'John',
      user_id: 'xxxx',
      text: comment_text
    }
    self.comments.append(comment)
    return ['comments']
</python>
```

### Youtubeプレイヤー
```html
<html>
  <div>
    <v-btn> Test </v-btn>
    <player :video-id="v.video_id" player-width="1280" player-height="750" :player-vars="{autoplay: 1}" />
  </div>
</html>
<pyhton>
class Plugin():
  def __init__(self):
    self.video_id = 'SX_ViT4Ra7k'
</pyhton>
```
