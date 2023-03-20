<!-- InstaTonne-FrontEnd/src/components/UserPost.vue -->
<!--
  Copyright (c) 2023 CMPUT 404 W2023 Group 6

  This file is part of InstaTonne.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  Description:
  This component is part of InstaTonne.
-->

<template>
  <div class="viewBox">
    <br />
    <div>
      <PostFullCard v-if="post.type == 'post'" :post-data="post" />
    </div>
    <div id="app" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
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
