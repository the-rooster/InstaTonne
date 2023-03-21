<template>
  <v-card class="mx-auto" color="#eee" theme="light" max-width="80%">
    <v-card-actions>
      <v-list-item v-if="loading" class="w-100">
        <v-progress-circular
          indeterminate
          width="20"
          size="100"
          class="loadingIcon"
        />
      </v-list-item>
      <v-list-item v-else class="w-100">
        <template #append>
          {{ props.requestData.displayName }}
        </template>
        <v-list-item>
          <router-link
            :to="`ProfilePage/${encodeURIComponent(
              props.requestData.actor.id
            )}/`"
          >
            {{ props.requestData.summary }}
          </router-link>
        </v-list-item>
        <v-list-item>
          <v-btn @click="acceptRequest()"> Accept </v-btn>
          <v-btn @click="rejectRequest"> Reject </v-btn>
          {{ error }}
        </v-list-item>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { createHTTP } from "../../axiosCalls";

const loading = ref(false);

const props = defineProps({
  requestData: {
    type: Object,
    required: true,
  },
  authorId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["update"]);

const error = ref("");

async function acceptRequest() {
  loading.value = true;
  const foreignId = encodeURIComponent(props.requestData.actor.id);
  await createHTTP(`authors/${props.authorId}/followers/${foreignId}`)
    .put(JSON.stringify({}))
    .then(() => {
      emit("update");
      loading.value = false;
    });
}

async function rejectRequest() {
  loading.value = true;
  const foreignId = encodeURIComponent(props.requestData.actor.id);
  await createHTTP(`authors/${props.authorId}/followers/${foreignId}`)
    .delete(JSON.stringify({}))
    .then(() => {
      emit("update");
      loading.value = false;
    });
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
