// import { cookieAuthKey, cookieRefreshAuthKey } from '~/store/auth'
import Vue from 'vue'

export default function ({ $axios, store }) {
  $axios.onRequest((config) => {
    // 파이어베이스 로그인 토큰정보를 서버에 전달
    const token = sessionStorage.getItem('access_token') || ''
    config.headers.common['Access-Control-Allow-Origin'] = '*'; // 클라이언트부터 cors요청 허용
    if (token) {
      config.headers.Authorization = token
    }
    return config
  })

  Vue.$http = $axios
}
