<template lang="pug">
  div
    v-toolbar(app v-if="breakpoint.sm || breakpoint.xs")
      v-toolbar-side-icon
      v-toolbar-title.headline(@click="to('/')") ipu-room
      v-btn(flat @click="to('/market')") ストアへ
      v-spacer
      v-btn(large icon color="primary")
        v-icon person
    v-toolbar(app v-else)
      v-toolbar-title.headline(@click="to('/')") ipu-room
      v-btn(flat @click="to('/about')") 概要
      v-btn(flat href="https://i-pu.github.io/ipu") ドキュメント
      v-btn(flat href="https://github.com/i-pu/ipu") リポジトリ
      v-btn(flat href="https://i-pu.github.io/ipu/other/plugin-spec.html") ロードマップ
      v-btn(flat @click="to('/market')") ストアへ
      v-spacer
      v-btn(large icon color="primary")
        v-icon person
</template>

<script lang="ts">
import { createComponent, SetupContext, computed } from '@vue/composition-api'
import router from '@/router'

export default createComponent({
  setup (props: {}, { root }: SetupContext) {
    const breakpoint = computed(() => root.$vuetify.breakpoint)
    const to = (path: string) => {
      router.push(path)
    }

    return {
      breakpoint,
      to,
    }
  },
})
</script>