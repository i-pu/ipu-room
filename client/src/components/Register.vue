<template lang="pug">
  div
    b-navbar(type="dark" variant="dark")
      b-navbar-brand へやつくるやつ

      b-navbar-nav
        b-nav-item
          b-form(inline)
            b-input-group
            b-form-input(v-model="nickName")
            b-input-group-append
              b-button(:disabled="nickName === ''" @click="register" variant="primary") 登録
        b-nav-item
          b-button(@click="$emit('makeroom')") 部屋を作る
</template>

<script>
export default {
  name: 'Lobby',
  data () {
    return {
      nickName: '',
    }
  },
  mounted () {
  },
  methods: {
    register () {
      if (this.nickName.includes(',')) {
        console.error('名前に,は使用できません')
        return
      }
      this.$emit('register', this.nickName)
    }
  }
}
</script>