# その他のイベント

困ったら [モックサーバー実装(TypeScript)](https://github.com/i-pu/ipu-room/blob/master/backend/src/mock/simple-server.ts) を見てください。
クライアントはこれに準拠しています。

```ts
// =========================
// index.d.ts
//
// Copyright (c) 2019 i-pu
// =========================

export interface Plugin {
  template: string,
  functions: string,
  instanceId: string,
  config: {
    enabled: boolean,
  }
}

/**
* Expresses Data of static infomation about a plugin.
* @param id HTML template
* @param thumbnailUrls
* @param content raw script of a plugin
*/
interface PluginMeta {
  id: string,
  version: string,
  thumbnailUrls: string[],
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}

export interface PluginPackage {
  plugin: Plugin,
  meta: PluginMeta,
}

/**
* Room
*/
export interface Room {
  name: string,
  id: string,
  thumbnailUrl: string,
  members: User[],
  pluginPackages: PluginPackage[]
}

/**
* User
*/
export interface User {
  name: string,
  id: string,
  avatarUrl: string
}


```

## room/create
部屋を作る
### client to server
```ts
{
  // 部屋名
  roomName: string
  // プラグインIDの配列
  plugins: string[]
}
```

### server to client 
```ts
{
  // 作成された部屋
  room: Room
}
```

## room/enter
部屋に入る
### client to server
- roomId: `string`
### server to client 
same to [room/create](#roomcreate)

## room/exit
部屋から出る
### client to server
{}
### server to client
{}

## room/update
部屋から誰か出たときに発生
### server to clinet
same to [room/create](#roomcreate)

## room/remove
部屋を削除する
### client to server
```ts
{
  roomId: string
}
```

### server to client
```ts
{}
```
  
## visit
### client to server
- userName: `string`
### client to server
発生しない
None
### server to client 
- user:
  - name: `string`
  - id: `string`
  - roomId: `string`

## lobby
### client to server
{}
### server to client 
- rooms: [room]  
same to [room/create](#roomcreate)

## disconnect
### server to client 
{}
### client to server
{}
