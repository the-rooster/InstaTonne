<template>
  <div class="viewBox">
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em"
      class="loadingIcon"
    />
    <div v-else-if="errorMessage.length > 0">
      <ErrorPage :error-message="errorMessage" />
    </div>
    <PostEditor
      v-else
      :post-data="postData"
      :save-function="savePost"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import PostEditor from "./PostEditor.vue";
import ErrorPage from "./ErrorPage.vue";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "../axiosCalls";
import Cookies from "js-cookie";

const loading = ref(true);
const errorMessage = ref("");
const postData = ref({});

let route = useRoute();
const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/posts/${route.params.postid}/`)
    .get()
    .then((response: { data: object }) => {
      postData.value = response.data;
      loading.value = false;
    })
    .catch(() => {
      errorMessage.value = "404 Post Not Found";
      loading.value = false;
    });
});

async function savePost(updatedPost) {
  loading.value = true;
  console.log("POST: ",updatedPost);
  await createHTTP(`authors/${authorId}/posts/${route.params.postid}/`)
    .post(JSON.stringify(updatedPost))
    .then((response: { data: object }) => {
      loading.value = false;
    });
}
</script>

<style scoped></style>
