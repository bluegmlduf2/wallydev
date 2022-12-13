import colors from 'vuetify/es5/util/colors'

export default {
  // Target: https://go.nuxtjs.dev/config-target
  // server : npm run build 시 dist에 nodejs배포용 파일생성
  // static : npm run generate 시 dist에 웹서버 배포용 파일생성
  target: 'server',
  router: {
    // base: '/wallydev/', // github repository 이름 넣기
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'WALLY DEV',
    htmlAttrs: {
      lang: 'ko',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      // 메타태그
      {
        hid: 'description',
        name: 'description',
        content: 'Wally의 후쿠오카 생활과 개발이야기를 담고 있습니다',
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content:
          '후쿠오카 맛집,일본생활,일본,개발,코딩,일본취업,자바스크립트,PHP,VUE,JS',
      },
      {
        hid: 'author',
        name: 'author',
        content: 'Wally',
      },
      // OG태그
      {
        hid: 'og:title',
        name: 'og:title',
        content: 'WALLY DEV',
      },
      {
        hid: 'og:description',
        name: 'og:description',
        content: 'Wally의 후쿠오카 생활과 개발이야기를 담고 있습니다',
      },
      {
        hid: 'og:site_name',
        name: 'og:site_name',
        content: 'WALLY DEV - 코딩과 일본생활',
      },
      {
        hid: 'og:url',
        name: 'og:url',
        content: 'https://wallydev.com',
      },
      {
        hid: 'og:locale',
        name: 'og:locale',
        content: 'ko_KR',
      },
      {
        hid: 'og:image',
        name: 'og:image',
        content: 'https://wallydev.com/android-chrome-512x512.png',
      },
      {
        hid: 'og:image:width',
        name: 'og:image:width',
        content: '512',
      },
      {
        hid: 'og:image:height',
        name: 'og:image:height',
        content: '512',
      },
      // 검색 크롤링 범위 설정
      { hid: 'robots', name: 'robots', content: 'ALL' },
      // 구글 서치 콘솔
      {
        name: 'google-site-verification',
        content: 'omPgIWqnBfqP7j0mgp3cWOcvTQodgpxCdUM8QvR87Wg',
      },
      // 네이버 서치 콘솔
      {
        name: 'naver-site-verification',
        content: '0aedc057c577ca3d446182dda3f909b581ea718d',
      },
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico',
      },
    ],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['@/assets/css/common.css'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/axios',
    { src: '~/plugins/infinite-loading', ssr: false },
    { src: '~/plugins/global-component', ssr: false },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/dotenv',
    [
      '@nuxtjs/firebase',
      {
        config: {
          apiKey: process.env.VUE_APP_APIKEY,
          authDomain: process.env.VUE_APP_AUTHDOMAIN,
          projectId: process.env.VUE_APP_PROJECTID,
          storageBucket: process.env.VUE_APP_STORAGEBUCKET,
          messagingSenderId: process.env.VUE_APP_MESSAGINGSENDERID,
          appId: process.env.VUE_APP_APPID,
          measurementId: process.env.VUE_APP_MEASUREMENTID,
        },
        services: {
          auth: {
            persistence: 'session',
            initialize: {
              onAuthStateChangedAction: 'onAuthStateChanged',
            },
            ssr: true,
          },
        },
      },
    ],
  ],

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en',
    },
    meta: true,
    icon: true,

    workbox: {
      importScripts: ['/firebase-auth-sw.js'],
      dev: process.env.NODE_ENV === 'development',
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    theme: {
      themes: {
        light: {
          maincolor: '#41b883',
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  axios: {
    // proxy사용시 baseURL사용불가
    baseURL: process.env.VUE_APP_API_URL,
    // proxy: true,
  },
  proxy: {
    // CORS 방지용 프론트(localhost:3000)->서버(localhost:5001)
    // http://localhost:3000/api_wallydev -> http://localhost:5001/api_wallydev
    // '/api_wallydev': process.env.VUE_APP_API_URL,
  },
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
  server: {
    // 모바일기기(로컬) 테스트를 위하여 추가하여 사용하기도 하지만 배포환경에서 문제가 될 가능성이 있어 npm명령어에 입력하여사용
    // host: '192.168.0.101', // default: localhost
    // port: '3000', // default: 3000
  },
}
