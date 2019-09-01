<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap)
      v-navigation-drawer(
        v-model="drawer"
        absolute
      )
        v-list
          v-list-group(prepend-icon="home")
            template(v-slot:activator)
              v-list-tile
                v-list-tile-title カテゴリ

            v-list-tile(
              v-for="category in categories"
              :key="category.name"
            )
              v-list-tile-action
                v-icon {{ category.icon }}
              v-list-tile-title {{ category.name }}

          v-list-group(prepend-icon="home")
            template(v-slot:activator)
              v-list-tile
                v-list-tile-title 並び替え
            v-list-tile(
              v-for="sortKey in sortKeys"
              :key="sortKey.name"
            )
              v-list-tile-action
                v-icon {{ sortKey.icon }}
              v-list-tile-title {{ sortKey.name }}

      v-flex(d-flex xs12 sm12 md12)
        v-toolbar(app color="light-blue" dark)
          v-toolbar-side-icon(@click.stop="drawer = !drawer")
          v-toolbar-title.headline.text-uppercase
            span.pr-3(@click="toLobby") マーケット

          v-spacer

          v-text-field(
            hide-details
            prepend-icon="search"
            single-line
            v-model="searchText"
            placeholder="名前, タグで検索"
          )

          PluginUploadForm(@reload="reloadPlugins")
        
        v-list(two-line subheader)
          v-subheader
            v-icon.px-2 sort
            | {{ category.name }}
            v-icon.px-2 sort_by_alpha
            | {{ sortKey.name }}

          v-list-tile(avatar ripple @click="toDetail(pluginOverview.id)" v-for="pluginOverview in pluginOverviews")
            v-list-tile-avatar
              img(:src="pluginOverview.thumbnailUrls[0]")
            v-list-tile-content
              v-list-tile-title {{ pluginOverview.name }}
              v-list-tile-sub-title {{ pluginOverview.description | less }}
            v-list-tile-action
              v-list-tile-action-text {{ pluginOverview.version }}

</template>

<script lang="ts">
import { createComponent, onBeforeMount, ref, watch } from '@vue/composition-api'
import _ from 'lodash'
import router from '@/router'
import { PluginMeta, PluginPackage } from '@/model'
import PluginUploadForm from '@/components/market/PluginUploadForm.vue'

interface MarketCategory { name: string, icon: string }
interface MarketSortKey { name: string, icon: string, query: string }

const categories: MarketCategory[] = [
  { name: 'すべてのカテゴリ', icon: 'home' },
  { name: 'A', icon: 'home' },
  { name: 'B', icon: 'home' },
  { name: 'C', icon: 'home' },
  { name: 'D', icon: 'home' },
]
const sortKeys: MarketSortKey[] = [
  { name: '人気順', icon: 'sort_by_alpha', query: '' },
  { name: '新着順', icon: 'sort_by_alpha', query: '' },
]

export default createComponent({
  components: { PluginUploadForm },
  filters: {
    less (s: string): string {
      return s.slice(0, 14) + '...'
    },
  },
  setup () {
    const drawer = ref<boolean>(false)
    const category = ref<MarketCategory>(categories[0])
    const sortKey = ref<MarketSortKey>(sortKeys[0])
    const searchText = ref<string>('')
    const pluginOverviews = ref<PluginMeta[]> ([])

    watch(() => _.debounce(() => {
      console.log(searchText.value)
    }, 1500))

    onBeforeMount(() => {
      reloadPlugins()
    })

    const toDetail = (pluginId: string) => {
      router.push(`/market/${pluginId}`)
    }

    const toLobby = () => {
      router.push('/lobby')
    }

    const reloadPlugins = async () => {
      const metas: PluginMeta[] = await fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins`)
        .then((res) => res.json())
        .catch(console.log)
      pluginOverviews.value = metas
    }

    return {
      reloadPlugins,
      drawer,
      toDetail,
      toLobby,
    }
  },
})
</script>