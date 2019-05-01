import Vue from 'vue'
import Router from 'vue-router'

import Top from '@/views/Top.vue'
import Lobby from '@/views/Lobby.vue'
import Room from '@/views/Room.vue'

import 'vuetify/dist/vuetify.min'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Top',
      component: Top,
    },
    {
      path: '/lobby',
      name: 'Lobby',
      component: Lobby,
    },
    {
      path: '/room/:roomId',
      name: 'Room',
      component: Room,
    }
  ],
})
