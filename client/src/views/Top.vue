<template lang='pug'>
  div
    v-parallax(dark src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg")
      v-layout(align-center column justify-center)
        h1.display-2.font-weight-thin.mb-3 Heya
        h4.subheading Please make room

        v-spacer
        
        v-flex
          v-card(white)
            v-card-text
              v-layout(align-center)
                v-text-field(placeholder="Your name")
                v-btn(color="blue-grey" class="white--text" @click="toLobby") Lobby
                  v-icon(right dark) arrow_right_alt
</template>

<script>
export default {
  name: '',
  data () {
    return { }
  },
  created () {},
  methods: {
    toLobby () {
      this.$router.push('/lobby')
    }
  }
}
</script>

<style scoped lang='stylus'>

</style>