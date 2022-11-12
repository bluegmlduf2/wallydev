<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '~/components/AppBar.vue'
export default {
  name: 'DefaultLayout',
  components: { AppBar },
}
</script>
