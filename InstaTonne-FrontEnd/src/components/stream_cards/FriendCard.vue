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
      <v-row
        v-else
        class="flex-container"
      >
        <v-col>
          <router-link
            id="router"
            :to="`ProfilePage/${encodeURIComponent(requestData.url)}/`"
            class="flex-container"
          >
            <v-col>
              <img
                class="profile-picture"
                src="../../assets/pfp.png"
              >
            </v-col>
            <v-col class="d-flex justify-center align-center">
              <div>
                <h2>{{ props.requestData.displayName }}</h2>
                <h3>GitHub: {{ props.requestData.github }}</h3>
              </div>
            </v-col>
          </router-link>
        </v-col>
        <v-col
          cols="3"
          class="d-flex justify-center align-center"
        >
          <v-btn @click="removeFriend">
            Remove
          </v-btn>
          {{ error }}
        </v-col>
      </v-row>
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
.flex-container {
  display: flex;
  grid-auto-flow: row;
  width: 100%;
  justify-content: space-around;
}
#router {
  width: px;
}
</style>
