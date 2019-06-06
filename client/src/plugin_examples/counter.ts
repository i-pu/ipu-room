// ==========================
//  Example plugin counter
// ========================

import { Plugin, PluginMeta } from '@/model'

export const plugin: Plugin = {
  template: `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  functions: {
    initialize: ['return { count: 0 }'],
    plus: ['this.record.count++'],
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
