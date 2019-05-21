// ========================
//  Example plugin paint
// ========================

import { Plugin, PluginMeta } from '@/model'

export const PAINT_PLUGIN: Plugin = {
  template: `<div><vue-p5 @setup="_setup" @draw="_draw" @mousedragged="_mouseDragged"></vue-p5></div>`,
  functions: {
    initialize: ['return { lines: [] }'],
    _setup: ['sketch', `
      console.log('set up')
      sketch.createCanvas(600, 600)
    `],
    _draw: ['sketch', `
      for (let line of this.record.lines) {
        sketch.line(line.px, line.py, line.x, line.y);
      }
    `],
    _mouseDragged: ['p', `
      this.record.lines.push({ x: p.mouseX, y: p.mouseY, px: p.pmouseX, py: p.pmouseY })
    `]
  },
}

export const PAINT_META: PluginMeta = {
  plugin_id: 'counter_xxx',
  // plugin name
  name: 'counter',
  thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
  description: 'aaa',
  author: 'a',
  tags: 'a,b,c',
  content: '<html></html>',
}
