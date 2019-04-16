<template lang='pug'>
  div
    b-container
      b-row
        b-col#header
      b-row
        b-col#desk(cols="9")
          canvas(width="640" height="360")
        b-col#chat(cols="3")
      b-row
        b-col#status(cols="12")
</template>

<script>
export default {
  name: 'Room',
  data () {
    return {

    }
  },
  methods: { }
}
</script>

<style scoped>
#header {
  width: 100%;
  height: 5vh;
  background-color: cyan;
}

#desk {
  width: 100%;
  height: 100%;
  padding: 0;
  background-color: aliceblue;
}

#desk canvas {
  width: 100%;
  height: 100%;
}

#chat {
  width: 100%;
  height: auto;
  background-color: turquoise;
}

#status {
  width: 100%;
  height: 30vh;
  background-color: blanchedalmond;
}
</style>
