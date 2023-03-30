<template>
  <v-card
    class="mx-auto my-5 rounded-xl"
    color="#E3F2FD"
    theme="light"
    max-width="100%"
  >
    <v-card class="mx-4 my-4 rounded-xl" min-height="30vh">
      <v-list-item-title
        ><h2 class="my-4">{{ props.postData.title }}</h2></v-list-item-title
      >
      <v-img
        v-if="isImage"
        :src="require('${ props.postData.content }')"
        class="cropped-image"
      />
      <v-card-text v-else>
        <div
          v-html="content"
          v-if="props.postData.contentType == 'text/markdown'"
          class="content-container"
        ></div>
        <div
          v-if="
            props.postData.contentType == 'text/plain' ||
            props.postData.contentType == 'application/base64'
          "
          class="content-container"
        >
          {{ content }}
        </div>
        <img
          v-bind:src="content"
          v-if="
            props.postData.contentType == 'image/png;base64' ||
            props.postData.contentType == 'image/jpeg;base64'
          "
          class="cropped-image"
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
    props.postData.contentType === "image/png;base64" ||
    props.postData.contentType === "image/jpeg;base64";
});

// defineProps<{ msg: string }>()
</script>

<style scoped>
.read-the-docs {
  color: #888;
}

.content-container {
  max-height: 30vh;
  overflow: hidden;
  position: relative;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  font-size: large;
}

.cropped-image {
  max-height: 30vh;
  object-fit: cover;
}
</style>
