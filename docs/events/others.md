# その他のイベント

## room/create
部屋を作る
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
### server to client who is leaving
{}
### server to client who is staying
- members: 
  - id: `string`  
  user id
  - name: `string`  
  user name
  - roomId: `string`  
  
## visit
### client to server
- userName: `string`
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

## sample
this is only development.
### server to client 
### client to server

