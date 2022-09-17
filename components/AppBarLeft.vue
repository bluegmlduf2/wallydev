<template>
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
          class="text-decoration-none black--text"
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
</template>

<script>
export default {
  name: 'AppBarLeft',
  data() {
    return {
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
}
</script>

<style>
</style>