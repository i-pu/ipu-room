import Vue from 'vue'
import './plugins/vuetify'
// import VueSocketIO from 'vue-socket.io'

// Vue.use(new VueSocketIO({
//   connection: 'http://10.160.163.229:8000',
//   // options: { path: '/socket.io/' }
// }))

Vue.productionTip = false

import App from './App'

import router from './router'

router.push('/lobby/1234')

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
