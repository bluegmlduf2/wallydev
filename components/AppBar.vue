<template>
  <div>
    <v-app-bar :clipped-left="true" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title class="d-none d-sm-block" v-text="title" />
      <v-spacer />
      <div max-width="100">
        <v-text-field
          prepend-icon="mdi-magnify"
          single-line
          hide-details
          outlined
          dense
          rounded
        ></v-text-field>
      </div>
      <v-btn icon href="https://github.com/bluegmlduf2">
        <v-icon>mdi-github</v-icon>
      </v-btn>
      <v-btn
        v-if="isLoggedIn && isAdminIn"
        icon
        @click="$router.push('/write')"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
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
            <div>
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
  </div>
</template>

<script>
export default {
  name: 'AppBarLeft',
  data() {
    return {
      title: 'WALLY DEV',
      drawer: false,
      tree: [],
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
  },
  methods: {
    async signInWithGoogle() {
      const provider = new this.$fireModule.default.auth.GoogleAuthProvider()
      await this.$fire.auth
        .signInWithPopup(provider)
        .then((res) => {
          res.user.getIdToken(true).then((idToken) => {
            localStorage.setItem('access_token', idToken.toString())
            localStorage.setItem(
              'refresh_token',
              res.user.refreshToken.toString()
            )
          })
        })
        .catch((e) => {})
    },
    async logout() {
      await this.$fire.auth.signOut()
    },
  },
}
</script>

<style scoped>
.hover-text:hover {
  color: #41b883 !important;
}
</style>