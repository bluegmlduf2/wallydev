<template>
  <v-container>
    <v-row class="mb-6" justify="start">
      <v-col v-for="e in post" :key="e.id">
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
  </v-container>
</template>

<script>
export default {
  name: 'IndexCategory',
  async asyncData({ params, store }) {
    const category = params.category
    await store.dispatch('getPosts', { category })

    return { category }
  },
  data() {
    return {
      category: '',
    }
  },
  computed: {
    post() {
      return this.$store.getters.post
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