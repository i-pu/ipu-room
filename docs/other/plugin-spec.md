# Plugin Specifications
## Change Logs
- 2019.6.5

# 構成
* 単一ファイルに記述、拡張子は`*.ipl`

## Plugin Sequence

![Plugin Sequence](https://i.imgur.com/EA0WOuu.png)

```:sequence
Title: Plugin Sequence

participant User1
participant User2 
participant Server
User1 ->> Server : room/enter
Server ->> User1 : room/enter
User1 -> User1 : Compile Plugins
User1 -> User1 : Initialize Record
User1 ->> Server : plugin/trigger
Server ->> User1 : plugin/trigger
User2 ->> Server : room/enter
Server ->> User2 : room/enter
Server ->> User1 : room/update
User2 -> User2 : Compile Plugins
User2 ->> Server : plugin/sync
Server ->> User1 : plugin/clone
User1 ->> Server : plugin/clone
Server ->> User2 : plugin/sync
User2 -> User2 : Synchronize Record
User2 ->> Server : plugin/trigger
Server ->> User1 : plugin/trigger
Server ->> User2 : plugin/trigger
```

## Plugin Lifecycle

## Examples
see <https://github.com/i-pu/ipu/tree/master/client/src/plugin_examples>

## Demo

## Future
* プラグイン内アドオン
* 複数ファイルに対応
* イベントフックの対応(誰かが退室した時に`onLeave()`が呼ばれるみたいな)
* コメントが流れるチャットプラグイン作りたい
* 大富豪プラグインつくりたい
* みんなでYoutubeみれるプラグインつくりたい