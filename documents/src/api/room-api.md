# ルームAPI

モデルは [ここ](/plugin/#モデル) を参照

## 部屋を作る

`room/create`

### Request
```ts
{
  roomName: string, // 部屋の名前
  plugins: string[], // プラグインIDの配列
}
```

### Response
```ts
{
  room: Room,
  plugins: PluginPackage[]
}
```

## 部屋に入る

`room/enter`

### Request
```ts
{
  roomId: string
}
```

### Response
```ts
{
  room: Room,
  plugins: PluginPackage[]
}
```

## 部屋から出る

`room/exit`

### Request
```ts
{}
```

### Response
```ts
{}
```

## `room/update` イベント

部屋から誰かが出たときに発生

`room/update`

### Response
```ts
{
  room: Room,
  plugins: PluginPackage[]
}
```
  
## `visit` イベント
### Request
```ts
{
  userName: string
}
```

### Response
- user:
  - name: `string`
  - id: `string`
  - roomId: `string`

## `lobby` イベント
### Request
```ts
{}
```

### Response
```ts
{
  rooms: Room[] // 現在存在する部屋一覧
}
```
