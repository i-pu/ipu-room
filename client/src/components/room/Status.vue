<template lang='pug'>
  div
    v-container(grid-list-md)
      v-layout(row wrap)
        v-flex(xs12)
          v-subheader メンバー
        v-flex(v-for="member, i in members" :key="i" xs4 md4)

          v-card.d-flex.align-center(
            height="200"
          )
            // v-img(:src="member.avatar_url")
            v-card-title(primary-title)
              .headline {{ member.name }}
            v-card-actions
</template>

<script>
export default {
  name: 'Status',
  props: {
    members: Array
  },
  methods: {

  }
}
</script>