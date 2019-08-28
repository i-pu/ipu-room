# 内部仕様
## パス
### クライアント
`/`

### サーバ
- `/web-socket-server/`
web-socket-serverのデフォルトのパス
- `/web-socket-server/socket.io/`
socket.ioがポーリングするためのパス

# API
- `/database-controller/`
database-controllerのデフォルトのパス
- `/database-controller/api/v1/`
version1のパス
- `/database-controller/api/v1/rooms`
roomsのパス

## ログ
### database-controller
#### 概要
env_loggerでワンライナーでjsonのログを吐くようにする

severityも指定する．

```json
{
  "severity": "INFO",
  "content": {
      "user": {
          "id": "uuid4",
          "name": "hoge"
      }
  }
}
```