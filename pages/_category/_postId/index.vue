<template>
  <v-container class="pa-md-10 pa-lg-10">
    <v-row no-gutters>
      <span class="text-h3 font-weight-bold">{{ post.title }}</span>
    </v-row>
    <v-row class="my-3 mx-1" align="center">
      <span class="text-subtitle-1 font-weight-light">{{ post.postDate }}</span>
      <span class="text-subtitle-1 font-weight-light ml-2"
        >조회수 {{ post.readCount }}</span
      >
      <v-spacer></v-spacer>
      <div v-if="isLoggedIn && isAdminIn">
        <v-btn
          class="text-subtitle-1 font-weight-light px-0"
          text
          small
          @click="updatePost(post)"
          >수정</v-btn
        >
        <v-btn
          class="text-subtitle-1 font-weight-light px-0"
          text
          small
          @click="deletePost(post)"
          >삭제</v-btn
        >
      </div>
    </v-row>
    <v-row no-gutters class="my-5">
      <tiptap-viewer id="post-content" :content="post.postContent" />
    </v-row>
    <v-row v-if="isLoggedIn" no-gutters class="mt-3">
      <v-textarea
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
        :key="item.id"
        class="mx-3 my-2 card-no-border"
        width="100%"
        outlined
      >
        <v-list-item>
          <v-list-item-content class="pt-5 pb-0">
            <div class="text-h6">{{ item.commentUserName }}</div>
            <div class="text-caption mb-4">{{ item.commentDate }}</div>
            <v-textarea
              class="text-body-1 comment-content"
              flat
              solo
              :outlined="!item.isUpdate"
              :readonly="item.isUpdate"
              :value="item.commentContent"
              no-resize
              rows="1"
              dense
              :auto-grow="true"
              placeholder="댓글을 입력해주세요"
            />
          </v-list-item-content>
        </v-list-item>
        <v-card-actions v-if="isLoggedIn && item.isMe">
          <v-btn
            outlined
            rounded
            text
            @click="
              item.isUpdate
                ? changeCommentOpen(item, false)
                : updateComment(item)
            "
          >
            {{ item.isUpdate ? '수정' : '저장' }}
          </v-btn>
          <v-btn
            outlined
            rounded
            text
            @click="
              item.isUpdate
                ? deleteComment(item)
                : changeCommentOpen(item, true)
            "
          >
            {{ item.isUpdate ? '삭제' : '취소' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <Alert
      :is-open="isOpen"
      :dialog-message="dialogMessage"
      @closeDialog="isOpen = false"
    />
  </v-container>
</template>

<script>
import TiptapViewer from '~/components/TiptapViewer.vue'

export default {
  name: 'IndexPostDetail',
  components: {
    TiptapViewer,
  },
  async asyncData({ params, store }) {
    const postId = params.postId
    await store.dispatch('getPostDetail', postId)
  },
  data() {
    return {
      isOpen: false,
      dialogMessage: '',
    }
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
    writeComment() {
      this.isOpen = true
      this.dialogMessage = '성공메세지야 떠라'
    },
    updatePost(post) {
      this.$router.push({ name: 'write', params: { post }, props: true })
    },
    deletePost(post) {
      alert(3)
    },
    updateComment(comment) {
      this.changeCommentOpen(comment, true)
      alert(2)
    },
    deleteComment(comment) {
      alert(3)
    },
    changeCommentOpen(comment, isActive) {
      this.$store.commit('SET_COMMENT_OPEN', {
        ...comment,
        isUpdate: isActive,
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