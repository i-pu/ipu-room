// ==========================
//  Example plugin counter
// ========================
import { PluginMeta } from '@model'

export default {
  id: 'counter-0123-abcdef-4567',
  name: 'counter',
  thumbnailUrls: [
    'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: 'v0.1.1',
  tags: 'a,b,c',
  content: `
    <template>
      <div>
        <h3> {{ record.count }} </h3>
        <v-btn @click="plus"> Add </v-btn>
      </div>
    </template>
    <script>
    ({
      initialize () {
        return {
          count: 0
        }
      },
      plus() {
        this.record.count++
      }
    })
    </script>`
} as PluginMeta
