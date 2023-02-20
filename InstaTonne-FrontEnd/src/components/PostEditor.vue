<template>
  <div
    class="viewBox"
  >
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
      @onclick="savePost"
    >
      SAVE
    </v-btn>
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import postJson from '../examplePost.json'
import AuthorCard from './AuthorCard.vue'

//TODO: replace the logo above with a placeholder pfp

// eventually this will be replaced by some sort of backend call
const postData = ref(postJson);

// const visibility = ref(postData.value.visibility);


function savePost() {
  // eventually this should do a backend call to push postData
  // Note: since everything is binded, all the changes should be stored in postData already!
  return
}

</script>

<style scoped>
</style>
  