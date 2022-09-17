<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" clipped fixed app>
      <v-treeview
        v-model="tree"
        :items="items"
        activatable
        item-key="name"
        open-all
        @update:active="moveToPage"
        
      >
        <template #prepend="{ item }">
          <v-icon>{{ item.icon }}</v-icon>
        </template>
      </v-treeview>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="true" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn icon>
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
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
          name: 'Life',
          to: '/inspire',
          children: [
            {
              name: '일본생활',
              to: '/inspire',
            },
            {
              name: '요리',
              to: '/inspire',
            },
          ],
        },
        {
          icon: 'mdi-laptop',
          name: 'Development',
          children: [
            {
              name: 'Javascript',
              to: '/inspire',
            },
            {
              name: 'VueJs',
              to: '/inspire',
            },
          ],
        },
      ],
    }
  },
  methods: {
    moveToPage(item) {
      console.log(item)
    },
  },
}
</script>
