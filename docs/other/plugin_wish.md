# プラグイン(に限らず)構想
## 図
```
[ Plugin Frontend (JS or TS) ] [ Frontend (Vue) ]
   ↑   socket  ↓
[ Backend Interface (Python) ] [ Http Server (Rust) ]
   ↑ js, html       ↓ ipl
[ Backend Plugin Compiler API (node.js) ]
```

## 提案
* マーケット, 部屋 GraphQLはどうですか？
* ストアとプラグインコンパイラをマイクロサービス(APIで疎結合)

## Plugin Event Lifecycle
```
[ Compile ]
|
[ Initialize ]
|
[  ]
```

## TODO
* ストアのプラグインデモはローカル動作に
* 

## 大富豪プラグイン
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