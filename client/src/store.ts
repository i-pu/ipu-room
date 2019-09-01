import Vuex, { Commit } from 'vuex'

export interface Session {
  userName: string
  userId: string
}

export default new Vuex.Store<Session>({
  state: {
    userName: '',
    userId: '',
  },
  getters: {
    userName (state: Session): string {
      return state.userName
    },
    userId (state: Session): string {
      return state.userId
    },
  },
  mutations: {
    userName (state: Session, payload: string) {
      state.userName = payload
    },
    userId (state: Session, payload: string) {
      state.userId = payload
    },
  },
  actions: {
    setUserName ({ commit }: { commit: Commit }, payload: string) {
      commit('userName', payload)
    },
    setUserId ({ commit }: { commit: Commit }, payload: string) {
      commit('userId', payload)
    },
  },
})
