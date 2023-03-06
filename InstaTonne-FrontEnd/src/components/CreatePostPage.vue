<template>
  <div
    class="viewBox"
  >
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em;"
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
      :require-extra="true"
    />
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import PostEditor from './PostEditor.vue'
import ErrorPage from './ErrorPage.vue'
import { createHTTP, USER_AUTHOR_ID_COOKIE } from '../axiosCalls'
import Cookies from "js-cookie";

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const loading = ref(false)
const errorMessage = ref("")
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
    author: authorId
});
  
async function savePost(updatedPost) {
    loading.value = true;
    
    await createHTTP(`authors/${authorId}/posts/`).post(JSON.stringify(updatedPost)).then((response: { data: object }) => {
        errorMessage.value = "Post created Successfully"
        loading.value = false;
    });
}

</script>

<style scoped>
</style>
      
  