> ## [IPU-space Backend](README.md)

### Index

#### Variables

* [roomList](README.md#const-roomlist)
* [sessions](README.md#const-sessions)

#### Functions

* [activatePlugin](README.md#const-activateplugin)
* [compilePlugin](README.md#const-compileplugin)

#### Object literals

* [pluginMarket](README.md#const-pluginmarket)

## Variables

### `Const` roomList

● **roomList**: *`Record<string, Room>`*

*Defined in [mock/resources.ts:17](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L17)*

___

### `Const` sessions

● **sessions**: *`Record<string, object>`*

*Defined in [mock/resources.ts:25](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L25)*

___

## Functions

### `Const` activatePlugin

▸ **activatePlugin**(`meta`: `PluginMeta`): *`Promise<PluginPackage>`*

*Defined in [plugin-compiler/compiler.ts:15](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/plugin-compiler/compiler.ts#L15)*

**Parameters:**

Name | Type |
------ | ------ |
`meta` | `PluginMeta` |

**Returns:** *`Promise<PluginPackage>`*

___

### `Const` compilePlugin

▸ **compilePlugin**(`meta`: `PluginMeta`): *`Promise<Plugin>`*

*Defined in [plugin-compiler/compiler.ts:92](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/plugin-compiler/compiler.ts#L92)*

**Parameters:**

Name | Type |
------ | ------ |
`meta` | `PluginMeta` |

**Returns:** *`Promise<Plugin>`*

___

## Object literals

### `Const` pluginMarket

### ■ **pluginMarket**: *object*

*Defined in [mock/resources.ts:20](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L20)*

###  Chat

● **Chat**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

###  Counter

● **Counter**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

###  Paint

● **Paint**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

###  Player

● **Player**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

###  PlayingCard

● **PlayingCard**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

###  Status

● **Status**: *`PluginMeta`*

*Defined in [mock/resources.ts:21](https://github.com/i-pu/ipu/blob/525c5a5/backend/src/mock/resources.ts#L21)*

___