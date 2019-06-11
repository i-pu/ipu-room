# Plugin Events

# `plugin/register`
## Client to Server
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
## Server to Client
- state: boolean
アップロードの可否

# `plugin/trigger`
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
- event_name: string
イベント名
- args: any[]
引数

# `plugin/sync`
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID

# `plugin/clone`
- room_id: string
部屋ID
- instance_id: string
プラグインインスタンスID
- record: Record<string, any>
プラグインのレコード
- from: string
syncリクエスト元ソケットID
