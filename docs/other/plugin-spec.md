# プラグイン仕様 
v2019.6.5

# 構成
* 単一ファイルに記述、拡張子は`*.ipl`

## `<template>` 部
* Vueテンプレート
* Vuetifyのコンポーネントが使用可能
* アンダーバーから始まるメソッド名はソケットを介さず直接メソッドを呼ぶ

## `<script>` 部
* プラグインで使用されるメソッドを `export default` する
* `this.env` でメタ情報が取得できる
* `this.$send`
# 例 - カウンター
### counter.ipl
```html
<template>
  <div>
    <h3> {{ record.count }} </h3>
    <v-btn @click="plus"> Add </v-btn>
  </div>
</template>
<script>
export default {
  initialize () {
    return {
      count: 0
    }
  },
  plus() {
    this.record.count++
  }
}
</script>
```

### コンパイル後(サーバーから送られてくるもの)
```js
{
  plugin: {
    template: `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
    functions: {
      initialize: ['return { count: 0 }'],
      plus: ['this.record.count++']
    },
    instanceId: 'd7bd1c2e-8d90-4b32-acd5-ff4568a72c74'
  },
  meta: {
    id: 'counter_xxx',
    // plugin name
    name: 'counter',
    thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    description: 'aaa',
    author: 'a',
    tags: 'a,b,c',
    content: '<html></html>'
  }
}
```

# 例 - ペイント
### paint.ipl
```html
<template>
  <div>
    <vue-p5 
      @setup="_setup" 
      @draw="_draw" 
      @mousedragged="_addLine" 
    />
  </div>
</template>
<script>
export default {
  initialize () {
    return { lines: [], line: {} }
  },
  onDraw (p) {
    this.record.lines.push({ x: p.x, y: p.y, px: p.px, py: p.py })
  },
  _setup (sketch) {
    console.log('set up')
    sketch.createCanvas(600, 600)
  },
  _draw (sketch) {
    for (let line of this.record.lines) {
      sketch.line(line.px, line.py, line.x, line.y)
    }
  },
  _addLine (p) {
    this.record.line = { x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY }
    this.$send('onDraw', this.record.line)
  }
}
</script>
```
### コンパイル後
```js
{
  plugin: {
    template: `<div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_addLine"></vue-p5></div>`,
    functions: {
      initialize: ['return { lines: [], line: {} }'],
      _setup: ['sketch', `
        console.log('set up')
        sketch.createCanvas(600, 600)
      `],
      _draw: ['sketch', `
        for (let line of this.record.lines) {
          sketch.line(line.px, line.py, line.x, line.y)
        }
      `],
      _addLine: ['p', `
        this.record.line = { x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY }
        this.$send('onDraw', this.record.line)
      `],
      onDraw: ['p', `
        this.record.lines.push({ x: p.x, y: p.y, px: p.px, py: p.py })
      `],
    }
  },
  meta: {
    plugin_id: 'counter_xxx',
    // plugin name
    name: 'counter',
    thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    description: 'aaa',
    author: 'a',
    tags: 'a,b,c',
    content: '<html>...</html>',
  }
}
```

# 展望
* プラグイン内アドオン
* 複数ファイルに対応
* イベントフックの対応(誰かが退室した時に`onLeave()`が呼ばれるみたいな)
* コメントが流れるチャットプラグイン作りたい
* 大富豪プラグインつくりたい
* みんなでYoutubeみれるプラグインつくりたい