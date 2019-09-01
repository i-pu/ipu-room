import Vue from 'vue'
import VueCompositionApi from '@vue/composition-api'
import Vuetify from 'vuetify/lib'

import 'vuetify/dist/vuetify.min'
import '@fortawesome/fontawesome-free/css/all.css'

import store from '@/store'
import App from '@/App.vue'
import router from '@/router'

Vue.use(Vuetify, { iconfont: 'md' })

Vue.use(VueCompositionApi)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
