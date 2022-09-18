import PostApi from '~/api/PostApi'

export const state = () => ({
  post: [],
})

export const actions = {
  async getPosts({ commit }, payload) {
    // 게시물 정보 취득
    return await new PostApi()
      .getPosts(payload)
      .then((response) => {
        // 서버에서 가져온 게시물을 초기화
        commit('setPost', response.data);
      })
      .catch((e) => {
        console.warn(e)
      })
  },
}

export const mutations = {
  setPost: (state, payload) => {
    state.comments = payload
  },
}

export const getters = {
  post(state) {
    return state.post
  },
}
