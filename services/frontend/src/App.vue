<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h2 class="ma-4">Dominik Arnold 11-747-680</h2>
    </v-app-bar>
    <v-main>
      <ConfigurationPanel/>
    </v-main>
  </v-app>
</template>


<style>
/* disable scrolling */
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}
html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
</style>


<script>
import ConfigurationPanel from './components/ConfigurationPanel.vue'

export default {
  name: 'App',

  components: {
    ConfigurationPanel,
  },

  data: () => ({
    //
  }),
}
</script>
