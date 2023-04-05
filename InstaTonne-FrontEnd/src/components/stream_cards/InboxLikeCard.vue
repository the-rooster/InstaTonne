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
          <div class="avatar-liked-container mt-2">
            <v-avatar
              size="70"
              color="grey-darken-3"
              :image="author.profileImage"
            ></v-avatar>
            <h3 class="who-liked">
              <a
                :href="`/app/ProfilePage/${encodeURIComponent(author.url)}/`"
                >{{ author.displayName }}</a
              >
              liked your
              <span v-if="isCommentLike">comment on the </span>
              <i> {{ postData.title }} </i> post!
            </h3>
          </div>
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
const isCommentLike = ref(false);

const props = defineProps({
  likeData: {
    type: Object,
    required: true,
  },
});

onBeforeMount(() => {
  let postId: string = props.likeData.object;

  let groups = postId.match(
    /(.*)\/authors\/(?<authorId>.*)\/posts\//
  )?.groups;

  let authorId = "";

  console.log(props.likeData, "LIKE DATA");

  // If props.likeData.object contains "comment", then it's a comment like. Remove the comment id from the string.
  if (props.likeData.object.includes("comment")) {
    isCommentLike.value = true;
    postId = postId.replace(/\/comments\/(.*)/, "");
  }

  if (groups) {
    authorId = groups.authorId;
  }
  postUrl.value = `authors/${encodeURIComponent(
    authorId
  )}/posts/${encodeURIComponent(postId)}/`;

  console.log("POSTID", postId);
  console.log("AUTHORID", authorId);
  createHTTP(
    `authors/${encodeURIComponent(authorId)}/posts/${encodeURIComponent(
      postId
    )}`
  )
    .get()
    .then((result) => {
      console.log("POSTASFSAF", result.data);
      postData.value = result.data;
    });

  createHTTP(`authors/${encodeURIComponent(props.likeData.author)}/`)
    .get()
    .then((response) => {
      console.log(response.data, 51515);
      author.value = response.data;
      console.log(response.data, 567);
    });
});

console.log(toRaw(props.likeData).id, 555);

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

.avatar-liked-container {
  display: flex;
  align-items: center;
  justify-content: left;
}

.who-liked {
  margin-left: 1rem;
}

.post-preview-card {
  min-width: 100;
  border-width: 0.1em;
  border-color: #fefefe;
}
</style>
