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
- roomId: string
部屋ID
- instanceId: string
プラグインインスタンスID
- data: クライアント同士で用いるデータ
    - event: string
    イベント名
    - args: any[]
    引数
## server to client
- data: クライアント同士で用いるデータ
    - event: string
    イベント名
    - args: any[]
    引数

# `plugin/sync`
## client to server
- roomId: string
部屋ID
- instanceId: string
プラグインインスタンスID
## server to client
- record: Record<string, any>
レコード

# `plugin/clone`
## client to server
- roomId: string
部屋ID
- instanceId: string
プラグインインスタンスID
- record: Record<string, any>
プラグインのレコード
- from: string
syncリクエスト元ソケットID
## server to client
- roomId: string
部屋ID
- instanceId: string
プラグインインスタンスID
- from: string
syncリクエスト元ソケットID