// ========================
//  Example plugin paint
// ========================

import { Plugin, PluginMeta } from '@/model'

export const plugin: Plugin = {
  template: `<div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_addLine"></vue-p5></div>`,
  functions: {
    initialize: ['return { lines: [], line: {} }'],
    _setup: ['sketch', `
      console.log('set up')
      sketch.createCanvas(600, 600)
    `],
    _draw: ['sketch', `
      for (let line of this.record.lines) {
        sketch.line(line.px, line.py, line.x, line.y);
      }
    `],
    _addLine: ['p', `
      this.record.line = { x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY }
      this.$send('onDraw', this.record.line)
    `],
    onDraw: ['p', `
      this.record.lines.push({ x: p.x, y: p.y, px: p.px, py: p.py })
    `],
  },
  instanceId: 'a'
}

export const meta: PluginMeta = {
  id: 'counter_xxx',
  // plugin name
  name: 'counter',
  thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
  description: 'aaa',
  author: 'a',
  tags: 'a,b,c',
  content: '<html></html>',
}
