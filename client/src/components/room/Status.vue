<template lang='pug'>
  div
    v-container(grid-list-md)
      v-layout(row wrap)
        v-flex(xs12)
          v-subheader メンバー
        v-flex(v-for="i in 6" :key="i" xs2 md2)
          v-card.d-flex.align-center(
            v-if="members[i - 1]"
            height="200"
          )
            // v-img(:src="member.avatarUrl")
            v-card-title(primary-title)
              .headline {{ members[i - 1].name }}
            v-card-actions

          v-card.d-flex.align-center(
            v-else
            dark height="200"
          )
            // v-img(:src="member.avatarUrl")
            v-card-title(primary-title)
              .headline 無人
            v-card-actions
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { User } from '@/model'

@Component
export default class Status extends Vue {
  @Prop() public members!: User[]
}
</script>