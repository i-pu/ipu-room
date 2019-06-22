<template lang="pug">
  div
    v-toolbar(app v-if="$vuetify.breakpoint.sm || $vuetify.breakpoint.xs")
      v-toolbar-side-icon
      v-toolbar-title.headline(@click="$router.push('/')") ipu-room
      v-spacer
      v-btn(large icon color="primary")
        v-icon person
    v-toolbar(app v-else)
      v-toolbar-title.headline(@click="$router.push('/')") ipu-room
      v-btn(flat @click="$router.push('/about')") 概要
      v-btn(flat href="https://i-pu.github.io/ipu") ドキュメント
      v-btn(flat href="https://github.com/i-pu/ipu") リポジトリ
      v-btn(flat href="https://i-pu.github.io/ipu/other/plugin-spec.html") ロードマップ
      v-btn(flat @click="$router.push('/market')") ストアへ
      v-spacer
      v-btn(large icon color="primary")
        v-icon person
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

@Component
export default class TopToolbar extends Vue {
  
}
</script>