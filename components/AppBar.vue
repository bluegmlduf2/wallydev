<template>
  <div>
    <v-app-bar :clipped-left="true" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
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
      <v-btn icon>
        <v-icon>mdi-github</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-login</v-icon>
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
            <v-icon>{{ props.item.icon }}</v-icon>
            {{ props.item.name }}
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
          name: 'Life',
          children: [
            {
              name: '일본생활',
              to: '/post/life',
            },
            {
              name: '요리',
              to: '/post/cooking',
            },
          ],
        },
        {
          icon: 'mdi-laptop',
          name: 'Development',
          children: [
            {
              name: 'Javascript',
              to: '/post/javascript',
            },
            {
              name: 'VueJs',
              to: '/post/vuejs',
            },
          ],
        },
      ],
    }
  },
}
</script>

<style scoped>
.hover-text:hover {
  color: #41b883 !important;
}
</style>