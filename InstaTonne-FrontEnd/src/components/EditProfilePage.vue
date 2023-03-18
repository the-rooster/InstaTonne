<template>
  <div class="viewBox">
    <h1>Just some text</h1>
    <v-text-field
      v-model="authorData.displayName"
      label="Display Name"
      placeholder="authorData.displayName"
      class="my-10"
      clearable
    />
    <v-text-field
      v-model="authorData.github"
      label="Github"
      placeholder="authorData.github"
      class="my-10"
      clearable
    />
    <v-text-field
      v-model="authorData.profileImage"
      label="Upload image"
      variant="filled"
      prepend-icon="mdi-camera"
      class="my-10"
    />
    <v-btn :disabled="disableSaving" @click="savePost"> SAVE </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeMount } from "vue";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "../axiosCalls";
import { useRoute } from "vue-router";
import Cookies from "js-cookie";

console.log("showing something");

const route = useRoute();
const loading = ref(true);

const authorData = ref({});

const disableSaving = computed(() => authorData.value.displayName === "");

let profileId = route.params.id;

if (!profileId) {
  profileId = Cookies.get(USER_AUTHOR_ID_COOKIE);
}

createHTTP("authors/" + profileId + "/")
  .get()
  .then((response) => {
    console.log(response.data, 51515);
    authorData.value = response.data;
    console.log(response.data, 567);
  });

async function savePost() {
  loading.value = true;
  await createHTTP(`authors/${profileId}`)
    .post(JSON.stringify(authorData.value))
    .then((response: { data: object }) => {
      loading.value = false;
    });
}
</script>

<style scoped></style>
