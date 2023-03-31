<template>
  <v-card
    class="mx-auto my-5 rounded-l"
    color="#E3F2FD"
    theme="light"
    max-width="80%"
  >
    <v-card-actions>
      <v-list-item
        v-if="loading"
        class="w-100"
      >
        <v-progress-circular
          indeterminate
          width="20"
          size="100"
          class="loadingIcon"
        />
      </v-list-item>
      <v-list-item
        v-else
        class="w-100"
      >
        <v-list-item-title />
        <template #append>
          <router-link :to="`ProfilePage/${encodeURIComponent(requestData.url)}/`">
            <div>
              <img
                class="profile-picture"
                :src="requestData.profileImage"
              >
              {{ props.requestData.displayName }}
            </div>
          </router-link>
          <v-list-item>
            <v-btn @click="removeFriend">
              Remove
            </v-btn>
            {{ error }}
          </v-list-item>
        </template>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from "vue";
import AuthorCard from "../AuthorCard.vue";
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

async function removeFriend() {
  loading.value = true;
  const foreignId = encodeURIComponent(props.requestData.id);
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
