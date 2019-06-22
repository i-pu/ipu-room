// ==========================
//  degault status plugin
// ========================
import { PluginMeta } from '@client/model'

export default {
  id: 'status-0123-abcdef-4567',
  name: 'status',
  thumbnailUrls: [
    'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: 'v0.0.1',
  tags: '基本',
  content: `
<template lang="pug">
  v-container(grid-list-md)
    v-layout(row wrap)
      v-flex(xs12)
        v-subheader メンバー
      v-flex(v-for="i in 6" :key="i" xs12 md2)
        v-card.d-flex.align-center(
          v-if="$members[i - 1]"
          height="200"
        )
          v-card-title(primary-title)
            .headline {{ $members[i - 1].name }}
          v-card-actions

        v-card.d-flex.align-center(
          v-else
          dark height="200"
        )
          v-card-title(primary-title)
            .headline 無人
          v-card-actions
</template>
<script>
  ({
    initialize () {
      return {}
    },
  })
</script>`
} as PluginMeta