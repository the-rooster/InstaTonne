<template>
  <v-card
    class="mx-auto my-5 rounded-xl"
    color="#E3F2FD"
    theme="light"
    max-width="80%"
  >
    <v-card class="mx-4 my-4 rounded-xl" min-height="30vh">
      <v-list-item-title
        ><h3>{{ props.postData.title }}</h3></v-list-item-title
      >
      <v-img v-if="isImage" :src="require('${ props.postData.content }')" />
      <v-card-text class="my-10" v-else>
        <div
          v-html="content"
          v-if="props.postData.contentType == 'text/markdown'"
        ></div>
        <span
          v-if="
            props.postData.contentType == 'text/plain' ||
            props.postData.contentType == 'application/base64'
          "
          >{{ content }}</span
        >
        <img
          v-bind:src="content"
          v-if="
            props.postData.contentType == 'image/png;base64' ||
            props.postData.contentType == 'image/jpeg;base64'
          "
        />
      </v-card-text>
    </v-card>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

// defineProps<{ msg: string }>()

import { onMounted } from "vue";

const isImage = ref(false);

const props = defineProps({
  postData: {
    type: Object,
    required: true,
  },
});

let content = computed(() => {
  console.log("PROP", props.postData);

  if (!props.postData) {
    return "";
  }

  if (props.postData.contentType == "text/markdown") {
    console.log("Yippy ka ye");
    console.log(DOMPurify.sanitize(marked.parse(props.postData.content)));
    return DOMPurify.sanitize(marked.parse(props.postData.content));
  }

  return props.postData.content;
});

onMounted(() => {
  console.log("POSTDATA for PostPreview", props.postData);

  isImage.value =
    props.postData.author.contentType === "image/png;base64" ||
    props.postData.author.contentType === "image/jpeg;base64";
});

// defineProps<{ msg: string }>()
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
