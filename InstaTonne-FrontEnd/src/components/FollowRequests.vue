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
      </div>
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

</script>

<style scoped>
</style>
  