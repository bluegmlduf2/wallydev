<template>
  <v-container v-if="post" class="pa-md-10 pa-lg-10">
    <v-row no-gutters>
      <span class="text-h3 font-weight-bold">{{ post.title }}</span>
    </v-row>
    <v-row class="my-3 mx-1" align="center">
      <span class="text-subtitle-1 font-weight-light">{{
        post.createdDate
      }}</span>
      <span class="text-subtitle-1 font-weight-light ml-2"
        >조회수 {{ post.postViewCount }}</span
      >
      <v-spacer></v-spacer>
      <div v-if="isLoggedIn && isAdminIn">
        <v-btn
          class="text-subtitle-1 font-weight-light px-0"
          text
          small
          @click="updatePost(post.postId)"
          >수정</v-btn
        >
        <v-btn
          class="text-subtitle-1 font-weight-light px-0"
          text
          small
          @click="deletePost(post.postId)"
          >삭제</v-btn
        >
      </div>
    </v-row>
    <v-row no-gutters class="my-5">
      <tiptap-viewer id="post-content" :content="post.content" />
    </v-row>
    <v-row v-if="isLoggedIn" no-gutters class="mt-3">
      <v-textarea
        v-model="commentContent"
        solo
        no-resize
        hide-details
        label="댓글을 입력해주세요"
        rows="3"
        append-icon="mdi-arrow-left-bottom-bold"
        no
        @click:append="writeComment"
      ></v-textarea>
    </v-row>
    <v-divider class="my-7"></v-divider>
    <v-row>
      <v-card
        v-for="item in post.comment"
        :key="item.commentId"
        class="mx-3 my-2 card-no-border comment-wrapper"
        width="100%"
        outlined
      >
        <v-list-item>
          <v-list-item-content class="pt-5 pb-0">
            <div class="text-h6">{{ item.writerUserName }}</div>
            <div class="text-caption mb-4">{{ item.createdDate }}</div>
            <v-textarea
              class="text-body-1 comment-content"
              flat
              solo
              :outlined="!item.isUpdated"
              :readonly="item.isUpdated"
              :value="item.commentContent"
              no-resize
              rows="1"
              dense
              :auto-grow="true"
              placeholder="댓글을 입력해주세요"
            />
          </v-list-item-content>
        </v-list-item>
        <v-card-actions v-if="isLoggedIn && item.commentUserAuth">
          <v-btn
            outlined
            rounded
            text
            @click="
              item.isUpdated
                ? changeCommentOpen(item, false)
                : updateComment(item, $event)
            "
          >
            {{ item.isUpdated ? '수정' : '저장' }}
          </v-btn>
          <v-btn
            outlined
            rounded
            text
            @click="
              item.isUpdated
                ? deleteComment(item)
                : changeCommentOpen(item, true)
            "
          >
            {{ item.isUpdated ? '삭제' : '취소' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <Alert
      :is-open="isOpen"
      :dialog-message="dialogMessage"
      :dialog-type="dialogType"
      @closeDialog="isOpen = false"
    />
  </v-container>
</template>

<script>
import TiptapViewer from '~/components/TiptapViewer.vue'
import message from '~/assets/js/message'

export default {
  name: 'IndexPostDetail',
  components: {
    TiptapViewer,
  },
  data() {
    return {
      isOpen: false,
      dialogMessage: '',
      dialogType: '',
      commentContent: '',
    }
  },
  async fetch() {
    const postId = this.$route.params.postId
    await this.$store.dispatch('getPost', postId)
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
    isLoggedIn() {
      return this.$store.getters?.isLoggedIn
    },
    isAdminIn() {
      return this.$store.getters?.isAdminIn
    },
  },
  methods: {
    updatePost(postId) {
      this.$router.push({ name: 'write', params: { postId } })
    },
    async deletePost(postId) {
      // 게시글을 삭제
      await this.$store
        .dispatch('deletePost', postId)
        .catch((e) => {
          // 서버에서 에러가 발생했을때
          this.isOpen = true
          this.dialogType = 'error'
          this.dialogMessage = e.message
        })
        .finally(() => {
          this.$store.commit('SET_LOADING', false)
        })
    },
    async writeComment() {
      // 작성한 댓글의 정보
      const param = {
        postId: this.post.postId,
        commentContent: this.commentContent,
      }

      // 화면에서 유효성 체크
      if (!param.commentContent) {
        this.isOpen = true
        this.dialogType = 'error'
        this.dialogMessage = message.inputAll
        return
      }
      // 댓글을 등록
      await this.$store
        .dispatch('createComment', param)
        .then((response) => {
          // 댓글등록확인
          this.isOpen = true
          this.dialogType = 'info'
          this.dialogMessage = response.message
          this.commentContent = ''
          this.$fetch() // 댓글 정보 초기화
        })
        .catch((e) => {
          // 서버에서 에러가 발생했을때
          this.isOpen = true
          this.dialogType = 'error'
          this.dialogMessage = e.message
        })
        .finally(() => {
          this.$store.commit('SET_LOADING', false)
        })
    },
    async updateComment(comment, $event) {
      // 수정한 댓글의 정보
      const param = {
        commentId: comment.commentId,
        commentContent: $event.target
          .closest('.comment-wrapper')
          .querySelector('.comment-content textarea').value,
      }

      // 화면에서 유효성 체크
      if (!param.commentContent) {
        this.isOpen = true
        this.dialogType = 'error'
        this.dialogMessage = message.inputAll
        return
      }

      // 댓글을 수정
      await this.$store
        .dispatch('updateComment', param)
        .then((response) => {
          // 댓글등록확인
          this.isOpen = true
          this.dialogType = 'info'
          this.dialogMessage = response.message
          this.commentContent = ''
          this.$fetch() // 댓글 정보 초기화
        })
        .catch((e) => {
          // 서버에서 에러가 발생했을때
          this.isOpen = true
          this.dialogType = 'error'
          this.dialogMessage = e.message
        })
        .finally(() => {
          this.$store.commit('SET_LOADING', false)
        })
    },
    async deleteComment(comment) {
      // 댓글을 삭제
      await this.$store
        .dispatch('deleteComment', comment.commentId)
        .then((response) => {
          // 댓글삭제확인
          this.isOpen = true
          this.dialogType = 'info'
          this.dialogMessage = response.message
          this.commentContent = ''
          this.$fetch() // 댓글 정보 초기화
        })
        .catch((e) => {
          // 서버에서 에러가 발생했을때
          this.isOpen = true
          this.dialogType = 'error'
          this.dialogMessage = e.message
        })
        .finally(() => {
          this.$store.commit('SET_LOADING', false)
        })
    },
    changeCommentOpen(comment, isActive) {
      this.$store.commit('SET_COMMENT_OPEN', {
        ...comment,
        isUpdated: isActive,
      })
    },
  },
}
</script>
<style scoped>
.card-no-border {
  border: 0 !important;
}
/* 행간 */
#post-content {
  line-height: 1.75rem;
}
</style>