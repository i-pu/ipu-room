# プラグインAPI

## `plugin/register`
### Request
```ts
{
  name: string, // プラグイン名
  description: string, // プラグインの説明
  author: string, // 製作者
  tags: string, // タグ(カンマ区切り)
  content: string // プラグインの生データ(HTML)
}
```

### Response
```ts
{
  state: boolean // アップロードの可否
}
```

## `plugin/trigger`
### Request
```ts
{
  roomId: string, // 部屋ID
  instanceId: string, // プラグインインスタンスID
  data: {
    event: string, // イベント名
    args: any[] // 引数
  }
}
```

### Response
```ts
{
  data: {
    event: string, // イベント名
    args: any[] // 引数
  }
}
```

## `plugin/sync`
### Request
```ts
{
  roomId: string, // 部屋ID
  instanceId: string // プラグインインスタンスID
}
```

### Response
```ts
{
  record: Record<string, any> // レコード
}
```

## `plugin/clone`
### Request
```ts
{
  roomId: string, // 部屋ID
  instanceId: string, // プラグインインスタンスID
  record: Record<string, any>, // プラグインのレコード
  from: string // syncリクエスト元ソケットID
}
```

### Response
```ts
{
  roomId: string, // 部屋ID
  instanceId: string, // プラグインインスタンスID
  from: string // syncリクエスト元ソケットID
}
```
