
<template lang="pug">
  #desk
    vue-p5(
      ref="p5canvas"
      @setup="setup" 
      @draw="draw"
      @keypressed="keyPressed"
      @mousemoved="mouseMoved"
      @mousedragged="mouseDragged"
    )
</template>

<script>
import VueP5 from "vue-p5"

export default {
  name: 'Desk',
  components: { VueP5 },
  data () {
    return {
      lines: []
    }
  },
  mounted() {
    const { clientWidth, clientHeight } = this.$refs.p5canvas.$el
    console.log(`${clientWidth} x ${clientHeight}`)
  },
  methods: {
    mouseDragged ({ mouseX, mouseY, pmouseX, pmouseY }) {
      this.lines.push({ mouseX, mouseY, pmouseX, pmouseY })
    },
    setup (sketch) {
      const { clientWidth, clientHeight } = this.$refs.p5canvas.$el
      sketch.createCanvas(clientWidth, clientHeight)
      sketch.background(255)
    },
    draw (sketch) {
      for(const line of this.lines) {
        sketch.line(line.pmouseX, line.pmouseY, line.mouseX, line.mouseY)
      }
    }
  },
}
</script>

<style scoped>
#desk {
  height: 100%;
}

#desk div {
  height: 100%;
}
</style>