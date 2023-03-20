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
        <v-list-item-title />
        <template #append>
          {{
            props.requestData.displayName
          }}
        </template>
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
</script>

<style scoped>
.read-the-docs {
color: #888;
}
</style>
  