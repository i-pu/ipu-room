
<template lang="pug">
  div
    vue-p5(
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
  methods: {
    mouseDragged ({ mouseX, mouseY, pmouseX, pmouseY }) {
      this.lines.push({ mouseX, mouseY, pmouseX, pmouseY })
    },
    setup (sketch) {
      sketch.createCanvas(400, 400)
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
desk-canvas {
  width: 100%;
  height: 100%;
}
</style>