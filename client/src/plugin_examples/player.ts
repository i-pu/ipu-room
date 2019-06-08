// ========================
//  Example plugin player
// ========================

import { Plugin, PluginMeta } from '@/model'

module.exports = {
  plugin: {
    template: `
    <div>
      <player :video-id="record.videoId" ref="youtube" @playing="_playing" @paused="_paused" />
    </div>
    `,
    functions: {
      initialize: [`return { videoId: 'SX_ViT4Ra7k' }`],
      _playing: [`
        console.log('playing')
        this.$send('play')
      `],
      _paused: [`
        console.log('paused')
        this.$send('pause')
      `],
      play: [`
        this.$refs.youtube.player.playVideo()
      `],
      pause: [`
        this.$refs.youtube.player.pauseVideo()
      `]
    },
    instanceId: 'a',
    config: {
      enabled: true
    }
  },
  meta: {
    id: 'counter_xxx',
    // plugin name
    name: 'counter',
    thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    description: 'aaa',
    author: 'wakame-tech',
    tags: 'a,b,c',
    content: '<html></html>',
  }
} as {
  plugin: Plugin, meta: PluginMeta
}
