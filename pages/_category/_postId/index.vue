<template>
  <v-container class="pa-10">
    <v-row no-gutters>
      <span class="text-h3 font-weight-bold">{{ post.title }}</span>
    </v-row>
    <v-row class="my-3 mx-1" align="center">
      <span class="text-subtitle-1 font-weight-light">{{ post.date }}</span>
      <span class="text-subtitle-1 font-weight-light ml-3">조회수 1</span>
      <v-spacer></v-spacer>
      <v-btn class="text-subtitle-1 font-weight-light ml-5" text small
        >수정</v-btn
      >
      <v-btn class="text-subtitle-1 font-weight-light ml-3" text small
        >삭제</v-btn
      >
    </v-row>
    <v-row no-gutters>
      <Viewer id="toastUiEditor" :initial-value="post.content" height="400px" />
    </v-row>
    <v-row no-gutters class="mt-3">
      <v-textarea
        solo
        no-resize
        hide-details
        label="댓글작성"
        rows="3"
        append-icon="mdi-comment"
        no
      ></v-textarea>
    </v-row>
    <v-divider class="my-7"></v-divider>
    <v-row>
      <v-card
        v-for="(item, index) in 5"
        :key="index"
        class="mx-3 my-2 card-no-border"
        width="100%"
        outlined
      >
        <v-list-item>
          <v-list-item-content>
            <div class="text-h6">댓글작성자1</div>
            <div class="text-caption mb-4">2022.01.01</div>
            <v-list-item-subtitle class="text-body-1"
              >Greyhound divisely hello coldly
              fonwderfully</v-list-item-subtitle
            >
          </v-list-item-content>
        </v-list-item>
        <v-card-actions>
          <v-btn outlined rounded text> 수정 </v-btn>
          <v-btn outlined rounded text> 삭제 </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import '@toast-ui/editor/dist/toastui-editor-viewer.css'
import { Viewer } from '@toast-ui/vue-editor'

export default {
  name: 'IndexPostDetail',
  components: {
    Viewer,
  },
  async asyncData({ params, store }) {
    const postId = params.postId
    await store.dispatch('getPostDetail', postId)
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
  },
}
</script>
<style scoped>
.card-no-border {
  border: 0 !important;
}
</style>