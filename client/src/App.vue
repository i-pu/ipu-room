<template lang="pug">
  v-app
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span へやつくるやつ
      v-spacer
      v-btn(
        color="error"
        href="#"
        target="_blank"
      ) 退出

    v-content
      router-view
</template>

<script>
export default {
  name: 'App'
}
</script>
