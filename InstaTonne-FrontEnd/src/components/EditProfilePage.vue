<template>
  <div class="viewBox">
    <h1>Profile Editor</h1>
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
import { createHTTP } from "../axiosCalls";
import { USER_AUTHOR_ID_COOKIE } from "../constants";
import { useRoute } from "vue-router";
import { router } from "../main";
import Cookies from "js-cookie";
console.log("showing something");
const route = useRoute();
const loading = ref(true);
const authorData = ref({});
const disableSaving = computed(() => authorData.value.displayName === "");
const profileId = ref("");
onBeforeMount(() => {
  if (route.params.id) {
    profileId.value = route.params.id;
  }
  if (!profileId.value) {
    profileId.value = Cookies.get(USER_AUTHOR_ID_COOKIE);
  }
  createHTTP("authors/" + profileId.value + "/")
    .get()
    .then((response) => {
      console.log(response.data, 51515);
      authorData.value = response.data;
      console.log(response.data, 567);
    });
});
async function savePost() {
  loading.value = true;
  await createHTTP(`authors/${profileId.value}`)
    .post(JSON.stringify(authorData.value))
    .then((response: { data: object }) => {
      loading.value = false;
      router.push(`/ProfilePage/${encodeURIComponent(authorData.value.id)}/`);
    });
}
</script>

<style scoped></style>
