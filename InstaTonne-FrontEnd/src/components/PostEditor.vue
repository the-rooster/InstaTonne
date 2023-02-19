<template>
  <div
    class="viewBox"
  >
    <h3>
      This is the edit page! (WIP)
    </h3>
    {{ jsonData }}
  </div>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import postJson from '../examplePost.json'

  // eventually this will be replaced by some sort of backend call
  const jsonData = ref(postJson);
  </script>
  
  <style scoped>
  .read-the-docs {
    color: #888;
  }
  </style>
  