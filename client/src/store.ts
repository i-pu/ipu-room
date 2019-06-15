import Vue from 'vue'
import Vuex, { Commit } from 'vuex'

Vue.use(Vuex)

export interface State {
  userName: string
  userId: string
}

const storeState: State = {
  userName: '',
  userId: '',
}

const getters = {
  userName (state: State) {
    return state.userName
  },
  userId (state: State) {
    return state.userId
  },
}

const mutations = {
  userName (state: State, payload: string) {
    state.userName = payload
  },
  userId (state: State, payload: string) {
    state.userId = payload
  },
}

const actions = {
  setUserName ({ commit }: { commit: Commit }, payload: string) {
    commit('userName', payload)
  },
  setUserId ({ commit }: { commit: Commit }, payload: string) {
    commit('userId', payload)
  },
}

export default new Vuex.Store({
  state: storeState,
  mutations,
  getters,
  actions,
})
