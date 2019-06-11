# Plugin Events

[準拠しているコード](https://github.com/i-pu/ipu/blob/%2348/client/src/mock/simple-server.ts)

# `plugin/register`
## client to server
- name: string
プラグイン名
- description: string
プラグインの説明
- author: string
製作者
- tags: string
タグ(カンマ区切り)
- content: string
プラグインの生データ(HTML)
## server to client
- state: boolean
アップロードの可否

# `plugin/trigger`
## client to server
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
- event_name: string
イベント名
- args: any[]
引数
## server to client
- event: string
イベント名
- args: any[]
引数

# `plugin/sync`
## client to server
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
## server to client
- record: Record<string, any>
レコード

# `plugin/clone`
## client to server
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
- record: Record<string, any>
プラグインのレコード
- from: string
syncリクエスト元ソケットID
## server to client
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
- from: string
syncリクエスト元ソケットID