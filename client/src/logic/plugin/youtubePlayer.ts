// ========================
//  Example plugin counter
// ========================
import { Plugin } from './component'
// @ts-ignore
import { Youtube } from 'vue-youtube'

// test in local
export class YoutubePlayerServer {
  public videoId: string = 'SX_ViT4Ra7k'
}

const youtubeTemplate = `
<div>
  <v-btn> Test </v-btn>
  <player :video-id="videoId" player-width="1280" player-height="750" :player-vars="{autoplay: 1}" />
</div>
`

const youtubePlayer: Plugin = {
  template: youtubeTemplate,
  events: [],
  record: {
    videoId: 'SX_ViT4Ra7k',
  },
  addons: { player: Youtube },
}

export default youtubePlayer
