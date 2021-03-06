export const state = () => ({
  image: ''
})

export const mutations = {
  SET_IMAGE(state, name) {
    state.image = name
  },
}

export const actions = {
  setImage({commit}, name) {
    commit('SET_IMAGE', name)
  }
}
