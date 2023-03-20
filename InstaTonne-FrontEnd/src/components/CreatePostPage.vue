<!-- InstaTonne-FrontEnd/src/components/CreatePostPage.vue -->
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
  This component is part of InstaTonne and provides authentication functionality.
-->

<template>
  <div>
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em"
    />
    <div v-else-if="errorMessage.length > 0">
      <div>
        <v-icon
          class="me-1"
          size="500"
          color="green"
          icon="mdi-check-circle-outline"
        />
      </div>
      <ErrorPage :error-message="errorMessage" />
    </div>
    <PostEditor
      v-else
      :post-data="postData"
      :save-function="savePost"
      :require-extra="false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import PostEditor from "./PostEditor.vue";
import ErrorPage from "./ErrorPage.vue";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "../axiosCalls";
import Cookies from "js-cookie";

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const loading = ref(false);
const errorMessage = ref("");
const postData = ref({
  title: "",
  source: "",
  origin: "",
  description: "",
  contentType: "text/plain", //TODO: support markdown
  content: "",
  visibility: "",
  categories: [],
  unlisted: false,
  author: authorId,
});

async function savePost(updatedPost) {
  loading.value = true;
  console.log("SENDING POST: ", updatedPost);

  // case for posting image data as b64
  if (updatedPost.contentType.includes("image/")) {
    let reader = new FileReader();
    reader.readAsDataURL(updatedPost.content[0]);
    reader.onload = function () {
      updatedPost.content = reader.result;

      createHTTP(`authors/${authorId}/posts/`)
        .post(JSON.stringify(updatedPost))
        .then((response: { data: object }) => {
          errorMessage.value = "Post created Successfully";
          loading.value = false;
        });
    };
  } else {
    // posting standard plain text
    await createHTTP(`authors/${authorId}/posts/`)
      .post(JSON.stringify(updatedPost))
      .then((response: { data: object }) => {
        errorMessage.value = "Post created Successfully";
        loading.value = false;
      });
  }
}
</script>

<style scoped></style>
