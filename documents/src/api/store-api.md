# ストアAPI

名前はdatabase-controllerだが，これは初期の頃の命名ミスで，ゆくゆくはデータベースだけでなくいろいろなことをやらせる予定である．

/database-controllerが必要
- /database-controller/api/v1/plugins

## 全部のプラグインを取得
```
GET /database-controller/api/v1/plugins
```

```json
[
  {
    "id": "uuid4のid",
    "name": "counter",
    "description": "カウンターです",
    "author": "bob",
    "tags": "bob,util",
    "content": "long long source code" 
  }
]
```
## 1つのプラグインを取得

idの部分はuuid4

```
GET /database-controller/api/v1/plugins/{id}
```

- /database-controller/api/v1/plugins/7487f87...7a9a87f0a8
- 
```json
{
  "id": "7487f87...7a9a87f0a8",
  "name": "counter",
  "description": "カウンターです",
  "author": "bob",
  "tags": "bob,util",
  "content": "long long source code" 
}
```

## 新しくプラグインを作成する
```
POST /database-controller/api/v1/plugins
```

- /database-controller/api/v1/plugins

#### 引数
```json
{
  "id": "ここのidはあったとしても無視します",
  "name": "counter",
  "description": "カウンターです",
  "author": "bob",
  "tags": "bob,util",
  "content": "long long source code" 
}
```
##### 返り値
```json
{
  "id": "uuid4のid",
  "name": "counter",
  "description": "カウンターです",
  "author": "bob",
  "tags": "bob,util",
  "content": "long long source code" 
}
```
## プラグインを更新する

```
PUT /database-controller/api/v1/plugins/{id}
```

- /database-controller/api/v1/plugins/7487f87...7a9a87f0a8
##### 引数
```json
{
  "id": "ここのidはあったとしてもパスの方を使います",
  "name": "counter2",
  "description": "カウンター2です",
  "author": "bob",
  "tags": "bob,util",
  "content": "long long source code" 
}
```
##### 返り値
```json
{
  "id": "7487f87...7a9a87f0a8",
  "name": "counter2",
  "description": "カウンター2です",
  "author": "bob",
  "tags": "bob,util",
  "content": "long long source code" 
}
```
## プラグインを削除する(未実装)
```
DELETE /database-controller/api/v1/plugins
```
