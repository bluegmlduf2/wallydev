<template>
  <v-container>
    <v-row class="mb-6" justify="start">
      <v-col v-for="e in post" :key="e.id" cols="12" sm="6" md="4" lg="3">
        <v-card max-width="344" class="hover-up">
          <v-img :src="e.imageUrl" height="200px"></v-img>
          <v-card-title> {{ e.title }} </v-card-title>
          <v-card-subtitle class="subtitle-body text-overflow">
            {{ e.content }}
          </v-card-subtitle>
          <v-card-actions class="d-flex justify-end">
            <v-btn color="maincolor" text nuxt :to="`${category}/${e.id}`">
              더보기
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <br />
    <InfiniteLoading v-if="post.length" @infinite="scrolling"></InfiniteLoading>
  </v-container>
</template>

<script>
export default {
  name: 'IndexCategory',
  async asyncData({ params, store }) {
    const category = params.category
    await store.dispatch('getPosts', { category, page: 1 })

    return { category }
  },
  data() {
    return {
      category: '',
      page: 1,
    }
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
  },
  methods: {
    scrolling($state) {
      // 스크롤이 페이지 하단에 위치해도 약간의 딜레이를 주고 데이터를 가져옴
      setTimeout(async () => {
        this.page++
        // 게시글 더 가져오기
        const isMoreData = await this.$store.dispatch('getPosts', {
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