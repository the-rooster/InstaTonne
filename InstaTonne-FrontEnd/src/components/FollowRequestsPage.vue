<template>
  <div
    class="viewBox"
  >
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em;"
      class="loadingIcon"
    />
    <div v-else>
      {{ }}
      <div style="display: flex;">
        <FollowRequestCard
          v-for="request in followRequests"
          :key="request.displayName"
          :request-data="request"
          :author-id="authorId"
          @update="removeRequest(request)"
        />
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue'
import FollowRequestCard from './stream_cards/FollowRequestCard.vue'
import { createHTTP, USER_AUTHOR_ID_COOKIE } from '../axiosCalls'
import Cookies from "js-cookie";

const loading = ref(true)
const postData = ref({});

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const removeRequest = ((request) => {
  const index = postData.value.items.indexOf(request)
  postData.value.items.splice(index, 1)
})

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/inbox/`).get().then((response: { data: object }) => {
    postData.value = response.data;
    loading.value = false;
  });
})

const followRequests = computed(() => postData.value?.items?.filter(item => item.type == "Follow" && item.accepted == false))

</script>

<style scoped>
</style>
  