import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueSocketIO from 'vue-socket.io'
Vue.use(BootstrapVue)
Vue.use(new VueSocketIO({
  connection: 'http://localhost:8000',
  options: { path: '/socket.io/' }
}))

import App from './App'

new Vue({
  render: h => h(App),
}).$mount('#app')
