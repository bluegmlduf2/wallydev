import sanitizeHtml from 'sanitize-html'
import PostApi from '~/api/PostApi'
import ImageApi from '~/api/ImageApi'
import PostListApi from '~/api/PostListApi'
import CommentApi from '~/api/CommentApi'

export const state = () => ({
  post: null,
  postList: [],
  isLoading: false,
  authUser: null,
})

export const mutations = {
  SET_POST: (state, payload) => {
    state.post = payload
  },
  POST_CLEAR: (state) => {
    state.post = null
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
      isAdmin: authUser.email === "bluegmlduf2@gmail.com",
    }
  },
  SET_LOADING: (state, payload) => {
    state.isLoading = payload
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

    commit('SET_USER', { authUser, claims })
  },

  async getPostList({ commit }, payload) {
    // 게시물 리스트 정보 취득
    return await new PostListApi()
      .getPostList(payload)
      .then((response) => {
        // content의 불필요한 HTML을 제거, v-html사용은 xss에 취약
        const responseData = response.data.map((e) => {
          // 게시글 리스트의 타이틀 이미지 추출부분
          const imageSrc = e.content.match(/<img [^>]*src="[^"]*"[^>]*>/gm)
          let displayImage = null
          if (imageSrc) {
            displayImage = imageSrc.map((x) =>
              x.replace(/.*src="([^"]*)".*/, '$1')
            )[0]
          }
          // const displayImage = rawText.match(/src=([^]+)/);
          return {
            ...e,
            content: sanitizeHtml(e.content, {
              // 어떤 태그들도 표시를 허용하지 않음
              allowedTags: [],
              allowedAttributes: {},
            }),
            displayImage,
          }
        })
        // 최초 게시물을 초기화시
        if (payload.page === 1) {
          commit('SET_POST_LIST', responseData)
        } else if (payload.page > 1) {
          // 스크롤에 의해 게시물 더보기시
          commit('ADD_POST_LIST', responseData)
        }
        // 남은 게시글수 반환
        return response?.data.length || 0
      })
      .catch((e) => {
        console.warn(e)
      })
  },

  async getPost({ commit }, payload) {
    commit('SET_LOADING', true)
    // 게시물 상세 정보 취득
    commit('POST_CLEAR')
    return await new PostApi()
      .getPost(payload)
      .then((response) => {
        // 서버에서 가져온 게시물을 초기화
        commit('SET_POST', response.data)
      })
      .catch((e) => {
        console.warn(e)
      })
      .finally(() => {
        commit('SET_LOADING', false)
      })
  },

  async createPost({ commit }, payload) {
    commit('SET_LOADING', true)
    // 게시물 등록
    return await new PostApi().createPost(payload).then((response) => {
      const data = { ...response.data }
      // 작성한 게시물로 이동
      this.$router.push(`${data.category}/${data.postId}`)
    })
  },

  async updatePost({ commit }, payload) {
    commit('SET_LOADING', true)
    // 게시물 수정
    return await new PostApi().updatePost(payload).then((response) => {
      const data = { ...response.data }
      // 작성한 게시물로 이동
      this.$router.push(`${data.category}/${data.postId}`)
    })
  },

  // 게시물 이미지 등록
  async uploadImage({ commit }, payload) {
    commit('SET_LOADING', true)
    // 게시물 이미지 정보 등록
    return await new ImageApi().uploadImage(payload)
  },

  async deletePost({ commit }, payload) {
    commit('SET_LOADING', true)
    // 게시물 삭제
    return await new PostApi().deletePost(payload).then(() => {
      // 삭제후 홈화면으로 게시물로 이동
      this.$router.push('/')
    })
  },

  async createComment({ commit }, payload) {
    commit('SET_LOADING', true)
    // 댓글 등록
    return await new CommentApi().createComment(payload)
  },

  async updateComment({ commit }, payload) {
    commit('SET_LOADING', true)
    // 댓글 수정
    return await new CommentApi().updateComment(payload)
  },

  async deleteComment({ commit }, payload) {
    commit('SET_LOADING', true)
    // 댓글 삭제
    return await new CommentApi().deleteComment(payload)
  },
}

export const getters = {
  post(state) {
    return state.post
  },
  postList(state) {
    return state.postList
  },
  isLoading(state) {
    return state.isLoading
  },
  isLoggedIn: (state) => !!state?.authUser,
  isAdminIn: (state) => !!state?.authUser?.isAdmin,
}
