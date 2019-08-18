// ========================
//  Example plugin paint
// ========================
import { PluginMeta } from '@/model'

export default {
  id: 'playingcard-0123-abcdef-4567',
  name: 'ペイント',
  thumbnailUrls: [
    'https://image.flaticon.com/icons/svg/67/67745.svg',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: '0.0.1',
  tags: '娯楽',
  content: `
<template>
  <div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_dragged" @mousereleased="_released"></vue-p5></div>
</template>
<script>
  ({
    initialize () {
      return { lines: [], buffer: [] }
    },
    _setup (sketch) {
      sketch.createCanvas(600, 600)
    },
    _draw (sketch) {
      for (const line of this.record.lines) {
        sketch.line(line.px, line.py, line.x, line.y);
      }
    },
    _dragged (p) {
      const l = { x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY }
      this.record.lines.push(l)
      this.record.buffer.push(l)
      if (this.record.buffer.length > 10) {
        this.$send('onDraw', this.record.buffer, this.$socket.id)
        this.record.buffer = []
      }
    },
    _released (p) {
      this.$send('onDraw', this.record.buffer, this.$socket.id)
      this.record.buffer = []
    },
    onDraw (buffer, id) {
      if (this.$socket.id !== id) {
        this.record.lines.push(...buffer)
      }
    },
  })
</script>`
} as PluginMeta
