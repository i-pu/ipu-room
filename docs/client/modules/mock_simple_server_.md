[Ipu-space](../README.md) > ["mock/simple-server"](../modules/mock_simple_server_.md)

# External module: "mock/simple-server"

## Index

### Variables

* [Chat](mock_simple_server_.md#chat)
* [Counter](mock_simple_server_.md#counter)
* [Paint](mock_simple_server_.md#paint)
* [Player](mock_simple_server_.md#player)
* [app](mock_simple_server_.md#app)
* [color](mock_simple_server_.md#color)
* [io](mock_simple_server_.md#io)
* [sessions](mock_simple_server_.md#sessions)
* [uuidv4](mock_simple_server_.md#uuidv4)

### Functions

* [activatePlugin](mock_simple_server_.md#activateplugin)
* [deepCloneWithFunctions](mock_simple_server_.md#deepclonewithfunctions)
* [parseWithFunctions](mock_simple_server_.md#parsewithfunctions)
* [stringifyWithFunctions](mock_simple_server_.md#stringifywithfunctions)

### Object literals

* [roomList](mock_simple_server_.md#roomlist)

---

## Variables

<a id="chat"></a>

### `<Const>` Chat

**● Chat**: *`any`* =  require('./../plugin_examples/chat')

*Defined in [mock/simple-server.ts:5](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L5)*

___
<a id="counter"></a>

### `<Const>` Counter

**● Counter**: *`any`* =  require('./../plugin_examples/counter')

*Defined in [mock/simple-server.ts:4](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L4)*

___
<a id="paint"></a>

### `<Const>` Paint

**● Paint**: *`object`* =  require('./../plugin_examples/paint')

*Defined in [mock/simple-server.ts:7](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L7)*

#### Type declaration

 meta: `PluginMeta`

 plugin: `Plugin`

___
<a id="player"></a>

### `<Const>` Player

**● Player**: *`any`* =  require('./../plugin_examples/player')

*Defined in [mock/simple-server.ts:6](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L6)*

___
<a id="app"></a>

### `<Const>` app

**● app**: *`any`* =  require('http').createServer()

*Defined in [mock/simple-server.ts:8](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L8)*

___
<a id="color"></a>

### `<Const>` color

**● color**: *`any`* =  require('colors')

*Defined in [mock/simple-server.ts:12](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L12)*

___
<a id="io"></a>

### `<Const>` io

**● io**: *`Server`* =  require('socket.io')(app)

*Defined in [mock/simple-server.ts:11](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L11)*

___
<a id="sessions"></a>

### `<Const>` sessions

**● sessions**: *`Record`<`string`, `string`>*

*Defined in [mock/simple-server.ts:67](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L67)*

___
<a id="uuidv4"></a>

### `<Const>` uuidv4

**● uuidv4**: *`any`* =  require('uuid')

*Defined in [mock/simple-server.ts:10](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L10)*

___

## Functions

<a id="activateplugin"></a>

### `<Const>` activatePlugin

▸ **activatePlugin**(pluginData: *`object`*): `object`

*Defined in [mock/simple-server.ts:42](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L42)*

**Parameters:**

**pluginData: `object`**

| Name | Type |
| ------ | ------ |
| meta | `PluginMeta` |
| plugin | `Plugin` |

**Returns:** `object`

___
<a id="deepclonewithfunctions"></a>

### `<Const>` deepCloneWithFunctions

▸ **deepCloneWithFunctions**<`T`>(data: *`object`*): `T`

*Defined in [mock/simple-server.ts:38](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L38)*

**Type parameters:**

#### T 
**Parameters:**

| Name | Type |
| ------ | ------ |
| data | `object` |

**Returns:** `T`

___
<a id="parsewithfunctions"></a>

### `<Const>` parseWithFunctions

▸ **parseWithFunctions**<`T`>(data: *`string`*): `T`

*Defined in [mock/simple-server.ts:27](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L27)*

**Type parameters:**

#### T 
**Parameters:**

| Name | Type |
| ------ | ------ |
| data | `string` |

**Returns:** `T`

___
<a id="stringifywithfunctions"></a>

### `<Const>` stringifyWithFunctions

▸ **stringifyWithFunctions**(data: *`object`*): `string`

*Defined in [mock/simple-server.ts:20](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L20)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| data | `object` |

**Returns:** `string`

___

## Object literals

<a id="roomlist"></a>

### `<Const>` roomList

**roomList**: *`object`*

*Defined in [mock/simple-server.ts:49](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L49)*

<a id="roomlist.xxxx_yyyy_zzzz"></a>

####  xxxx-yyyy-zzzz

**xxxx-yyyy-zzzz**: *`object`*

*Defined in [mock/simple-server.ts:50](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L50)*

<a id="roomlist.xxxx_yyyy_zzzz.id"></a>

####  id

**● id**: *`string`* = "xxxx-yyyy-zzzz"

*Defined in [mock/simple-server.ts:52](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L52)*

___
<a id="roomlist.xxxx_yyyy_zzzz.members"></a>

####  members

**● members**: *`never`[]* =  []

*Defined in [mock/simple-server.ts:55](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L55)*

___
<a id="roomlist.xxxx_yyyy_zzzz.name"></a>

####  name

**● name**: *`string`* = "雑談部屋1"

*Defined in [mock/simple-server.ts:51](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L51)*

___
<a id="roomlist.xxxx_yyyy_zzzz.pluginpackages"></a>

####  pluginPackages

**● pluginPackages**: *`object`[]* =  [
      activatePlugin(Counter), 
      // activatePlugin(Counter),
      // activatePlugin(Chat),
      // activatePlugin(Player),
      activatePlugin(Paint)
    ]

*Defined in [mock/simple-server.ts:56](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L56)*

___
<a id="roomlist.xxxx_yyyy_zzzz.plugins"></a>

####  plugins

**● plugins**: *`never`[]* =  []

*Defined in [mock/simple-server.ts:63](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L63)*

___
<a id="roomlist.xxxx_yyyy_zzzz.thumbnail_url"></a>

####  thumbnail_url

**● thumbnail_url**: *`string`* = "https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg"

*Defined in [mock/simple-server.ts:54](https://github.com/i-pu/ipu/blob/ce338ba/client/src/mock/simple-server.ts#L54)*

___

___

___

