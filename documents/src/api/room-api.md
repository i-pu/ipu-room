# ルームAPI
## 部屋を作る

`room/create`

### client to server
- roomName: `string`  
部屋の名前
- plugins: `[string]`  
プラグイン
### server to client 
- room: `room`
  - id: `string`
  room id
  - name: `string`
  room name
  - members: `[]`
    - id: `string`  
    user id
    - name: `string`  
    user name
    - roomId: `string`  
  - plugins: `[]`
    - plugin:
      - template: `string`,
      - functions:  
        `string`: `string`が複数並ぶ 
        - `string`: `[string]`
        - ...
      - instanceId: `string`  
      動いているプラグインを特定するのに使うID
      - config:
        - enabled: `boolean`  
        有効にしているかどうか
    - meta: 
      - id: `string`
      - name: `string`
      - description: `string`
      - author: `string`
      - tags: `string`
      - content: `string`  
      ipl テキスト

## 部屋に入る

`room/enter`

### client to server
- roomId: `string`
### server to client 
same to [room/create](#roomcreate)

## 部屋から出る

`room/exit`

### client to server
{}
### server to client
{}

## イベント
### `room/update` イベント

部屋から誰かが出たときに発生

`room/update`

#### server to clinet
same to [room/create](#roomcreate)
  
### `visit` イベント
#### client to server
- userName: `string`

#### server to client 
- user:
  - name: `string`
  - id: `string`
  - roomId: `string`

### `lobby`
#### client to server
{}
#### server to client 
- rooms: [room]  
same to [room/create](#roomcreate)

### `disconnect`
#### server to client 
{}
#### client to server
{}