[Ipu-space](../README.md) > ["api/mock"](../modules/api_mock_.md)

# External module: "api/mock"

## Index

### Variables

* [COMMENTS_MOCK](api_mock_.md#comments_mock)
* [ROOMS_MOCK](api_mock_.md#rooms_mock)
* [ROOM_MEMBER_MOCK](api_mock_.md#room_member_mock)

### Object literals

* [USER_MOCK](api_mock_.md#user_mock)

---

## Variables

<a id="comments_mock"></a>

### `<Const>` COMMENTS_MOCK

**● COMMENTS_MOCK**: *`never`[]* =  []

*Defined in [api/mock.ts:30](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L30)*

___
<a id="rooms_mock"></a>

### `<Const>` ROOMS_MOCK

**● ROOMS_MOCK**: *`Room`[]* =  [
  {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnail_url: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [
      { id: '123', name: 'Tom', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
      // { id: '456', name: 'John', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
      // { id: '789', name: 'Alice', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
    ],
    pluginPackages: [],
    plugins: []
  },
]

*Defined in [api/mock.ts:3](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L3)*

___
<a id="room_member_mock"></a>

### `<Const>` ROOM_MEMBER_MOCK

**● ROOM_MEMBER_MOCK**: *`User`[]* =  [
  { id: '123', name: 'Tom', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
  { id: '456', name: 'John', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
  { id: '789', name: 'Alice', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
]

*Defined in [api/mock.ts:23](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L23)*

___

## Object literals

<a id="user_mock"></a>

### `<Const>` USER_MOCK

**USER_MOCK**: *`object`*

*Defined in [api/mock.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L20)*

<a id="user_mock.avatar_url"></a>

####  avatar_url

**● avatar_url**: *`string`* = "https://avatars0.githubusercontent.com/u/9064066?v=4&s=460"

*Defined in [api/mock.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L20)*

___
<a id="user_mock.id"></a>

####  id

**● id**: *`string`* = "123"

*Defined in [api/mock.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L20)*

___
<a id="user_mock.name"></a>

####  name

**● name**: *`string`* = "Tom"

*Defined in [api/mock.ts:20](https://github.com/i-pu/ipu/blob/102e976/client/src/api/mock.ts#L20)*

___

___

