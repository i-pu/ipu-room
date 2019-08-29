# Plugin
## 目標
一つのファイルでサーバーサイドの処理とクライアントサイドの処理をかけるようにしたい

## モデル
```ts
// =========================
// index.d.ts
//
// Copyright (c) 2019 i-pu
// =========================

export interface Plugin {
  template: string,
  functions: string,
  instanceId: string,
  config: {
    enabled: boolean,
  }
}

/**
* Expresses Data of static infomation about a plugin.
* @param id HTML template
* @param thumbnailUrls
* @param content raw script of a plugin
*/
interface PluginMeta {
  id: string,
  version: string,
  thumbnailUrls: string[],
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}

export interface PluginPackage {
  plugin: Plugin,
  meta: PluginMeta,
}

/**
* Room
*/
export interface Room {
  name: string,
  id: string,
  thumbnailUrl: string,
  members: User[],
  pluginPackages: PluginPackage[]
}

/**
* User
*/
export interface User {
  name: string,
  id: string,
  avatarUrl: string
}


```

## アーキテクチャ
```
[ Plugin Frontend (JS or TS) ] [ Frontend (Vue) ]
   ↑   socket  ↓
[ Backend Interface (Python) ] [ Http Server (Rust) ]
   ↑ js, html       ↓ ipl
[ Backend Plugin Compiler API (node.js) ]
```

## ライフサイクル
```
[ Compile ]
|
[ Load ]
|
[ Initialize ]
```

## 例:大富豪プラグイン
```html
<template>
  <div></div>
</template>
<script lang="ts">
import { Deck, Card } from 'playing-cards'
import _ from 'lodash'

@Turnable
class CareerPoker extends Plugin {
  @Inventory
  private deck: Card[]

  constructor () {
    const decks = new Deck(52).distribute(4)
    for (const [player, deck] of _.zip(decks, this.$players)) {
      player.$send('deck', deck)
    }
  }

  deck (deck: Card[]) {
    this.deck = deck
  }

  @Hook('turn')
  private myTurn () {

  }
}
</script>

```
