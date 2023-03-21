<template>
  <v-card class="mx-auto" color="#eee" theme="light" max-width="80%">
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

        <v-list-item-title><a :href="`/app/ProfilePage/${encodeURIComponent(props.postData.author?.url)}/`">{{
          props.postData.author?.displayName
        }}</a></v-list-item-title>

        <v-list-item-subtitle>{{
          props.postData.author?.host
        }}</v-list-item-subtitle>

        <template v-slot:append>
          <div class="justify-self-end">
            <router-link
              v-bind:to="`/editPost/${encodeURIComponent(getPostId())}/`"
            >
              <v-btn v-if="isAuthorsPost"
                ><v-icon class="me-1" icon="mdi-pencil"></v-icon
              ></v-btn>
            </router-link>
            <v-btn v-if="isAuthorsPost" @click="deletePost"
              ><v-icon class="me-1" icon="mdi-delete"></v-icon
            ></v-btn>
            <v-btn @click="likePost"
              ><v-icon class="me-1" icon="mdi-heart"></v-icon
            ></v-btn>
            <v-btn @click="sharePost"
              ><v-icon class="me-1" icon="mdi-share-variant"></v-icon
            ></v-btn>
          </div>
        </template>
      </v-list-item>
    </v-card-actions>

    <v-card class="mx-4" min-height="30vh">
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
      v-model="newComment"
      label="Comment"
      placeholder="Comment"
      clearable
      @keyup.enter="saveComment"
    />
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
import {router} from "../../main";
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
const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);
const loading = ref(true);

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

const isAuthorsPost = computed(() => {
  if (!props.postData.author) {
    return false;
  }
  let author_id = props.postData.author.id;
  console.log(author_id.endsWith(authorId), 8988);
  return author_id.endsWith(authorId);
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

async function likePost() {
  if (!props.postData.author) {
    return;
  }
  await createHTTP(
    `/authors/${encodeURIComponent(
      props.postData.author.id
    )}/posts/${encodeURIComponent(props.postData.id)}/likes/`
  )
    .post("")
    .then((response: { data: object }) => {
      console.log(response.data);
    });
}

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
    `/authors/${encodeURIComponent(
      props.postData.author.id
    )}/posts/${encodeURIComponent(props.postData.id)}/comments/`
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

  isImage.value =
    props.postData.author.contentType === "image/png;base64" ||
    props.postData.author.contentType === "image/jpeg;base64";
});

function getComments() {
  createHTTP(
    `authors/${encodeURI(props.postData.author.id)}/posts/${encodeURI(
      props.postData.id
    )}/comments/`
  )
    .get()
    .then((response) => {
      console.log(response.data, 4567);
      comments.value = response.data.comments;
    });
}

function getPostId() {
  return props.postData.id.substring(props.postData.id.lastIndexOf("/") + 1);
}

// defineProps<{ msg: string }>()
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
