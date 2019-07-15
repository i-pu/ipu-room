## プラグインのコンパイル [/api/v1/plugin/load/{id}]
 
### プラグインコンパイラAPI [GET]
 
#### 処理概要
 
* プラグインIDが `id` のプラグインをコンパイルし, `PluginPackage` を返却します
 
+ Parameters
    + id: 85826f18-3bc9-4cb7-ab6b-27d9e8a016ee (string, required) - プラグインの `id`
 
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
    + (object)
        + enabled: true (boolean) - プラグインが有効かどうか