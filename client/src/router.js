import Vue from 'vue'
import Router from 'vue-router'

import Top from '@/views/Top'
import Lobby from '@/views/Lobby'
import Room from '@/views/Room'

import PluginCreateForm from '@/components/PluginCreateForm'

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
      path: '/lobby/:userId',
      name: 'Lobby',
      component: Lobby
    },
    {
      path: '/room/:roomId',
      name: 'Room',
      component: Room
    },
    {
      path: '/test',
      name: 'PluginCreateForm',
      component: PluginCreateForm
    }
  ]
})