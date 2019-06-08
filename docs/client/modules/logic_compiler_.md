[Ipu-space](../README.md) > ["logic/compiler"](../modules/logic_compiler_.md)

# External module: "logic/compiler"

## Index

### Functions

* [compile](logic_compiler_.md#compile)
* [fetchPreinstalledModules](logic_compiler_.md#fetchpreinstalledmodules)

---

## Functions

<a id="compile"></a>

### `<Const>` compile

▸ **compile**(plugin: *`Plugin`*, properties: *`PluginProperties`*): `Promise`<`VueConstructor`<`object` & `object` & `object` & `Vue`>>

*Defined in [logic/compiler.ts:55](https://github.com/i-pu/ipu/blob/ce338ba/client/src/logic/compiler.ts#L55)*

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

**Returns:** `Promise`<`VueConstructor`<`object` & `object` & `object` & `Vue`>>

___
<a id="fetchpreinstalledmodules"></a>

### `<Const>` fetchPreinstalledModules

▸ **fetchPreinstalledModules**(): `Promise`<`object`>

*Defined in [logic/compiler.ts:10](https://github.com/i-pu/ipu/blob/ce338ba/client/src/logic/compiler.ts#L10)*

\[TODO\] Import dynamically additional components are used in a plugin.

**Returns:** `Promise`<`object`>

___

