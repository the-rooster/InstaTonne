<template>
  <v-card
    class="my-5 rounded-xl"
    color="#E3F2FD"
    theme="light"
    max-width="100%"
  >
    <v-card-actions>
      <v-list-item class="w-100">
        <v-list-item-title>{{
          props.commentData.author.displayName
        }}</v-list-item-title>
        <template v-slot:append>
          <p>{{ likeCount }} Likes</p>
          <div class="justify-self-end">
            <v-btn v-if="likedComment"
              ><v-icon class="me-1" icon="mdi-heart" color="blue" />
            </v-btn>
            <v-btn v-else @click="likeComment"
              ><v-icon class="me-1" icon="mdi-heart" />
            </v-btn>
          </div>
        </template>
        <v-list-item>{{ props.commentData.comment }}</v-list-item>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { onBeforeMount } from "vue";
import { createHTTP } from "../../axiosCalls";
import { defineProps, ref, toRaw } from "vue";

let author = ref({});

const props = defineProps({
  commentData: {
    type: Object,
    required: true,
  },
  postData: {
    type: Object,
    required: true,
  },
});

const likedComment = ref(false);

async function likeComment() {
  await createHTTP(
    `/authors/${encodeURI(props.postData.author.id)}/posts/${encodeURI(
      props.postData.id
    )}/comments/${props.commentData.id}/likes/`
  )
    .post("")
    .then((resp) => {
      likedComment.value = true;
      likeCount.value++;
      this.$forceUpdate();
      return;
    });
}

const likeCount = ref(0);

async function getCommentLikeCount() {
  await createHTTP(
    `/authors/${encodeURI(props.postData.origin)}/comments/${
      props.commentData.id
    }/likes/`
  )
    .get()
    .then((resp) => {
      console.log(
        "checking if comment liked",
        resp.data.items.length,
        resp.data
      );
      likeCount.value = resp.data.items.length;
    });
}

onBeforeMount(() => {
  getCommentLikeCount();
  createHTTP(toRaw(props.commentData).author)
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
</style>
