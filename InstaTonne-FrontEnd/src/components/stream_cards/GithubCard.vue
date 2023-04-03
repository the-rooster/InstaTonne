<template>
    <v-card
      class="mx-auto my-5 rounded-xl"
      color="#E3F2FD"
      theme="light"
      max-width="80%"
      style="margin: 5%"
    >
      <v-card-actions>
        <v-list-item class="w-100">
          <div class="main-container">
            {{ githubData }}
          </div>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup lang="ts">
  import { onBeforeMount } from "vue";
  import { createHTTP } from "../../axiosCalls";
  import { defineProps, ref, toRaw } from "vue";
  import PostPreviewCard from "./PostPreviewCard.vue";
  
  const postData = ref({});
  const postUrl = ref({});
  let author = ref({});
  
  const props = defineProps({
    githubData: {
      type: Object,
      required: true,
    },
  });
  
  
  
  // defineProps<{ msg: string }>();
  </script>
  
  <style scoped>
  .read-the-docs {
    color: #888;
  }
  
  .profile-picture {
    width: 10vw;
    height: 10vw;
    border-radius: 100%;
  }
  
  .avatar-liked-container {
    display: flex;
    align-items: center;
    justify-content: left;
  }
  
  .who-liked {
    margin-left: 1rem;
  }
  
  .post-preview-card {
    min-width: 100;
    border-width: 0.1em;
    border-color: #fefefe;
  }
  </style>
  