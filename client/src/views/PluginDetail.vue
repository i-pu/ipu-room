<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap v-if="loaded")
      v-toolbar(app)
        v-btn(icon to="/market")
          v-icon arrow_back
        v-toolbar-title.headline.text-uppercase
          span.pr-3 プラグインの詳細
        v-spacer
        PluginUploadForm(:update="true" :pluginMeta="pluginMeta")

      v-flex(xs12 d-flex)
        v-carousel(hide-delimiters height="300")
          v-carousel-item(
            v-for="src, i in pluginMeta.thumbnailUrls"
            :key="i"
            :src="src"
          )
          
      v-flex(xs12 d-flex)
        v-list(two-line subheader)
          v-subheader 基本情報
          v-list-tile
            v-list-tile-content
              v-list-tile-title パッケージ名
              v-list-tile-title {{ pluginMeta.author }}/{{ pluginMeta.name }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title バージョン
              v-list-tile-sub-title {{ pluginMeta.version }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title タグ
              v-list-tile-sub-title
                v-chip(
                  v-for="tag in pluginMeta.tags.split(',')"
                  label
                  color="pink"
                  text-color="white"
                )
                  v-icon(left) label
                  | {{ tag }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title 説明
              v-list-tile-sub-title {{ pluginMeta.description }}
</template>

<script lang="ts">
import { createComponent, onBeforeMount, ref, SetupContext } from '@vue/composition-api'
import { PluginMeta } from '@/model'
import PluginEditor from '@/components/market/PluginEditor.vue'
import PluginUploadForm from '@/components/market/PluginUploadForm.vue'

export default createComponent({
  components: { PluginEditor, PluginUploadForm },
  setup (props: {}, { root }: SetupContext) {
    const pluginMeta = ref<PluginMeta | null>(null)
    const loaded = ref<boolean>(false)

    onBeforeMount(async () => {
      loaded.value = false
      console.log(`pluginId: ${this.$route.params.pluginId}`)
      const meta: PluginMeta = await fetch(
        `${process.env.VUE_APP_API_ORIGIN}/market/plugins/${root.$route.params.pluginId}`,
      )
        .then((res) => res.json())
      console.log('[1/4] fetched plugin package')
      pluginMeta.value = meta
      loaded.value = true
    })

    return {
      pluginMeta,
      loaded,
    }
  },
})
</script>
