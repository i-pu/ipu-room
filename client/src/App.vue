<template lang="pug">
  v-app
    v-content
      router-view
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

@Component<App>({
  // sockets: {
  //   connect () {
  //     this.$router.push('/')
  //   }
  // }
})
export default class App extends Vue {}
</script>
