import Vue from 'vue'
import './plugins/vuetify'
import store from './store'
import VueSocketIO from 'vue-socket.io-extended'
import io from 'socket.io-client'

if (!store.getters.localOnly) {
  Vue.use(VueSocketIO, io(process.env.VUE_APP_API_ORIGIN))
}
Vue.config.productionTip = false

import App from './App.vue'
import router from './router'

router.push('/')

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
