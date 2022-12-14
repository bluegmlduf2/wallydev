import Vue from 'vue'
import InfiniteLoading from 'vue-infinite-loading'

Vue.component('InfiniteLoading', InfiniteLoading)

// vue-infinite-loading custom
Vue.use(InfiniteLoading, {
  slots: {
    noMore: '더이상 데이터가 없습니다',
    noResults: '데이터가 없습니다',
  },
  props: { spinner: 'waveDots' },
})
