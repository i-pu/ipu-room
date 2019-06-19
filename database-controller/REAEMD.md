### docker
#### volume
docker-composeでvolumeとして宣言しているものは
docker-compose downしても消えないので
docker-entrypoint-initdb.dをmountしている場合，
ちゃんと実行されない可能性がある
### diesel
#### cli
``` bash 
// 空のmigrationディレクトリを作成する
diesel setup
```
```bash
// タイムスタンプとnameを連結して
// migration ディレクトリに新しく作成する 
// up.sqlとdown.sqlが作成される
diesel migration generate [name]
```
```bash
// 
diesel migration run
```
有効になっているmigrationをdatabaseに適応する
#### AsChangeset
```
#[derive(AsChangeset)]
```
update のときにこの構造体をset(&PluginInfo)みたいに構造体を渡せるようになる
update の際にidを変更しないのでidは直接変更させる必要がある
またfilterをかけないとすべての情報が更新されてしまうので注意

#### QueryDsl
filter や find や order などが入った trait

#### Null に update するときに注意すること
Opion<T>にして，Noneをdatabaseに入れようとしても．  
Noneをデフォルトで無視するらしい．
Noneにupdateしたければ，Option<Option<T>>にする必要がある  
こっちでもいいらしい
```
#[changeset_options（treat_none_as_null =“true”）]
pub struct Hoge {
}
```

### serde
#### skip_deserialization
json 等から struct(rust) にするときスキップするのでdefault があればそれを呼ぶ