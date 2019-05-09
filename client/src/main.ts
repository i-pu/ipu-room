import Vue from 'vue'
import './plugins/vuetify'
import store from './store'
import VueSocketIO from 'vue-socket.io-extended'
import io from 'socket.io-client'

if (!store.getters.localOnly) {
  // not working
  // console.log(process.env)
  const VUE_APP_API_DEV_ORIGIN = 'http://10.160.163.229:8000'
  const VUE_APP_API_ORIGIN = 'http://35.187.206.173:31420'
  Vue.use(VueSocketIO, io(VUE_APP_API_ORIGIN))
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
