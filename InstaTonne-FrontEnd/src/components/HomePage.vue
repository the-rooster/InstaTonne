<template>
  <div class="viewBox">
    <div
      style="
        justify-content: center;
        align-items: center;
        position: relative;
        top: 0%;
        left: 43%;
        z-index: 100;
      "
    >
      <v-card height="5vh" width="10vw">
        <h3>Your Stream</h3>
        <br />
      </v-card>
    </div>

    <br />
    <div style="padding-bottom: 5em">
      <div v-for="item in posts" v-bind:key="item.id_url">
        <PostFullCard
          v-bind:postData="item"
          v-if="item.type == 'post'"
        ></PostFullCard>
        <InboxCommentCard
          v-bind:commentData="item"
          v-if="item.type == 'comment'"
        ></InboxCommentCard>
        <LikeCommentCard
          v-bind:likeData="item"
          v-if="item.type == 'like'"
        ></LikeCommentCard>
      </div>
    </div>
    <v-btn
      class="mx-auto clear-inbox"
      @click="
        () => {
          clearInbox();
        }
      "
    >
      clear your inbox
    </v-btn>
    <div id="app"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import PostFullCard from "./stream_cards/PostFullCard.vue";
import InboxCommentCard from "./stream_cards/InboxCommentCard.vue";
import LikeCommentCard from "./stream_cards/InboxLikeCard.vue";
import Cookies from "js-cookie";
// defineProps<{ msg: string }>()

import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../axiosCalls";

let posts = ref({});

onBeforeMount(() => {
  getInbox();
});

function clearInbox() {
  createHTTP(`authors/${Cookies.get(USER_AUTHOR_ID_COOKIE)}/inbox/`)
    .delete()
    .then((msg) => {
      getInbox();
    });
}

function getInbox() {
  createHTTP(`authors/${Cookies.get(USER_AUTHOR_ID_COOKIE)}/inbox/`)
    .get()
    .then((response) => {
      console.log(response.data, 3454545);
      posts.value = response.data.items.reverse();
      console.log(response.data.items, 125125125);
    });
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}

.clear-inbox {
  color: black;
  background-color: red;
  position: fixed;
  bottom: 5%;
  right: 1%;
}
</style>
