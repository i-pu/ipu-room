# 概要
名前はdatabase-controllerだが，これは初期の頃の命名ミスで，ゆくゆくはデータベースだけでなくいろいろなことをやらせる予定である．

## API
/database-controllerが必要
- /database-controller/api/v1/plugins
### Plugin
#### GET /database-controller/api/v1/plugins
全部のプラグインを取得
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
#### GET /database-controller/api/v1/plugins/{id}
1つのプラグインを取得．idの部分はuuid4
- /database-controller/api/v1/plugins/7487f87...7a9a87f0a8
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

#### POST /database-controller/api/v1/plugins
新しくプラグインを作成する
- /database-controller/api/v1/plugins


##### 引数
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
#### PUT /database-controller/api/v1/plugins/{id}
プラグインを更新する
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
#### DELETE /database-controller/api/v1/plugins
未実装
