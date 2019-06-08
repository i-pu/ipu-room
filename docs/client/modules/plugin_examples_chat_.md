[Ipu-space](../README.md) > ["plugin_examples/chat"](../modules/plugin_examples_chat_.md)

# External module: "plugin_examples/chat"

## Index

### Object literals

* [meta](plugin_examples_chat_.md#meta)
* [plugin](plugin_examples_chat_.md#plugin)

---

## Object literals

<a id="meta"></a>

### `<Const>` meta

**meta**: *`object`*

*Defined in [plugin_examples/chat.ts:52](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L52)*

<a id="meta.author"></a>

####  author

**● author**: *`string`* = "a"

*Defined in [plugin_examples/chat.ts:58](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L58)*

___
<a id="meta.content"></a>

####  content

**● content**: *`string`* = "<html></html>"

*Defined in [plugin_examples/chat.ts:60](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L60)*

___
<a id="meta.description"></a>

####  description

**● description**: *`string`* = "aaa"

*Defined in [plugin_examples/chat.ts:57](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L57)*

___
<a id="meta.id"></a>

####  id

**● id**: *`string`* = "counter_xxx"

*Defined in [plugin_examples/chat.ts:53](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L53)*

___
<a id="meta.name"></a>

####  name

**● name**: *`string`* = "counter"

*Defined in [plugin_examples/chat.ts:55](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L55)*

___
<a id="meta.tags"></a>

####  tags

**● tags**: *`string`* = "a,b,c"

*Defined in [plugin_examples/chat.ts:59](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L59)*

___
<a id="meta.thumbnail_url"></a>

####  thumbnail_url

**● thumbnail_url**: *`string`* = "https://avatars3.githubusercontent.com/u/50242068?s=200&v=4"

*Defined in [plugin_examples/chat.ts:56](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L56)*

___

___
<a id="plugin"></a>

### `<Const>` plugin

**plugin**: *`object`*

*Defined in [plugin_examples/chat.ts:3](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L3)*

<a id="plugin.instanceid"></a>

####  instanceId

**● instanceId**: *`string`* = ""

*Defined in [plugin_examples/chat.ts:49](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L49)*

___
<a id="plugin.template"></a>

####  template

**● template**: *`string`* =  `<div>
    <v-list id="chat" two-line="two-line" height="50%">
      <v-subheader>チャット</v-subheader>
      <template v-for="comment, i in record.comments">
        <v-list-tile v-if="comment.type === 'comment'" :key="comment.comment_id" avatar="avatar">
          <v-list-tile-avatar>
            <img :src="comment.avatar"/>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ comment.text }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ comment.user_name }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </template>
    </v-list>

    <v-container fluid="fluid" grid-list-md="grid-list-md" text-xs-center="text-xs-center">
      <v-layout row="row" wrap="wrap">
        <v-flex d-flex="d-flex" xs8="xs8" sm8="sm8" md8="md8">
          <v-text-field v-model="record.chatInput" label="コメント"></v-text-field>
        </v-flex>
        <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
          <v-btn color="info" @click="comment(record.chatInput); record.chatInput = ''">送信</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>`

*Defined in [plugin_examples/chat.ts:4](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L4)*

___
<a id="plugin.functions"></a>

####  functions

**functions**: *`object`*

*Defined in [plugin_examples/chat.ts:31](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L31)*

<a id="plugin.functions.comment"></a>

####  comment

**● comment**: *`string`[]* =  ['text', `
      this.record.comments.push({
        type: 'comment',
        avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
        comment_id: Math.random().toString(),
        user_name: 'John',
        user_id: 'xxxx',
        text: text
      })
    `]

*Defined in [plugin_examples/chat.ts:38](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L38)*

___
<a id="plugin.functions.initialize"></a>

####  initialize

**● initialize**: *`string`[]* =  [`
      return {
        comments: [],
        chatInput: ''
      }
    `]

*Defined in [plugin_examples/chat.ts:32](https://github.com/i-pu/ipu/blob/102e976/client/src/plugin_examples/chat.ts#L32)*

___

___

___

