// ========================
//  Example plugin player
// ========================

import { PluginMeta } from '@/model'

export default {
  id: 'playingcard-0123-abcdef-4567',
  name: 'Youtubeプレイヤー',
  thumbnailUrls: [
    'https://cdn.aprico-media.com/production/posts/eyecatches/000/000/957/original.jpg?1505469404',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: 'v0.0.1',
  tags: '娯楽',
  content: `
<template>
  <div>
    <player :video-id="record.videoId" ref="youtube" @playing="_playing" @paused="_paused" />
  </div>
</template>
<script>
  ({
    initialize () {
      return { videoId: 'SX_ViT4Ra7k' }
    },
    _playing () {
      console.log('playing')
      this.$send('play')
    },
    _paused () {
      console.log('paused')
      this.$send('pause')
    },
    play () {
      this.$refs.youtube.player.playVideo()
    },
    pause () {
      this.$refs.youtube.player.pauseVideo()
    },
  })
</script>`
} as PluginMeta
