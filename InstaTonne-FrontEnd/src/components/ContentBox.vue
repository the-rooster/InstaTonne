<template>
  <div
    class="viewBox"
  >
    <v-select
      v-if="props.editable"
      v-model="contentType"
      label="Select"
      :items="['text/plain', 'text/markdown', 'text/markdown', 'application/base64', 'image/png;base64', 'image/jpeg;base64']"
    />
    <v-textarea
      v-if="contentType == 'text/plain' || contentType == 'text/markdown'"
      v-model="content"
      clearable
    />
    <div v-if="contentType == 'text/markdown'">
      Markdown Preview:
      <div 
        v-html="markdownPreview"
      />
    </div>
    <v-file-input 
      v-if="contentType == 'application/base64' || contentType == 'image/png;base64' || contentType == 'image/jpeg;base64'"
      v-model="content"
      label="Upload Image"
      variant="solo"
      prepend-icon="mdi-camera"
    />
  </div>
</template>
      
<script setup lang="ts">
import { ref, computed } from 'vue'
//   import AuthorCard from './AuthorCard.vue'
import { marked } from "marked";

const props = defineProps({
    content: {
        type: String,
        required: true,
    },
    contentType: {
        type: String,
        required: true
    },
    editable: {
        type: Boolean,
        required: true
    }
});

const content = ref(props.content)
const contentType = ref(props.contentType)
  
//   const postData = ref(props.postData) 
  
//   const disableSaving = computed(() => postData.value.source.length == 0 ||
//   postData.value.origin.length == 0 ||
//   postData.value.title.length == 0 ||
//   postData.value.content.length == 0 ||
//   postData.value.description.length == 0 ||
//   (postData.value.visibility != "PUBLIC" && postData.value.visibility != "FRIENDS"))
  
//   async function savePost() {
//     props.saveFunction(postData.value)
//   }
  
const markdownPreview = computed(() => {
    return marked(content.value, { sanitize: true })
})
  
</script>

<style scoped>
</style>