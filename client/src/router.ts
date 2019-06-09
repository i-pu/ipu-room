import Vue from 'vue'
import Router, { Route } from 'vue-router'
import store from '@/store'

import Top from '@/views/Top.vue'
import Lobby from '@/views/Lobby.vue'
import Room from '@/views/Room.vue'
import PluginDetail from '@/views/PluginDetail.vue'

import 'vuetify/dist/vuetify.min'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Top',
      component: PluginDetail,
      // component: Top,
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
    },
    {
      path: '/editor',
      name: 'Editor',
      component: PluginDetail,
    }
  ],
})

export default router
