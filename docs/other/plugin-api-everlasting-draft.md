# Plugin API Everlasting Draft

## 
```html
<template>
  <h3> 履歴 </h3>
  <p v-for="rec, i in history">{{ i }}: {{ rec.name }} さん {{ rec.score }} 点</p>
</template>
<script lang="ts">
({
  await initialize() {
    this.record.history = await this.$everLasting.fetch('/history')
  },

  updateRanking(name: string, score: number) {
    this.$everLasting.push('/history', { name, score })
  }

  @Hook('everLasting/push')
})
</script>
```