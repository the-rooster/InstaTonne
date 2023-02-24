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
import AuthorCard from './AuthorCard.vue'
import createHTTP from '../axiosCalls'

const loading = ref(true)
const postData = ref({});
onBeforeMount(async () => {
  await createHTTP('authors/1/posts/1/').get().then((response: { data: object }) => {
    postData.value = response.data;
    loading.value = false;
  });
})

async function savePost() {
  // eventually this should do a backend call to push postData
  // Note: since everything is binded, all the changes should be stored in postData already!
  loading.value = true;
  console.log("posting....")
  await createHTTP('authors/1/posts/1/').post(JSON.stringify(postData.value)).then((response: { data: object }) => {
    loading.value = false;
  });
}

</script>

<style scoped>
</style>
  