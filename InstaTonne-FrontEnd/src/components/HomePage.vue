<template>
  <div class="viewBox">
    <h1>Your Stream</h1>
    <br />
    <div style="overflow-y: scroll; max-height: 90em">
      <div v-for="item in posts" v-bind:key="item.id_url">
        <PostFullCard
          v-bind:postData="item"
          v-if="(item.type == 'post')"
        ></PostFullCard>
        <InboxCommentCard
          v-bind:commentData="item"
          v-if="(item.type == 'comment')"
        ></InboxCommentCard>
        <LikeCommentCard
          v-bind:likeData="item"
          v-if="(item.type == 'like')"
        ></LikeCommentCard>
      </div>
    </div>
    <div id="app"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import PostFullCard from "./stream_cards/PostFullCard.vue";
import InboxCommentCard from "./stream_cards/InboxCommentCard.vue";
import LikeCommentCard from "./stream_cards/InboxLikeCard.vue";
import Cookies from "js-cookie";
// defineProps<{ msg: string }>()

import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../axiosCalls";

let posts = ref({});

createHTTP(`authors/${Cookies.get(USER_AUTHOR_ID_COOKIE)}/inbox/`)
  .get()
  .then((response) => {
    console.log(response.data, 3454545);
    posts.value = response.data.items;
    console.log(response.data.items,125125125);
  });
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
