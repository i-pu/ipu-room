## プラグインのコンパイル [/api/v1/plugin/compile]
 
### プラグインコンパイラAPI [POST]
 
#### 処理概要
 
* JSONで渡された `PluginMeta` をコンパイルし `PluginPackage` を返却します

#### リクエストボディの例
```json
{
  "name": "counter",
  "thumbnailUrls": [
    "https://avatars3.githubusercontent.com/u/50242068?s=200&v=4",
    "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
    "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
    "https://cdn.vuetifyjs.com/images/carousel/bird.jpg"
  ],
  "description": "これはプラグインですこれはプラグインですこれはプラグインです",
  "author": "wakame-tech",
  "version": "v0.1.1",
  "tags": "a,b,c",
  "content": "<template><div><h3> {{ record.count }} </h3><v-btn @click=\"plus\"> Add </v-btn></div></template><script>({initialize () {return {count: 0}},plus() {this.record.count++}})</script>"
}
```

+ Parameters

    なし
 
+ Response 200 (application/json)
 
    + Attributes
        + plugin (Plugin, required)
        + meta (PluginMeta, required)

## Data Structures

### PluginMeta
+ id: '85826f18-3bc9-4cb7-ab6b-27d9e8a016ee' (required, string) - プラグインID
+ thumbnailUrls: 'http://hoge/fuga.png' (required, array[string]) - thumnail url
+ name: Counter (required, string) - 名前
+ description: this is a plugin (required, string) - 説明
+ author: wakame_tech (required, string) - 作者
+ tags: game, default (required, array[string]) - タグ
+ content: `<template> ... </template>` (required, string) - プラグインソース

### Plugin
+ template: `<template> ... </template>` (required, string) - Vueテンプレート
+ functions: `(function () { ... }, ...)` (required, string) - イベント関数
+ instanceId: `85746f18-3ac9-4cbf-ab6b-27ba06d016ee` (required, string) - 固有のインスタンスID
+ config: (required)
    + enabled: true (boolean) - プラグインが有効かどうか