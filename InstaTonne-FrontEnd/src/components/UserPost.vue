<template>
    <div class="viewBox">

      <br />
      <div>

          <PostFullCard
            v-bind:postData="post"
            v-if="(post.type = 'post')"
          ></PostFullCard>

      </div>
      <div id="app"></div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  import {useRoute} from "vue-router";
  import PostFullCard from "./stream_cards/PostFullCard.vue";
  import Cookies from "js-cookie";
  // defineProps<{ msg: string }>()
  
  import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../axiosCalls";
  
  let post = ref({});

  let route = useRoute();
  
  createHTTP(`authors/${route.params.id}/posts/${route.params.postid}/`)
    .get()
    .then((response) => {
      console.log(response.data, 3454545);
      post.value = response.data;
      console.log(response.data);
      console.log("YAHOO");
    });
  </script>
  
  <style scoped>
  .read-the-docs {
    color: #888;
  }
  </style>
  