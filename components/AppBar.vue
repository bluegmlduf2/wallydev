<template>
  <div>
    <v-app-bar :clipped-left="true" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title class="d-none d-sm-block" v-text="title" />
      <v-spacer />
      <div max-width="100">
        <v-text-field
          v-model="searchText"
          prepend-icon="mdi-magnify"
          single-line
          hide-details
          outlined
          dense
          rounded
          @click:prepend="searchPost"
          @keyup.enter="searchPost"
        ></v-text-field>
      </div>
      <v-btn icon href="https://github.com/bluegmlduf2" target="_blank">
        <v-icon>mdi-github</v-icon>
      </v-btn>
      <client-only>
        <v-btn v-if="isLoggedIn && isAdminIn" icon nuxt to="/write">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </client-only>
      <v-btn v-if="!isLoggedIn" icon @click="signInWithGoogle">
        <v-icon>mdi-login</v-icon>
      </v-btn>
      <v-btn v-else icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" clipped fixed app>
      <v-treeview
        v-model="tree"
        :items="items"
        activatable
        item-key="name"
        open-all
        hoverable
      >
        <template slot="label" slot-scope="props">
          <nuxt-link
            v-if="props.item.to"
            class="text-decoration-none black--text hover-text"
            :to="props.item.to"
          >
            <div @click="searchText = ''">
              <v-icon>{{ props.item.icon }}</v-icon>
              {{ props.item.name }}
            </div>
          </nuxt-link>
          <span v-else class="black--text"
            ><v-icon>{{ props.item.icon }}</v-icon
            >{{ props.item.name }}</span
          >
        </template>
      </v-treeview>
    </v-navigation-drawer>
    <div class="progress-wrapper">
      <v-progress-circular
        v-if="isLoading"
        :size="70"
        :width="7"
        color="maincolor"
        indeterminate
      ></v-progress-circular>
    </div>
    <Alert
      :is-open="isOpen"
      :dialog-message="dialogMessage"
      @closeDialog="isOpen = false"
    />
  </div>
</template>

<script>
import message from '~/assets/js/message'

export default {
  name: 'AppBarLeft',
  data() {
    return {
      title: 'WALLY DEV',
      drawer: false,
      tree: [],
      searchText: '',
      isOpen: false,
      dialogMessage: '',
      items: [
        {
          icon: 'mdi-home',
          name: 'Home',
          to: '/',
        },
        {
          icon: 'mdi-human-greeting-variant',
          name: 'LifeStyle',
          children: [
            {
              name: 'Today',
              to: '/today',
            },
            {
              name: 'Food',
              to: '/food',
            },
          ],
        },
        {
          icon: 'mdi-laptop',
          name: 'Development',
          children: [
            {
              name: 'Javascript',
              to: '/javascript',
            },
            {
              name: 'VueJs',
              to: '/vuejs',
            },
            {
              name: 'PHP',
              to: '/php',
            },
          ],
        },
      ],
    }
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters?.isLoggedIn
    },
    isAdminIn() {
      return this.$store.getters?.isAdminIn
    },
    isLoading() {
      return this.$store.getters.isLoading
    },
  },
  methods: {
    async signInWithGoogle() {
      const provider = new this.$fireModule.default.auth.GoogleAuthProvider()
      await this.$fire.auth
        .signInWithPopup(provider)
        .then((res) => {
          res.user.getIdToken(true).then((idToken) => {
            sessionStorage.setItem('access_token', idToken.toString())
            sessionStorage.setItem(
              'refresh_token',
              res.user.refreshToken.toString()
            )
            // 현재페이지 새로고침(해당 페이지 데이터 초기화용)
            location.reload()
          })
          this.isOpen = true
          this.dialogMessage = message.welcome
        })
        .catch((e) => {})
    },
    async logout() {
      await this.$fire.auth.signOut()
      sessionStorage.removeItem('access_token')
      sessionStorage.removeItem('refresh_token')
      this.isOpen = true
      this.dialogMessage = message.bye
    },
    searchPost() {
      // 검색어 입력확인
      if (this.searchText) {
        this.$router.push({
          name: 'search',
          query: { searchText: this.searchText },
        })
      } else {
        this.isOpen = true
        this.dialogMessage = message.inputText('검색어')
      }
    },
  },
}
</script>

<style scoped>
.hover-text:hover {
  color: #41b883 !important;
}
/* 프로그레스바 중앙정렬 */
.progress-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateY(-50%) translateX(-50%);
  margin: auto;
  z-index: 1;
}
</style>