import Vue from 'vue'
import Vuex from 'vuex'

import modals from './modals'
import dimens from './dimens'
import auth from './auth'
import image from './image'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    modals: modals,
    dimens: dimens,
    auth: auth,
    image: image,
  }
});