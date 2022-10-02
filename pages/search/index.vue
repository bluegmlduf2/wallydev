<template>
  <v-container>
    <v-row class="mb-6" justify="start">
      <v-col v-for="e in post" :key="e.id" cols="12" sm="6" md="4" lg="3">
        <v-card max-width="344" class="hover-up">
          <v-img :src="e.imageUrl" height="200px"></v-img>
          <v-card-title> {{ e.title }} </v-card-title>
          <v-card-subtitle class="subtitle-body text-overflow">
            {{ e.postContent }}
          </v-card-subtitle>
          <v-card-actions class="d-flex justify-end">
            <v-btn color="maincolor" text nuxt :to="`${e.category}/${e.id}`">
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
  name: 'IndexSeach',
  data() {
    return {
      searchText: '',
      page: 1,
    }
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
  },
  watch: {
    // 같은 경로의 route의 리로딩시 대응
    // 같은 경로의 router로 push하는 경우 화면이 동작하지않는다.
    // 그래서 router로 push될시 query 값인 searchText를 감시하여 동작이 있으면 getPostsBySearchText를 호출
    '$route.query.searchText': 'getPostsBySearchText',
  },
  // 새로고침시 fetch가 동작하지 않아서 mounted로 변경
  mounted() {
    // watch에서 getPostsBySearchText메소드를 같이 사용하므로 분리함
    this.getPostsBySearchText()
  },
  methods: {
    async getPostsBySearchText() {
      this.searchText = this.$route.query?.searchText || ''
      await this.$store.dispatch('getPosts', {
        searchText: this.searchText,
        page: 1,
      })
    },
    scrolling($state) {
      // 스크롤이 페이지 하단에 위치해도 약간의 딜레이를 주고 데이터를 가져옴
      setTimeout(async () => {
        this.page++
        // 게시글 더 가져오기
        const isMoreData = await this.$store.dispatch('getPosts', {
          searchText: this.searchText,
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