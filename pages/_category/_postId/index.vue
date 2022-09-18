<template>
 <div>123</div>
</template>

<script>
export default {
  name: 'IndexPostDetail',
  async asyncData({ params, store }) {
    const postId = params.postId
    await store.dispatch('getPostDetail', { postId })
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
  },
}
</script>