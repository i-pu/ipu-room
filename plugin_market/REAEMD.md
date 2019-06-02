### diesel
#### AsChangeset
```
#[derive(AsChangeset)]
```
update のときにこの構造体をset(&PluginInfo)みたいに構造体を渡せるようになる
update の際にidを変更しないのでidは直接変更させる必要がある
またfilterをかけないとすべての情報が更新されてしまうので注意

#### QueryDsl
filter や find や order などが入った trait
