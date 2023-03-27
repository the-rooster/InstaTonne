<template>
  <div id="app">
    <v-app>
      <v-layout>
        <v-navigation-drawer
          v-if="loggedIn"
          expand-on-hover
          rail
          fixed
          permanent
          rail-width="60"
          width="500"
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

          <v-list density="compact" nav>
            <v-list-item
              v-for="route in routes"
              :key="route.path"
              color="blue"
              :title="route.name"
              :to="route.path"
              :prepend-icon="route.icon"
            />
          </v-list>
          <v-list>
            <v-list-item
              v-if="loggedIn"
              title="Logout"
              @click="logout"
              prepend-icon="mdi-logout"
            />
          </v-list>
        </v-navigation-drawer>
        <v-main>
          <router-view v-if="loggedIn" />
          <login-page
            v-else
            @logged-in="(authorId) => (activeUserId = authorId)"
          />
        </v-main>
      </v-layout>
    </v-app>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed, watch } from "vue";
import { RouterView, useRoute } from "vue-router";
import { nav_bar_routes as routes, router } from "./main";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "./axiosCalls";
import LoginPage from "./components/LoginPage.vue";
import Cookies from "js-cookie";

const loading = ref(true);
const authorData = ref({});
const activeUserId = ref("");

const loggedIn = computed(() => activeUserId.value != undefined);

const logout = () => {
  Cookies.remove(USER_AUTHOR_ID_COOKIE);
  router.push({ path: "/" });
  window.location.reload();
};

const route = useRoute();
watch(route, () => {
  activeUserId.value = Cookies.get(USER_AUTHOR_ID_COOKIE);
});

onBeforeMount(async () => {
  activeUserId.value = Cookies.get(USER_AUTHOR_ID_COOKIE);

  if (!activeUserId.value) {
    loading.value = false;
    return;
  }

  await createHTTP(`authors/${activeUserId.value}`)
    .get()
    .then((response: { data: object }) => {
      authorData.value = response.data;
      loading.value = false;
      console.log(response.data);
      console.log("GOT AUTHOR DATA!");
    });
});
</script>

<style scoped></style>
