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
                v-if="loading"
                prepend-avatar="./assets/EpicLogo.svg"
                title="---"
                subtitle="---"
              />
              <v-list-item
                v-else
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
                prepend-icon="./assets/EpicLogo.svg"
                color="red"
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
import { ref, onBeforeMount } from 'vue'
import { RouterView } from 'vue-router';
import { routes } from "./main"
import createHTTP from './axiosCalls'

const loading = ref(true)
const postData = ref({});
onBeforeMount(async () => {
  await createHTTP('authors/1/posts/1/').get().then((response: { data: object }) => {
    postData.value = response.data;
    loading.value = false;
  });
})
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