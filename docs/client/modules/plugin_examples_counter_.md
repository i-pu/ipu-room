[Ipu-space](../README.md) > ["plugin_examples/counter"](../modules/plugin_examples_counter_.md)

# External module: "plugin_examples/counter"

## Index

### Object literals

* [meta](plugin_examples_counter_.md#meta)
* [plugin](plugin_examples_counter_.md#plugin)

---

## Object literals

<a id="meta"></a>

### `<Const>` meta

**meta**: *`object`*

*Defined in [plugin_examples/counter.ts:16](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L16)*

<a id="meta.author"></a>

####  author

**● author**: *`string`* = "a"

*Defined in [plugin_examples/counter.ts:22](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L22)*

___
<a id="meta.content"></a>

####  content

**● content**: *`string`* = "<html></html>"

*Defined in [plugin_examples/counter.ts:24](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L24)*

___
<a id="meta.description"></a>

####  description

**● description**: *`string`* = "aaa"

*Defined in [plugin_examples/counter.ts:21](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L21)*

___
<a id="meta.id"></a>

####  id

**● id**: *`string`* = "counter_xxx"

*Defined in [plugin_examples/counter.ts:17](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L17)*

___
<a id="meta.name"></a>

####  name

**● name**: *`string`* = "counter"

*Defined in [plugin_examples/counter.ts:19](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L19)*

___
<a id="meta.tags"></a>

####  tags

**● tags**: *`string`* = "a,b,c"

*Defined in [plugin_examples/counter.ts:23](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L23)*

___
<a id="meta.thumbnail_url"></a>

####  thumbnail_url

**● thumbnail_url**: *`string`* = "https://avatars3.githubusercontent.com/u/50242068?s=200&v=4"

*Defined in [plugin_examples/counter.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L20)*

___

___
<a id="plugin"></a>

### `<Const>` plugin

**plugin**: *`object`*

*Defined in [plugin_examples/counter.ts:7](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L7)*

<a id="plugin.instanceid"></a>

####  instanceId

**● instanceId**: *`string`* = "a"

*Defined in [plugin_examples/counter.ts:13](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L13)*

___
<a id="plugin.template"></a>

####  template

**● template**: *`string`* =  `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`

*Defined in [plugin_examples/counter.ts:8](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L8)*

___
<a id="plugin.functions"></a>

####  functions

**functions**: *`object`*

*Defined in [plugin_examples/counter.ts:9](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L9)*

<a id="plugin.functions.initialize"></a>

####  initialize

**● initialize**: *`string`[]* =  ['return { count: 0 }']

*Defined in [plugin_examples/counter.ts:10](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L10)*

___
<a id="plugin.functions.plus"></a>

####  plus

**● plus**: *`string`[]* =  ['this.record.count++']

*Defined in [plugin_examples/counter.ts:11](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/counter.ts#L11)*

___

___

___

