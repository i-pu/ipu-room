import Vue from 'vue'
import Router from 'vue-router'

import Top from '@/views/Top.vue'
import About from '@/views/About.vue'
import Lobby from '@/views/Lobby.vue'
import Room from '@/views/Room.vue'
import PluginMarket from '@/views/PluginMarket.vue'
import PluginDetail from '@/views/PluginDetail.vue'

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
      path: '/about',
      name: 'About',
      component: About,
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

// router.beforeEach((to, from, next) => {
//   if (from.path !== '/' && !store.getters.userId) {
//     next('/')
//   } else {
//     next()
//   }
// })

export default router
