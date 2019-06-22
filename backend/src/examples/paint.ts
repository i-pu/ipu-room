// ========================
//  Example plugin paint
// ========================
import { PluginPackage } from '@client/model'

export default {
  plugin: {
    // tslint:disable-next-line
    template: `<div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_dragged" @mousereleased="_released"></vue-p5></div>`,
    functions: `({
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
    })`,
    instanceId: 'a',
    config: {
      enabled: true,
    },
  },
  meta: {
    id: 'paint-xxxx-12345678',
    // plugin name
    name: 'counter',
    thumbnailUrls: ['https://avatars3.githubusercontent.com/u/50242068?s=200&v=4'],
    description: 'aaa',
    author: 'wakame-tech',
    tags: 'a,b,c',
    content: '<html></html>',
  },
} as PluginPackage