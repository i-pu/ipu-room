// ==========================
//  Example plugin counter
// ========================
import { Plugin, PluginMeta } from '@/model'

module.exports = {
  plugin: {
    template: `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
    functions: {
      initialize: ['return { count: 0 }'],
      plus: ['this.record.count++'],
    },
    instanceId: '',
    config: {
      enabled: true
    }
  },
  meta: {
    id: 'counter-0123-abcdef-4567',
    // plugin name
    name: 'counter',
    thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    description: 'これはプラグインですこれはプラグインですこれはプラグインです',
    author: 'wakame-tech',
    version: 'v0.1.1',
    tags: 'a,b,c',
    content: '<html></html>',
  }
} as {
  plugin: Plugin, meta: PluginMeta
}
