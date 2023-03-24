<template>
  <v-card class="mx-auto" color="#fff" theme="light" max-width="100%">
    <v-card-actions>
      <v-list-item class="w-100">
        <v-list-item-title>{{ author.displayName }}</v-list-item-title>
        <template v-slot:append>
          <div class="justify-self-end">
            <v-btn @click="likeComment"
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


async function likeComment() {
  await createHTTP(
    `/authors/${encodeURIComponent(props.postData.author.id)}/posts/${encodeURI(
      props.postData.id
    )}/comments/${props.commentData.id}/likes/`
  )
    .post("")
    .then((resp) => {
      return;
    });
}

onBeforeMount(() => {
  createHTTP(`/authors/${encodeURIComponent(props.postData.author.id)}/`)
  .get()
  .then((response) => {
    author.value = response.data;
  });
})



// defineProps<{ msg: string }>();
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>