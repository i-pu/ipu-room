// ==========================
//  Example plugin counter
// ========================

import { Plugin, PluginProperties, PluginMeta } from '@/model'

export const COUNTER_PLUGIN: Plugin = {
  template: `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  functions: {
    plus (this: { record: Record<string, any> }) {
      this.record.count++
    }
  }
}

export const COUNTER_META: PluginMeta = {
  plugin_id: 'counter_xxx',
  // plugin name
  name: 'counter',
  description: 'aaa',
  author: 'a',
  tags: 'a,b,c',
  content: '<html></html>'
}
