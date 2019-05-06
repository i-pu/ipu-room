// ========================
//  Example plugin counter
// ========================
import { BasePlugin } from '../baseplugin'
import { Youtube } from 'vue-youtube'

// test in local
export class YoutubePlayer extends BasePlugin {
  public videoId: string = 'SX_ViT4Ra7k'

  constructor () {
    super('Youtube')
  }
}

const youtubeTemplate = `
<div>
  <v-btn> Test </v-btn>
  <player :video-id="videoId" player-width="1280" player-height="750" :player-vars="{autoplay: 1}" />
</div>
`

export default {
  instance: new YoutubePlayer(),
  template: youtubeTemplate,
  addons: { player: Youtube },
}
