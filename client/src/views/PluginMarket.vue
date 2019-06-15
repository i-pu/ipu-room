<template lang="pug">
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
          span.pr-3 マーケット

        v-spacer

        v-text-field(
          hide-details
          prepend-icon="search"
          single-line
          v-model="searchText"
          placeholder="名前, タグで検索"
        )

        plugin-create-form
      
      v-list(two-line subheader)
        v-subheader
          v-icon.px-2 sort
          | {{ category.name }}
          v-icon.px-2 sort_by_alpha
          | {{ sortKey.name }}

        v-list-tile(avatar ripple @click="$router.push(`/market/${pluginOverview.id}`)" v-for="pluginOverview in pluginOverviews")
          v-list-tile-avatar
            img(:src="pluginOverview.thumbnailUrls[0]")
          v-list-tile-content
            v-list-tile-title {{ pluginOverview.name }}
            v-list-tile-sub-title {{ pluginOverview.description | less }}
          v-list-tile-action
            v-list-tile-action-text {{ pluginOverview.version }}

</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { PluginMeta } from '../model'
const Counter = require('@/plugin_examples/counter')
import PluginUploadForm from '@/components/market/PluginUploadForm.vue'

interface MarketCategory { name: string, icon: string }
interface MarketSortKey { name: string, icon: string, query: string }

@Component({
  components: { PluginUploadForm },
  watch: {
    searchText: _.debounce((v: string) => {
      console.log(v)
    }, 1500)
  },
  filters: {
    less (s: string): string {
      return s.slice(0, 14) + '...'
    }
  }
})
export default class PluginMarket extends Vue {
  private drawer: boolean = false

  private categories: MarketCategory[] = [
    { name: 'すべてのカテゴリ', icon: 'home' },
    { name: 'A', icon: 'home' },
    { name: 'B', icon: 'home' },
    { name: 'C', icon: 'home' },
    { name: 'D', icon: 'home' }
  ]
  private sortKeys: MarketSortKey[] = [
    { name: '人気順', icon: 'sort_by_alpha', query: '' },
    { name: '新着順', icon: 'sort_by_alpha', query: '' }
  ]

  private category: MarketCategory = this.categories[0]
  private sortKey: MarketSortKey = this.sortKeys[0]
  private searchText: string = ''

  private pluginOverviews: PluginMeta[] = [...Array(20)].map(() => Counter.meta)
}
</script>