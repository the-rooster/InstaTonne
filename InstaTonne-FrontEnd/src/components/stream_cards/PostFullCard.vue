<template>
  <v-card class="mx-auto" color="#fff" theme="light" max-width="400">
    <v-card-actions>
      <v-list-item class="w-100">
        <!-- <template v-slot:prepend>
          <v-avatar
            color="grey-darken-3"
            image="{{
            props.postData.author.profileImage
            }}"
          ></v-avatar>
        </template> -->

        <v-list-item-title>{{
          props.postData.author?.displayName
        }}</v-list-item-title>

        <v-list-item-subtitle>{{
          props.postData.author?.host
        }}</v-list-item-subtitle>

        <template v-slot:append>
          <div class="justify-self-end">
            <v-icon class="me-1" icon="mdi-heart"></v-icon>
            <span class="subheading me-2">256</span>
            <span class="me-1">·</span>
            <v-icon class="me-1" icon="mdi-share-variant"></v-icon>
            <span class="subheading">45</span>
          </div>
        </template>
      </v-list-item>
    </v-card-actions>

    <v-card>
      <v-img v-if="isImage" :src="require('${ props.postData.content }')" />
      <v-card-text v-else>
        <span>{{ props.postData.content }}</span>
        <span>{{ props.postData.comments }}</span>
      </v-card-text>
    </v-card>

    <v-card-actions>
      <v-btn variant="text"> Comments </v-btn>

      <v-spacer />

      <v-btn
        :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        @click="show = !show"
      />
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider />

        <v-card-text>
          <div v-for="item in comments" v-bind:key="item.id_url">
            <CommentCard
              v-if="(item.type = 'comment')"
              v-bind:commentData="item"
            />
          </div>
          <!-- I'm a thing. But, like most politicians, he promised more than he
          could deliver. You won't have time for sleeping, soldier, not with all
          the bed making you'll be doing. Then we'll go with that data file!
          Hey, you add a one and two zeros to that or we walk! You're going to
          do his laundry? I've got to find a way to escape. -->
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from "vue";
import CommentCard from "./CommentCard.vue";
import Cookies from "js-cookie";
// defineProps<{ msg: string }>()

import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../../axiosCalls";

const props = defineProps({
  postData: {
    type: Object,
    required: true,
  },
});

console.log(props.postData);

let comments = ref({});
createHTTP(`${props.postData.id_url}/comments/`)
  .get()
  .then((response) => {
    console.log(response.data, 1341234);
    comments.value = response.data.comments;
    console.log(response.data.comments, 567);
    console.log(comments.value, 987);
  });

// defineProps<{ msg: string }>()
const isImage = props.postData.author.contentType === "image/png;base64";
const show = ref(false);
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
