<template>
  <div id="app">
    <v-app>
      <v-card>
        <v-layout>
          <v-navigation-drawer
            expand-on-hover
            rail
          >
            <v-list>
              <v-list-item
                :prepend-avatar="postData.author.profileImage"
                :title="postData.author.displayName"
                :subtitle="postData.author.github"
              />
            </v-list>

            <v-divider />

            <v-list
              density="compact"
              nav
            >
              <v-list-item
                v-for="route in routes"
                :key="route.path"
                prepend-icon="mdi-folder"
                :title="route.name"
                :to="route.path"
              />
            </v-list>
          </v-navigation-drawer>

          <v-main style="height: 100em;">
            <router-view />
          </v-main>
        </v-layout>
      </v-card>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router';
import { routes } from "./main"
import postJson from './examplePost.json'

const postData = ref(postJson);
</script>

<style scoped>
v-app{
  height: 0;
}
</style>

<!-- <v-bottom-navigation
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
    </v-bottom-navigation> -->