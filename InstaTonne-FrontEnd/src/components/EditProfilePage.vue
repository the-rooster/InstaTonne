<!-- InstaTonne-FrontEnd/src/components/EditProfilePage.vue -->
<!--
  Copyright (c) 2023 CMPUT 404 W2023 Group 6

  This file is part of InstaTonne.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  Description:
  This component is part of InstaTonne.
-->

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
