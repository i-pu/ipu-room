import Vue from 'vue'
import Router, { Route } from 'vue-router'
import store from '@/store'

import Top from '@/views/Top.vue'
import Lobby from '@/views/Lobby.vue'
import Room from '@/views/Room.vue'
import PluginMarket from '@/views/PluginMarket.vue'
import PluginDetail from '@/views/PluginDetail.vue'

Vue.use(Router)

const router = new Router({
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
    },
    {
      path: '/market',
      name: 'PluginMarket',
      component: PluginMarket,
    },
    {
      path: '/market/:pluginId',
      name: 'PluginDetail',
      component: PluginDetail,
    },
  ],
})

router.beforeEach((to, from, next) => {
  if (from.path !== '/' && !store.getters.userId) {
    next('/')
  } else {
    next()
  }
})

export default router
