<template lang="pug">
  #app
    lobby
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Lobby from './components/Lobby'

export default {
  name: 'App',
  components: { Lobby }
}
</script>
