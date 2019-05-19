// ===============================
//  Example plugin youtube player
// ===============================
import { Plugin } from '../model'

// test in local
export class YoutubePlayerServer {
  public video_id: string = 'SX_ViT4Ra7k'
}

const youtubeTemplate = `
<div>
  <v-btn @click="$log('test')"> Test </v-btn>
  <player :video-id="v.video_id" player-width="1280" player-height="750" :player-vars="{autoplay: 1}"  @ready="$log('ready')" @playing="$log('playing')" />
</div>
`

const youtubePlayer: Plugin = {
  template: youtubeTemplate,
  events: [],
  record: { video_id: 'SX_ViT4Ra7k' },
  addons: {},
}

export default youtubePlayer
