<template>
  <v-card
    class="mx-auto"
    color="#fff"
    theme="light"
    max-width="400"
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
        <v-list-item-title>
          <AuthorCard :author-info="props.requestData.actor" />
        </v-list-item-title>
        <template #append>
          {{
            props.requestData.displayName
          }}
          <div class="justify-self-end">
            <v-icon
              class="me-1"
              icon="mdi-heart"
            />
          </div>
        </template>
        <v-list-item>{{ props.requestData.summary }}</v-list-item>
        <v-list-item>
          <v-btn @click="acceptRequest()">
            Accept
          </v-btn>
          <v-btn @click="rejectRequest">
            Reject
          </v-btn>
          {{ error }}
        </v-list-item>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import AuthorCard from "../AuthorCard.vue"
import { createHTTP,  } from '../../axiosCalls'

const loading = ref(false)

const props = defineProps({
    requestData: {
        type: Object,
        required: true,
    },
    authorId: {
        type: Number,
        required: true
    }
});

const emit = defineEmits(['update'])

const error = ref("")

async function acceptRequest() {
  loading.value = true;
  const foreignId = encodeURIComponent(props.requestData.actor.id)
  await createHTTP(`authors/${props.authorId}/followers/${foreignId}`).put(JSON.stringify({})).then(() => {
    emit('update')
    loading.value = false;
  });
}

async function rejectRequest() {
  loading.value = true;
  const foreignId = encodeURIComponent(props.requestData.actor.id)
  await createHTTP(`authors/${props.authorId}/followers/${foreignId}`).delete(JSON.stringify({})).then(() => {
    emit('update')
    loading.value = false;
  });
}
</script>

<style scoped>
.read-the-docs {
color: #888;
}
</style>
  