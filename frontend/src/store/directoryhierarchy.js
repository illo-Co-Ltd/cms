import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    message: 'Hello'
  },
  mutations: {
    changeMessage (state, newMsg) {
      state.message = newMsg
    }

  },
  actions: {
    callMutation ({ commit }, { newMsg }) {
      commit('changeMessage', newMsg)
    }
  },
  getters: {
    getMsg (state) {
      return `${state.message} => Length : ${state.message.length}`
    }
  }
})