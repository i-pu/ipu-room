import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLocalOnly: true,
    userName: '',
    userId: ''
  },
  mutations: {
    userName (state, payload: string) {
      state.userName = payload
    },
    userId (state, payload: string) {
      state.userId = payload
    }
  },
  getters: {
    localOnly (state) {
      return state.isLocalOnly
    },
    userName (state) {
      return state.userName
    },
    userId (state) {
      return state.userId
    }
  },
  actions: {
    setUserName ({ commit }, payload) {
      commit('userName', payload)
    },
    setUserId ({ commit }, payload) {
      commit('userId', payload)
    }
  }
})
