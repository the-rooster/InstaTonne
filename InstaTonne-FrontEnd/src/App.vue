<template>
  <div id="app">
    <v-app>
      <v-layout>
        <v-navigation-drawer
          expand-on-hover
          rail
          absolute
          width="500"
          v-if="loggedIn"
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
              :prepend-avatar="authorData.profileImage"
              :title="authorData.displayName"
              :subtitle="authorData.github"
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
              color="red"
              :title="route.name"
              :to="route.path"
            />
          </v-list>
        </v-navigation-drawer>        
        <v-main style="height: 100em;">
          <router-view v-if="loggedIn" />
          <login-page
            v-else
            @logged-in="(authorId) => activeUserId = authorId"
          />
        </v-main>
      </v-layout>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue'
import { RouterView } from 'vue-router';
import { nav_bar_routes as routes } from "./main"
import { createHTTP, USER_AUTHOR_ID_COOKIE } from './axiosCalls'
import LoginPage from './components/LoginPage.vue'
import Cookies from 'js-cookie';
import { reactive } from 'vue';

const loading = ref(true)
const authorData = ref({});
const activeUserId = ref("")

const loggedIn = computed(() => activeUserId.value != undefined);

onBeforeMount(async () => {
  activeUserId.value = Cookies.get(USER_AUTHOR_ID_COOKIE)

  if (!activeUserId.value){
    loading.value = false;
    return;
  }

  await createHTTP(`authors/${activeUserId.value}`).get().then((response: { data: object }) => {
    authorData.value = response.data;
    loading.value = false;
    console.log(response.data);
    console.log("GOT AUTHOR DATA!");
  });
})
</script>

<style scoped>

</style>
