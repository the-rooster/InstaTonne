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
      Followers
      <div
        v-if="followers.length > 0"
        style="display: flex; flex-direction: column;"
      >
        <FriendCard
          v-for="request in followers"
          :key="request"
          :request-data="request"
          :author-id="authorId"
          style="margin: 1em;"
        />
      </div>
      <div v-else> 
        No Followers :(
      </div>
      Follow Requests
      <div
        v-if="followRequests.length > 0"
        style="display: flex; flex-direction: column;"
      >
        <FollowRequestCard
          v-for="request in followRequests"
          :key="request.displayName"
          :request-data="request"
          :author-id="authorId"
          style="margin: 1em;"
          @update="removeRequest(request)"
        />
      </div>
      <div v-else> 
        No Follow Requests
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue'
import FriendCard from './stream_cards/FriendCard.vue'
import FollowRequestCard from './stream_cards/FollowRequestCard.vue'
import { createHTTP, USER_AUTHOR_ID_COOKIE } from '../axiosCalls'
import Cookies from "js-cookie";

const loading = ref(true)
// number of calls to make
const loadingCounter = ref(3);
const followingData = ref({});
const followersData = ref({});
const requestData = ref({});

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const removeRequest = ((request) => {
  const index = requestData.value.items.indexOf(request)
  requestData.value.items.splice(index, 1)
})

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/followers/${encodeURI("http://127.0.0.1:8000")}/authors/1/`).get().then((response: { data: object }) => {
    followingData.value = response.data;
    loadingCounter.value = loadingCounter.value - 1;
    if (loadingCounter.value == 0) {
      loading.value = false;
    }
  });
  await createHTTP(`authors/${authorId}/followers/`).get().then((response: { data: object }) => {
    followersData.value = response.data;
    loadingCounter.value = loadingCounter.value - 1;
    if (loadingCounter.value == 0) {
      loading.value = false;
    }
  });
  await createHTTP(`authors/${authorId}/inbox/`).get().then((response: { data: object }) => {
    requestData.value = response.data;
    loadingCounter.value = loadingCounter.value - 1;
    if (loadingCounter.value == 0) {
      loading.value = false;
    }
  });

})

const followers = computed(() => followersData.value?.items)
const followRequests = computed(() => requestData.value?.items?.filter(item => item.type == "Follow" && item.accepted == false))

</script>

<style scoped>
</style>
  