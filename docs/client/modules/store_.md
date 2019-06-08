[Ipu-space](../README.md) > ["store"](../modules/store_.md)

# External module: "store"

## Index

### Interfaces

* [State](../interfaces/store_.state.md)

### Object literals

* [actions](store_.md#actions)
* [getters](store_.md#getters)
* [mutations](store_.md#mutations)
* [storeState](store_.md#storestate)

---

## Object literals

<a id="actions"></a>

### `<Const>` actions

**actions**: *`object`*

*Defined in [store.ts:39](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L39)*

<a id="actions.setuserid"></a>

####  setUserId

▸ **setUserId**(__namedParameters: *`object`*, payload: *`string`*): `void`

*Defined in [store.ts:43](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L43)*

**Parameters:**

**__namedParameters: `object`**

| Name | Type |
| ------ | ------ |
| commit | `Commit` |

**payload: `string`**

**Returns:** `void`

___
<a id="actions.setusername"></a>

####  setUserName

▸ **setUserName**(__namedParameters: *`object`*, payload: *`string`*): `void`

*Defined in [store.ts:40](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L40)*

**Parameters:**

**__namedParameters: `object`**

| Name | Type |
| ------ | ------ |
| commit | `Commit` |

**payload: `string`**

**Returns:** `void`

___

___
<a id="getters"></a>

### `<Const>` getters

**getters**: *`object`*

*Defined in [store.ts:18](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L18)*

<a id="getters.localonly"></a>

####  localOnly

▸ **localOnly**(state: *[State](../interfaces/store_.state.md)*): `boolean`

*Defined in [store.ts:19](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L19)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| state | [State](../interfaces/store_.state.md) |

**Returns:** `boolean`

___
<a id="getters.userid"></a>

####  userId

▸ **userId**(state: *[State](../interfaces/store_.state.md)*): `string`

*Defined in [store.ts:25](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L25)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| state | [State](../interfaces/store_.state.md) |

**Returns:** `string`

___
<a id="getters.username"></a>

####  userName

▸ **userName**(state: *[State](../interfaces/store_.state.md)*): `string`

*Defined in [store.ts:22](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L22)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| state | [State](../interfaces/store_.state.md) |

**Returns:** `string`

___

___
<a id="mutations"></a>

### `<Const>` mutations

**mutations**: *`object`*

*Defined in [store.ts:30](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L30)*

<a id="mutations.userid-1"></a>

####  userId

▸ **userId**(state: *[State](../interfaces/store_.state.md)*, payload: *`string`*): `void`

*Defined in [store.ts:34](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L34)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| state | [State](../interfaces/store_.state.md) |
| payload | `string` |

**Returns:** `void`

___
<a id="mutations.username-1"></a>

####  userName

▸ **userName**(state: *[State](../interfaces/store_.state.md)*, payload: *`string`*): `void`

*Defined in [store.ts:31](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L31)*

**Parameters:**

| Name | Type |
| ------ | ------ |
| state | [State](../interfaces/store_.state.md) |
| payload | `string` |

**Returns:** `void`

___

___
<a id="storestate"></a>

### `<Const>` storeState

**storeState**: *`object`*

*Defined in [store.ts:12](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L12)*

<a id="storestate.islocalonly"></a>

####  isLocalOnly

**● isLocalOnly**: *`true`* = true

*Defined in [store.ts:13](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L13)*

___
<a id="storestate.userid-2"></a>

####  userId

**● userId**: *`string`* = ""

*Defined in [store.ts:15](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L15)*

___
<a id="storestate.username-2"></a>

####  userName

**● userName**: *`string`* = ""

*Defined in [store.ts:14](https://github.com/i-pu/ipu/blob/102e976/client/src/store.ts#L14)*

___

___

