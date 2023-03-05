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
      <ErrorPage :error-message="errorMessage" />
    </div>
    <div v-else>
      <div style="display: flex;">
        <AuthorCard :author-info="postData.author" />
        <v-card>
          <template #title>
            Published On:
          </template>
          <v-card-item>
            {{ postData.published }}
          </v-card-item>
        </v-card>
        <v-card>
          <template #title>
            Visibility:
          </template>
          <v-card-item>
            <v-radio-group v-model="postData.visibility">
              <v-radio
                label="public"
                value="PUBLIC"
              />
              <v-radio
                label="friends only"
                value="FRIENDS"
              />
            </v-radio-group>
          </v-card-item>
        </v-card>
      </div>
      <v-textarea
        v-model="postData.title"
        clearable
      />
      <v-textarea
        v-model="postData.description"
        clearable
      />
      <v-textarea
        v-model="postData.content"
        clearable
      />
      <v-combobox
        v-model="postData.categories"
        chips
        clearable
        label="Categories"
        multiple
      >
        <template #selection="{ attrs, item, select, selected }">
          <v-chip
            v-bind="attrs"
            :model-value="selected"
            closable
            @click="select"
            @click:close="remove(item)"
          >
            {{ item }}
          </v-chip>
        </template>
      </v-combobox>
      <v-btn
        @click="savePost"
      >
        SAVE
      </v-btn>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { useRoute } from "vue-router";
import AuthorCard from './AuthorCard.vue'
import ErrorPage from './ErrorPage.vue'
import { createHTTP, USER_AUTHOR_ID_COOKIE } from '../axiosCalls'
import Cookies from "js-cookie";

const loading = ref(true)
const errorMessage = ref("")
const postData = ref({});

let route = useRoute();

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/posts/${route.params.postid}/`).get().then((response: { data: object }) => {
    postData.value = response.data;
    loading.value = false;
  }).catch(() => {
    errorMessage.value = "404 Post Not Found"
    loading.value = false;
  });
})

async function savePost() {
  // eventually this should do a backend call to push postData
  // Note: since everything is binded, all the changes should be stored in postData already!
  loading.value = true;
  await createHTTP(`authors/${authorId}/posts/${route.params.postid}/`).post(JSON.stringify(postData.value)).then((response: { data: object }) => {
    loading.value = false;
  });
}

</script>

<style scoped>
</style>
  