[Ipu-space](../README.md) > ["plugin_examples/paint"](../modules/plugin_examples_paint_.md)

# External module: "plugin_examples/paint"

## Index

### Object literals

* [meta](plugin_examples_paint_.md#meta)
* [plugin](plugin_examples_paint_.md#plugin)

---

## Object literals

<a id="meta"></a>

### `<Const>` meta

**meta**: *`object`*

*Defined in [plugin_examples/paint.ts:31](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L31)*

<a id="meta.author"></a>

####  author

**● author**: *`string`* = "a"

*Defined in [plugin_examples/paint.ts:37](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L37)*

___
<a id="meta.content"></a>

####  content

**● content**: *`string`* = "<html></html>"

*Defined in [plugin_examples/paint.ts:39](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L39)*

___
<a id="meta.description"></a>

####  description

**● description**: *`string`* = "aaa"

*Defined in [plugin_examples/paint.ts:36](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L36)*

___
<a id="meta.id"></a>

####  id

**● id**: *`string`* = "counter_xxx"

*Defined in [plugin_examples/paint.ts:32](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L32)*

___
<a id="meta.name"></a>

####  name

**● name**: *`string`* = "counter"

*Defined in [plugin_examples/paint.ts:34](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L34)*

___
<a id="meta.tags"></a>

####  tags

**● tags**: *`string`* = "a,b,c"

*Defined in [plugin_examples/paint.ts:38](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L38)*

___
<a id="meta.thumbnail_url"></a>

####  thumbnail_url

**● thumbnail_url**: *`string`* = "https://avatars3.githubusercontent.com/u/50242068?s=200&v=4"

*Defined in [plugin_examples/paint.ts:35](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L35)*

___

___
<a id="plugin"></a>

### `<Const>` plugin

**plugin**: *`object`*

*Defined in [plugin_examples/paint.ts:7](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L7)*

<a id="plugin.instanceid"></a>

####  instanceId

**● instanceId**: *`string`* = "a"

*Defined in [plugin_examples/paint.ts:28](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L28)*

___
<a id="plugin.template"></a>

####  template

**● template**: *`string`* =  `<div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_addLine"></vue-p5></div>`

*Defined in [plugin_examples/paint.ts:8](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L8)*

___
<a id="plugin.functions"></a>

####  functions

**functions**: *`object`*

*Defined in [plugin_examples/paint.ts:9](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L9)*

<a id="plugin.functions._addline"></a>

####  _addLine

**● _addLine**: *`string`[]* =  ['p', `
      this.record.line = { x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY }
      this.$send('onDraw', this.record.line)
    `]

*Defined in [plugin_examples/paint.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L20)*

___
<a id="plugin.functions._draw"></a>

####  _draw

**● _draw**: *`string`[]* =  ['sketch', `
      for (let line of this.record.lines) {
        sketch.line(line.px, line.py, line.x, line.y);
      }
    `]

*Defined in [plugin_examples/paint.ts:15](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L15)*

___
<a id="plugin.functions._setup"></a>

####  _setup

**● _setup**: *`string`[]* =  ['sketch', `
      console.log('set up')
      sketch.createCanvas(600, 600)
    `]

*Defined in [plugin_examples/paint.ts:11](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L11)*

___
<a id="plugin.functions.initialize"></a>

####  initialize

**● initialize**: *`string`[]* =  ['return { lines: [], line: {} }']

*Defined in [plugin_examples/paint.ts:10](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L10)*

___
<a id="plugin.functions.ondraw"></a>

####  onDraw

**● onDraw**: *`string`[]* =  ['p', `
      this.record.lines.push({ x: p.x, y: p.y, px: p.px, py: p.py })
    `]

*Defined in [plugin_examples/paint.ts:24](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/paint.ts#L24)*

___

___

___

