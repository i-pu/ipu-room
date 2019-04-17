import Vue from 'vue'
import Router from 'vue-router'

import Top from '@/views/Top'
import Lobby from '@/views/Lobby'
import Room from '@/views/Room'

import 'vuetify/dist/vuetify.min'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Top',
      component: Top
    },
    {
      path: '/lobby',
      name: 'Lobby',
      component: Lobby
    },
    {
      path: '/room',
      name: 'Room',
      component: Room
    }
  ]
})