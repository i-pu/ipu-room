# =========================
# compiler_test.py
#
# Copyright (c) 2019 i-pu
# =========================

# from .html_interpreter import compile
# from . import compiler
from compiler import compiler

# sample counter plugin
counter_plugin = '''
<html>
  <div>
    <h3> {{ record.count }} </h3>
    <v-btn @click="plus(1)"> Add </v-btn>
  </div>
</html>
<script>
initializer (aa, b) {
  return { count: 0 }
}

plus() {
  this.record.count++
}
</script>
'''

# sample chat plugin
chat_plugin = """
<html>
  <div>
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
          <v-btn color="info" @click="comment(); record.chatInput = ''">送信</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</html>
<script>
comment () {
  this.record.comments.push({
    type: 'comment',
    avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
    comment_id: 'a',
    user_name: 'John',
    user_id: 'xxxx',
    text: this.record.chatInput
  })
}
</script>
"""
counter_plugin = """

<template>
  <div>
    <h3> {{ record.count }} </h3>
    <v-btn @click="plus(1)"> Add </v-btn>
  </div>
</template>
<script>
export default class {
  data () {
    return {
      count: 0
    }
  }

  meta () {
    return {
      plugin_id: 'counter_xxx',
      // plugin name
      name: 'counter',
      thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
      description: 'aaa',
      author: 'a',
      tags: 'a,b,c',
      content: '<html></html>'
    }
  }

  plus() {
    this.record.count++
  }
}
</script>
"""

# test

template, functions = compiler(counter_plugin)
print('template: \n{}'.format(template))
print(functions)
