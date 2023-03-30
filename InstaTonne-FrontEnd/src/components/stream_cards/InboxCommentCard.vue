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
          <div class="avatar-comment-container mt-2">
            <v-avatar
              size="70"
              color="grey-darken-3"
              :image="commentData.author.profileImage"
            ></v-avatar>
            <h3 class="who-commented">
              <a
                :href="`/app/ProfilePage/${encodeURIComponent(
                  commentData.author.url
                )}/`"
              >
                {{ commentData.author.displayName }}
              </a>
              commented on your <i>{{ postData.title }} </i> post:
            </h3>
          </div>
          <h4 class="comment-content">
            <v-list-item
              ><i> {{ props.commentData.comment }}</i></v-list-item
            >
          </h4>
          <div class="preview-card-container">
            <PostPreviewCard
              class="post-preview-card"
              :postData="postData"
              :href="postUrl"
            />
          </div>
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
    .then((response) => {
      author.value = response.data;
    });
});

// defineProps<{ msg: string }>();
</script>

<style scoped>
.read-the-docs {
  color: #888;
}

.avatar-comment-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.who-commented {
  margin-left: 1rem;
}
</style>
