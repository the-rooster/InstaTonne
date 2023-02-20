<template>
  <v-app>
    <v-bottom-navigation
      grow
      elevation="10"
    >
      <v-btn
        v-for="route in routes"
        :key="route.path"
        :value="route.path"
      >
        <v-icon>mdi-history</v-icon>

        <router-link :to="route.path">
          {{ route.name }}
        </router-link>
      </v-btn>
    </v-bottom-navigation>
    <main>
      <router-view />
    </main>
  </v-app>
</template>

<script setup lang="ts">
import { routes } from "./main"
</script>

<style scoped>
v-app{
  height: 0;
}
</style>
