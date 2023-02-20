<template>
  <div
    class="viewBox"
  >
    <div style="display: flex;">
      <AuthorCard :author-info="postData.author" />
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import postJson from '../examplePost.json'
import AuthorCard from './AuthorCard.vue'

const postData = ref(postJson);

</script>

<style scoped>
</style>
  