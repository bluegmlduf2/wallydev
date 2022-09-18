import PostApi from '~/api/PostApi'

export const state = () => ({
  post: [],
})

export const mutations = {
  setPost: (state, payload) => {
    state.post = payload
  },
}

export const actions = {
  async getPosts({ commit }, payload) {
    // 게시물 정보 취득
    return await new PostApi()
      .getPosts(payload)
      .then((response) => {
        // 서버에서 가져온 게시물을 초기화
        commit('setPost', response)
      })
      .catch((e) => {
        console.warn(e)
      })
  },
  async getPostDetail({ commit }, payload) {
    // 게시물 상세 정보 취득
    return await new PostApi()
      .getPostDetail(payload)
      .then((response) => {
        // 서버에서 가져온 게시물을 초기화
        commit('setPost', response)
      })
      .catch((e) => {
        console.warn(e)
      })
  },
}

export const getters = {
  post(state) {
    return state.post
  },
}
