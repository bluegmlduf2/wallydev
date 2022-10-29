<template>
  <v-container v-if="!!postList">
    <v-row class="mb-6" justify="start">
      <v-col
        v-for="e in postList"
        :key="e.postId"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card max-width="344" class="hover-up">
          <v-img :src="e.imageUrl" height="200px"></v-img>
          <v-card-title> {{ e.title }} </v-card-title>
          <v-card-subtitle class="subtitle-body text-overflow">
            {{ e.content }}
          </v-card-subtitle>
          <v-card-actions class="d-flex justify-end">
            <v-btn color="maincolor" text nuxt :to="`${category}/${e.postId}`">
              더보기
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <br />
    <InfiniteLoading @infinite="scrolling"></InfiniteLoading>
  </v-container>
</template>

<script>
export default {
  name: 'IndexCategory',
  data() {
    return {
      category: '',
      page: 1,
    }
  },
  async fetch() {
    this.category = this.$route.params.category
    await this.$store.dispatch('getPostList', {
      category: this.category,
      page: 1,
    })
  },
  computed: {
    postList() {
      return this.$store.getters.postList
    },
  },
  fetchOnServer: false, // fetch함수의 실행을 위해 이 화면의 경우는 서버에서 렌더링을 하지않고 클라이언트에서 한다
  methods: {
    scrolling($state) {
      // 스크롤이 페이지 하단에 위치해도 약간의 딜레이를 주고 데이터를 가져옴
      setTimeout(async () => {
        this.page++
        // 게시글 더 가져오기
        const isMoreData = await this.$store.dispatch('getPostList', {
          category: this.category,
          page: this.page,
        })

        // 남은 데이터 존재여부에 따라 스크롤표시
        if (isMoreData) {
          $state.loaded()
        } else {
          $state.complete()
        }
      }, 500)
    },
  },
}
</script>

<style scoped>
.hover-up:hover {
  transform: translateY(-8px);
  transition: transform 0.25s ease-in 0s;
}
.subtitle-body {
  max-height: 70px;
  min-height: 70px;
}
</style>