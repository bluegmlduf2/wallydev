import PostApi from '~/api/PostApi'
import PostListApi from '~/api/PostListApi'

export const state = () => ({
  post: null,
  postList: [],
  authUser: null,
})

export const mutations = {
  SET_POST: (state, payload) => {
    state.post = payload
  },
  SET_POST_LIST: (state, payload) => {
    state.postList = payload
  },
  ADD_POST_LIST: (state, payload) => {
    state.postList = [...state.postList, ...payload]
  },
  SET_COMMENT_OPEN: (state, payload) => {
    // 댓글을 수정상태로 변경
    state.post.comment = state.post.comment.map((e) =>
      e.commentId === payload.commentId
        ? { ...e, isUpdated: payload.isUpdated }
        : e
    )
  },
  // stateを空にします
  RESET_STORE(state) {
    state.authUser = null
  },
  // stateにpayloadをセットします
  SET_USER(state, { authUser, claims }) {
    state.authUser = {
      uid: authUser.uid,
      email: authUser.email,
      emailVerified: authUser.emailVerified,
      displayName: authUser.displayName,
      photoURL: claims.picture,
      isAdmin: authUser.email === process.env.VUE_APP_ADMIN_EMAIL,
    }
  },
}

export const actions = {
  async nuxtServerInit({ dispatch }, ctx) {
    if (this.$fire.auth === null) {
      // throw 'nuxtServerInit Example not working - this.$fire.auth cannot be accessed.'
    }

    if (ctx.$fire.auth === null) {
      // throw 'nuxtServerInit Example not working - ctx.$fire.auth cannot be accessed.'
    }

    if (ctx.app.$fire.auth === null) {
      // throw 'nuxtServerInit Example not working - ctx.$fire.auth cannot be accessed.'
    }

    if (ctx.res && ctx.res.locals && ctx.res.locals.user) {
      const { allClaims: claims, ...authUser } = ctx.res.locals.user

      // console.info(
      //   'Auth User verified on server-side. User: ',
      //   authUser,
      //   'Claims:',
      //   claims
      // )

      await dispatch('onAuthStateChanged', {
        authUser,
        claims,
      })
    }
  },

  async onAuthStateChanged({ commit }, { authUser, claims }) {
    if (!authUser) {
      // ログアウトしたらページ遷移します
      await this.$router.push('/')
      commit('RESET_STORE')
      return
    }

    // if (authUser && claims) {
    //   try {
    //     // ログインしたらページ遷移します
    //     await this.$router.push('/')
    //   } catch (e) {
    //     console.error(e)
    //   }
    // }

    commit('SET_USER', { authUser, claims })
  },

  async getPostList({ commit }, payload) {
    // 게시물 리스트 정보 취득
    return await new PostListApi()
      .getPostList(payload)
      .then((response) => {
        // 최초 게시물을 초기화시
        if (payload.page === 1) {
          commit('SET_POST_LIST', response.data)
        } else if (payload.page > 1) {
          // 스크롤에 의해 게시물 더보기시
          commit('ADD_POST_LIST', response.data)
        }
        // 남은 게시글수 반환
        return response?.data.length || 0
      })
      .catch((e) => {
        console.warn(e)
      })
  },

  async getPost({ commit }, payload) {
    // 게시물 상세 정보 취득
    return await new PostApi()
      .getPost(payload)
      .then((response) => {
        // 서버에서 가져온 게시물을 초기화
        commit('SET_POST', response.data)
      })
      .catch((e) => {
        console.warn(e)
      })
  },

  async createPost({ commit }, payload) {
    // 게시물 등록
    return await new PostApi()
      .createPost(payload)
      .then((response) => {
        const data = { ...response.data }
        // 작성한 게시물로 이동
        this.$router.push(`${data.category}/${data.postId}`)
      })
  },
}

export const getters = {
  post(state) {
    return state.post
  },
  postList(state) {
    return state.postList
  },
  isLoggedIn: (state) => !!state?.authUser,
  isAdminIn: (state) => !!state?.authUser?.isAdmin,
}
