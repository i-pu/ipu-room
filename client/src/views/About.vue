<template lang="pug">
  v-container(fluid grid-list-md ma-0 pa-0 text-xs-center)
    v-layout(row wrap)
      top-toolbar

      v-flex(d-flex xs12 sm12 md12)
        v-responsive(:aspect-ratio="16/3")
          v-sheet.d-flex(color="grey lighten-3" height="100%")
            .display-3.text-center.font-weight-thin.py-4(primary-title) ipu-room

      v-flex(d-flex xs12 sm4 md4)
        v-card.elevation-0(white)
          v-card-media.mt-4.text-xs-center(height="45px")
            v-icon.brown--text(x-large) people
          v-card-title(primary-title)
            .headline(text-xs-center) 交流
          v-card-text 部屋を自由に作ることができます.
      v-flex(d-flex xs12 sm4 md4)
        v-card.elevation-0(white)
          v-card-media.mt-4.text-xs-center(height="45px")
            v-icon.brown--text(x-large) flash_on
          v-card-title(primary-title)
            .headline(text-xs-center) リアルタイム
          v-card-text ソケット通信によりリアルタイムなコミュニケーションが楽しめます.
      v-flex(d-flex xs12 sm4 md4)
        v-card.elevation-0(white)
          v-card-media.mt-4.text-xs-center(height="45px")
            v-icon.brown--text(x-large) widgets
          v-card-title(primary-title)
            .headline(text-xs-center) プラグイン
          v-card-text プラグインを導入して部屋を彩りましょう.
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import TopToolbar from '@/components/TopToolbar.vue'

@Component<About>({
  components: { TopToolbar },
})
export default class About extends Vue {

}
</script>