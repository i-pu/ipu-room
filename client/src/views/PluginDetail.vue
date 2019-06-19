<template lang="pug">
  v-layout(row wrap v-if="loaded")
    v-toolbar(app)
      v-btn(icon to="/market")
        v-icon arrow_back
      v-toolbar-title.headline.text-uppercase
        span.pr-3 {{ pluginPackage.meta.name }} の詳細
      v-spacer
    v-flex(xs12 d-flex)
      v-carousel(hide-delimiters height="300")
        v-carousel-item(
          v-for="src, i in pluginPackage.meta.thumbnailUrls"
          :key="i"
          :src="src"
        )
    v-list(two-line subheader)
      v-subheader 基本情報
      v-list-tile(
        v-for="value, key in pluginPackage.meta"
      )
        v-list-tile-content
          v-list-tile-title {{ key }}
          v-list-tile-sub-title(v-if="key !== 'tags'") {{ value }}
          v-list-tile-sub-title(v-else)
            v-chip(
              v-for="tag in value.split(',')"
              label
              color="pink"
              text-color="white"
            )
              v-icon(left) label
              | {{ tag }}

    PluginEditor(:pluginPackage="pluginPackage")
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import PluginEditor from '@/components/market/PluginEditor.vue'
import { PluginPackage } from '../model'

@Component({
  components: { PluginEditor },
})
export default class PluginDetail extends Vue {
  private pluginPackage!: PluginPackage
  private loaded: boolean = false

  created () {
    fetch(`http://localhost:8080/api/v1/market/plugins/aaa`)
      .then(res => res.json())
      .then((pluginPackage: PluginPackage) => {
        this.pluginPackage = pluginPackage
        this.loaded = true
      })
  }
}
</script>
