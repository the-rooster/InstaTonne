<template>
  <v-card class="mx-auto" color="#fff" theme="light" max-width="400">
    <v-card-actions>
      <v-list-item class="w-100">
        <v-list-item-title>{{
          props.commentData.author?.displayName
        }}</v-list-item-title>
        <template v-slot:append>
          <div class="justify-self-end">
            <v-icon class="me-1" icon="mdi-heart"></v-icon>
          </div>
        </template>
        <v-list-item>{{ props.commentData.comment }}</v-list-item>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps({
  commentData: {
    type: Object,
    required: true,
  },
});

console.log(props.commentData, 34879);

// defineProps<{ msg: string }>();
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
