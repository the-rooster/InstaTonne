<template>
  <v-card
    class="mx-auto my-5 rounded-xl"
    color="#E3F2FD"
    theme="light"
    max-width="80%"
  >
    <v-card-actions>
      <v-list-item class="w-100">
        <template v-slot:prepend>
          <v-avatar
            size="70"
            color="grey-darken-3"
            image="{{
              props.postData.author.profileImage
              }}"
          ></v-avatar>
        </template>

        <v-list-item-title class="text-h6"
          ><a
            :href="`/app/ProfilePage/${encodeURIComponent(
              props.postData.author?.url
            )}/`"
            >{{ props.postData.author?.displayName }}</a
          ></v-list-item-title
        >

        <v-list-item-subtitle class="text-h7">{{
          props.postData.author?.host
        }}</v-list-item-subtitle>

        <template v-slot:append>
          <p>{{ numberOfLikes }} Likes</p>
          <div class="justify-self-end">
            <v-btn v-if="isLiked"
              ><v-icon class="me-1" icon="mdi-heart" color="blue"></v-icon
            ></v-btn>
            <v-btn v-else @click="likePost"
              ><v-icon class="me-1" icon="mdi-heart-outline"></v-icon
            ></v-btn>

            <v-btn v-if="isShared"
              ><v-icon
                class="me-1"
                icon="mdi-share-variant"
                color="blue"
              ></v-icon
            ></v-btn>
            <v-btn v-else @click="sharePost"
              ><v-icon class="me-1" icon="mdi-share-variant-outline"></v-icon
            ></v-btn>
          </div>
        </template>
      </v-list-item>
    </v-card-actions>

    <v-card class="mx-4 rounded-xl" min-height="30vh">
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
    <v-text-field
      class="mx-4 my-2 rounded-xl"
      v-model="newComment"
      label="Comment"
      placeholder="Comment"
      clearable
      @keyup.enter="saveComment"
    />
    <v-card-actions v-if="hasComments">
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
        <!-- <v-textarea v-model="commentData.content" clearable />
        <v-card-actions>
          <v-spacer />
          <v-btn @click="saveComment">Submit</v-btn>
        </v-card-actions> -->
        <v-card-text>
          <div v-for="item in comments" v-bind:key="item.id_url">
            <CommentCard
              v-if="item.type == 'comment'"
              v-bind:commentData="item"
              v-bind:postData="postData"
            />
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script setup lang="ts">
import { ref, toRaw, onBeforeMount, computed } from "vue";
import { router } from "../../main";
import CommentCard from "./CommentCard.vue";
import Cookies from "js-cookie";
import { marked } from "marked";
import DOMPurify from "dompurify";

// defineProps<{ msg: string }>()

import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../../axiosCalls";
import { vModelCheckbox } from "vue";
import { onMounted } from "vue";

let comments = ref({});
const isImage = ref(false);
const show = ref(false);

const props = defineProps({
  postData: {
    type: Object,
    required: true,
  },
  commentData: {
    type: Object,
    required: true,
  },
  newComment: {
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
    console.log("YAHOOO");
    console.log(DOMPurify.sanitize(marked.parse(props.postData.content)));
    return DOMPurify.sanitize(marked.parse(props.postData.content));
  }

  return props.postData.content;
});

// console.log(toRaw(props.postData).id, 1000);
// console.log(toRaw(props.postData));

async function likePost() {
  if (!props.postData.author) {
    return;
  }
  console.log(props.postData.origin, "originn");
  await createHTTP(`${encodeURI(props.postData.origin)}/likes/`)
    .post("")
    .then((response: { data: object }) => {
      console.log(response.data);
      router.go(0);
    });
}

const isLiked = ref(false);

// Check if I liked the post
async function checkIfLiked() {
  if (!props.postData.author) {
    return;
  }
  await createHTTP(`/authors/${encodeURI(props.postData.origin)}/likes/`)
    .get()
    .then((response: { data: object }) => {
      console.log(response.data, "check if liked");
      response.data.items.forEach((item: any) => {
        console.log("author id", authorId);
        const item_author_id = item.author.substring(
          item.author.lastIndexOf("/") + 1
        );
        console.log("item_author_id", item_author_id);
        if (item_author_id == authorId) {
          isLiked.value = true;
        }
      });
    });
}

const numberOfLikes = ref(0);

async function getPostLikeCount() {
  if (!props.postData.author) {
    return;
  }
  await createHTTP(`/authors/${encodeURI(props.postData.origin)}/likes/`)
    .get()
    .then((response: { data: object }) => {
      console.log(response.data, "get post like count");
      numberOfLikes.value = response.data.items.length;
      console.log(numberOfLikes.value, "number of likes");
    });
}

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);
const loading = ref(true);

async function sharePost() {
  if (!authorId) {
    return;
  }
  loading.value = true;
  var updatedPost = toRaw(props.postData);
  console.log(updatedPost, 1002);
  updatedPost.source = Cookies.get(USER_AUTHOR_ID_COOKIE);
  console.log(updatedPost, 1003);
  await createHTTP(`authors/${authorId}/posts/`)
    .post(JSON.stringify(updatedPost))
    .then((response: { data: object }) => {
      loading.value = false;
      router.go(0);
    });
}

const isShared = ref(false);

// Check if I have a post with the same ID
async function checkIfShared() {
  if (!authorId) {
    return;
  }
  await createHTTP(`authors/${authorId}/posts/`)
    .get()
    .then((response: { data: object }) => {
      console.log(response.data, "check if shared");
      for (let i = 0; i < response.data.items.length; i++) {
        if (response.data.items[i].id == props.postData.id) {
          console.log(
            "sharedd",
            response.data.items[i].id,
            props.postData.content
          );
          isShared.value = true;
          break;
        }
      }
    });
}

async function deletePost() {
  if (!props.postData.author) {
    return;
  }
  loading.value = true;
  let postId = props.postData.id;
  postId = postId.substring(postId.lastIndexOf("/") + 1);
  await createHTTP(`/authors/${authorId}/posts/${postId}`)
    .delete()
    .then((response: { data: object }) => {
      loading.value = false;
      router.go(0);
      router.back();
    });
}

const newComment = ref("");
async function saveComment() {
  if (!props.postData.author) {
    return;
  }
  console.log("newComment", newComment.value);
  await createHTTP(
    `/authors/${encodeURI(props.postData.author.id)}/posts/${encodeURI(
      props.postData.id
    )}/comments/`
  )
    .post(
      JSON.stringify({
        type: "comment",
        contentType: "text/plain",
        comment: newComment.value,
      })
    )
    .then((response: { data: object }) => {
      loading.value = false;
      getComments();
    });
}

onMounted(() => {
  console.log("POSTDATA", props.postData);
  getComments();
  getPostLikeCount();
  checkIfLiked();
  checkIfShared();

  console.log("isShared", isShared.value);

  isImage.value =
    props.postData.author.contentType === "image/png;base64" ||
    props.postData.author.contentType === "image/jpeg;base64";
});

const hasComments = ref(false);

function getComments() {
  createHTTP(
    `/authors/${encodeURI(props.postData.author.id)}/posts/${encodeURI(
      props.postData.id
    )}/comments/`
  )
    .get()
    .then((response) => {
      console.log(response.data, 4567);
      comments.value = response.data.comments;
      if (comments.value.length > 0) {
        hasComments.value = true;
      }
    });
}

// defineProps<{ msg: string }>()
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
