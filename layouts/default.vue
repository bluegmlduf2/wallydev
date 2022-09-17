<template>
  <v-app>
    <AppBarTop/>
    <AppBarLeft/>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import AppBarLeft from '~/components/AppBarLeft.vue'
import AppBarTop from '~/components/AppBarTop.vue'
export default {
  name: 'DefaultLayout',
  components: { AppBarLeft, AppBarTop },
  data() {
    return {
      
    }
  },
}
</script>
