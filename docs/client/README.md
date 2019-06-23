
#  IPU-space

## Index

### Interfaces

* [State](interfaces/state.md)

### Functions

* [boot](#boot)
* [compile](#compile)

---

## Functions

<a id="boot"></a>

### `<Const>` boot

▸ **boot**(__namedParameters: *`object`*, options: *`object`*): `Promise`<`PluginInstance`>

*Defined in [logic/loader.ts:7](https://github.com/i-pu/ipu/blob/2ce6c72/client/src/logic/loader.ts#L7)*

Initialize plugin with record and compile Vue Component

**Parameters:**

| Name | Type |
| ------ | ------ |
| __namedParameters | `object` |
| options | `object` |

**Returns:** `Promise`<`PluginInstance`>

___
<a id="compile"></a>

### `<Const>` compile

▸ **compile**(plugin: *`Plugin`*, properties: *`PluginProperties`*): `Promise`<`any`>

*Defined in [logic/compiler.ts:62](https://github.com/i-pu/ipu/blob/2ce6c72/client/src/logic/compiler.ts#L62)*

Compiles a plugin-package, and converts Vue component.

### Hook type

*   (without prefix, ex: add): send me, recieve all members in room.
*   (with '\_' prefix ex: \_add): call the function directly.
*   (with 'bc\_' ex: bc\_add): broadcast to room, recieve all members excepts me in room.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| plugin | `Plugin` |  hoge |
| properties | `PluginProperties` |  hoge |

**Returns:** `Promise`<`any`>

___

