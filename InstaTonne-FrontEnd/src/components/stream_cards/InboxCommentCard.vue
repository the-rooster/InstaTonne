<!-- InstaTonne-FrontEnd/src/components/stream_cards/PostFullCard.vue -->
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
  This component is part of InstaTonne and provides authentication functionality.
-->

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
        <v-list-item-title
          ><a :href="`/app/ProfilePage/${encodeURIComponent(author.url)}/`">{{
            author.displayName
          }}</a>
          commented on your post</v-list-item-title
        >
        <template v-slot:append>
          <div class="justify-self-end"></div>
        </template>
        <div
          style="
            display: flex;
            flex-direction: row;
            justify-content: space-between;
          "
        >
          <img :src="author.profileImage" class="profile-picture" />
          <v-list-item>{{ props.commentData.comment }}</v-list-item>
          <a v-bind:href="postUrl">
            <div class="post-tiny">
              <h1
                style="
                  text-overflow: ellipsis;
                  white-space: nowrap;
                  max-width: 100%;
                  overflow: hidden;
                "
              >
                {{ postData.title }}
              </h1>
              <span
                style="
                  text-overflow: ellipsis;
                  white-space: nowrap;
                  max-width: 100%;
                  overflow: hidden;
                "
                >{{ postData.description }}</span
              >
            </div>
          </a>
        </div>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { onBeforeMount } from "vue";
import { createHTTP } from "../../axiosCalls";
import { defineProps, ref, toRaw } from "vue";

const postData = ref({});
const postUrl = ref({});
let author = ref({});

const props = defineProps({
  commentData: {
    type: Object,
    required: true,
  },
});

onBeforeMount(() => {
  let commentId: string = props.commentData.id;

  let groups = commentId.match(
    /(.*)\/authors\/(?<authorId>.*)\/posts\/(?<postId>.*)\/comments\//
  )?.groups;

  let authorId = "";
  let postId = "";
  if (groups) {
    authorId = groups.authorId;
    postId = groups.postId;
  }

  postUrl.value = `authors/${encodeURIComponent(
    authorId
  )}/posts/${encodeURIComponent(postId)}`;

  console.log("POSTID", postId);
  console.log("AUTHORID", authorId);
  createHTTP(
    `authors/${encodeURIComponent(authorId)}/posts/${encodeURIComponent(
      postId
    )}`
  )
    .get()
    .then((result) => {
      console.log("POST", result.data);
      postData.value = result.data;
    });

  createHTTP(`authors/${encodeURIComponent(props.commentData.author)}`)
    .get()
    .then((result) => {
      console.log("POST", result.data);
      postData.value = result.data;
    });
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

.post-tiny {
  border: 0.2em solid black;
  padding: 1em;
  margin: 1em;
  width: 10vw;
  height: 10vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 60%;
}
</style>
