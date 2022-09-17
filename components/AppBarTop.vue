<template>
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
</template>

<script>
export default {
  name: 'AppBarTop',
  data() {
    return {
      title: 'WALLY DEV',
      drawer: false,
    }
  },
}
</script>

<style>
</style>