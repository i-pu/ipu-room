
<template lang="pug">
  #desk
    div(v-html="customHTML")
</template>

<script>

export default {
  name: 'Desk',
  data () {
    return {
      customHTML: '<p>Hello, Plugin</p>'
    }
  },
  sockets: {
    render (html) {
      this.customHTML = html
    }
  },
  mounted() {

  },
  methods: {
  },
}
</script>