import Vue from 'vue'
import Router from 'vue-router'
import Lobby from '@/views/Lobby'
import Room from '@/views/Room'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
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