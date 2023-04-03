<template>
  <v-card
    class="mx-auto my-5 rounded-xl"
    color="#E3F2FD"
    theme="light"
    max-width="80%"
  >
    <v-card-actions>
      <v-list-item v-if="loading" class="w-100">
        <v-progress-circular
          indeterminate
          width="20"
          size="100"
          class="loadingIcon"
        />
      </v-list-item>
      <v-row v-else class="flex-container">
        <v-col>
          <router-link
            id="router"
            :to="`ProfilePage/${encodeURIComponent(requestData.url)}/`"
            class="flex-container"
          >
            <v-col>
              <img class="profile-picture" :src="requestData.profileImage" />
            </v-col>
            <v-col class="d-flex justify-center align-center">
              <div>
                <h2>{{ props.requestData.displayName }}</h2>
                <h3>GitHub: {{ props.requestData.github }}</h3>
              </div>
            </v-col>
          </router-link>
        </v-col>
        <v-col cols="3" class="d-flex justify-center align-center">
          <ConfirmationModal
            ref="showConfirmation"
            message="Are you sure you want to remove this friend?"
            @selected="(value) => removeFriend(value)"
          />
          <v-btn
            class="remove-button"
            @click="
              () => {
                showConfirmation.show = true;
              }
            "
          >
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
import { createHTTP } from "../../axiosCalls";
import ConfirmationModal from "../ConfirmationModal.vue";

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
const showConfirmation = ref(false);

const error = ref("");

async function removeFriend(value: boolean) {
  if (value) {
    loading.value = true;
    const foreignId = encodeURIComponent(props.requestData.id);
    await createHTTP(`authors/${props.authorId}/followers/${foreignId}`)
      .delete(JSON.stringify({}))
      .then(() => {
        emit("update");
        loading.value = false;
      });
  }
  showConfirmation.value = false;
  window.location.reload();
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
.profile-picture {
  width: 16vw;
  height: 16vw;
  border-radius: 100%;
}

.remove-button {
  background-color: #ff9797;
  color: #000000;
}

#router {
  width: px;
}
</style>
