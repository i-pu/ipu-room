import Vue from 'vue'
import Vuex, { Commit } from 'vuex'
import { PPM, PluginComponent } from '@/logic/plugin/component'

Vue.use(Vuex)

export interface State {
  isLocalOnly: boolean
  userName: string
  userId: string
  ppm: PPM | null
}

const state: State = {
  isLocalOnly: true,
  userName: '',
  userId: '',
  ppm: null,
}

export const getters = {
  localOnly (state: State) {
    return state.isLocalOnly
  },
  userName (state: State) {
    return state.userName
  },
  userId (state: State) {
    return state.userId
  },
  plugins (state: State): Record<string, PluginComponent> {
    return state.ppm ? state.ppm.plugins : {}
  }
}

const mutations = {
  userName (state: State, payload: string) {
    state.userName = payload
  },
  userId (state: State, payload: string) {
    state.userId = payload
  }
}

export const actions = {
  setUserName ({ commit }: { commit: Commit }, payload: string) {
    commit('userName', payload)
  },
  setUserId ({ commit }: { commit: Commit }, payload: string) {
    commit('userId', payload)
  },
  async enterRoom ({ commit, state }: { commit: Commit, state: State }, payload: string[]) {
    state.ppm = new PPM(payload)
    console.log('set plugin')
    if (state.ppm) {
      await state.ppm.installPlugins()
      console.log('installed')
    }
  }
}

export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})
