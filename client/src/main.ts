import Vue from 'vue'
import './plugins/vuetify'
import store from './store'
import VueSocketIO from 'vue-socket.io-extended'
import io from 'socket.io-client'

import 'vuetify/dist/vuetify.min'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.use(VueSocketIO, io(process.env.VUE_APP_SOCKET_ORIGIN!!, {
  path: process.env.VUE_APP_SOCKET_PATH
}))
Vue.config.productionTip = false

import App from './App.vue'
import router from './router'

router.push('/')

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
