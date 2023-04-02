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
      <v-card
        height="6vh"
        width="12vw"
      >
        <h2>Your Stream</h2>
        <br>
      </v-card>
    </div>  
    <br>
    <div style="padding-bottom: 5em">
      <div
        v-for="item in posts"
        :key="item.id_url"
      >
        <PostFullCard
          v-if="item.type == 'post'"
          :post-data="item"
        />
        <InboxCommentCard
          v-if="item.type == 'comment'"
          :comment-data="item"
        />
        <LikeCommentCard
          v-if="item.type == 'like'"
          :like-data="item"
        />
      </div>
    </div>
    <ConfirmationModal
      ref="showConfirmation"
      message="Are you sure you want to clear your inbox?"
      @selected="(value) => clearInbox(value)"
    />
    <v-btn
      class="mx-auto clear-inbox"
      @click="
        () => {
          showConfirmation.show = true
        }
      "
    >
      clear your inbox
    </v-btn>
    <div id="app" />
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import PostFullCard from "./stream_cards/PostFullCard.vue";
import InboxCommentCard from "./stream_cards/InboxCommentCard.vue";
import LikeCommentCard from "./stream_cards/InboxLikeCard.vue";
import ConfirmationModal from "./ConfirmationModal.vue"
import Cookies from "js-cookie";
// defineProps<{ msg: string }>()

import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../axiosCalls";

let posts = ref({});

onBeforeMount(() => {
  getInbox();
});

const showConfirmation =  ref(false)

function clearInbox(value: boolean) {
  if (value) {
    createHTTP(`authors/${Cookies.get(USER_AUTHOR_ID_COOKIE)}/inbox/`)
    .delete()
    .then((msg) => {
      getInbox();
    });
  }
  showConfirmation.value.show = false;
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
