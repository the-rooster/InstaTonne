<template>
  <div class="viewBox">
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em"
      class="loadingIcon"
    />
    <div v-else class="flex-container">
      <div class="followers">
        <b>Followers</b>
        <div
          v-if="followers.length > 0"
          style="display: flex; flex-direction: column"
        >
          <div v-for="follower in followers" :key="follower.displayName">
            <FriendCard
              :key="follower"
              :request-data="follower"
              :author-id="authorId"
              style="margin: 1em"
            />
          </div>
        </div>
        <div v-else>No Followers :(</div>
      </div>
      <div class="requests">
        <b>Follow Requests</b>
        <div
          v-if="followRequests.length > 0"
          style="display: flex; flex-direction: column"
        >
          <div v-for="request in followRequests" :key="request.displayName">
            <FollowRequestCard
              :key="request.displayName"
              :request-data="request"
              :author-id="authorId"
              style="margin: 1em"
              @update="removeRequest(request)"
            />
          </div>
        </div>
        <div v-else>No Follow Requests</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from "vue";
import FriendCard from "./stream_cards/FriendCard.vue";
import FollowRequestCard from "./stream_cards/FollowRequestCard.vue";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "../axiosCalls";
import Cookies from "js-cookie";

const loading = ref(true);
// number of calls to make
const loadingCounter = ref(2);
const followersData = ref({});
const requestData = ref({});

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const removeRequest = (request) => {
  const index = requestData.value.items.indexOf(request);
  requestData.value.items.splice(index, 1);
};

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/followers/`)
    .get()
    .then((response: { data: object }) => {
      followersData.value = response.data;
      loadingCounter.value = loadingCounter.value - 1;
      if (loadingCounter.value == 0) {
        loading.value = false;
      }
    });
  await createHTTP(`authors/${authorId}/inbox/`)
    .get()
    .then((response: { data: object }) => {
      requestData.value = response.data;
      loadingCounter.value = loadingCounter.value - 1;
      if (loadingCounter.value == 0) {
        loading.value = false;
      }
    });
});

const followers = computed(() => followersData.value?.items);
const followRequests = computed(() =>
  requestData.value?.items?.filter(
    (item) => item.type == "Follow" && item.accepted == false
  )
);
</script>

<style scoped>
.flex-container {
  display: flex;
  grid-auto-columns: minmax(0, 1fr);
  grid-auto-flow: row;
  width: 100%;
}
.viewBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.followers {
  width: 50%;
}
.requests {
  width: 50%;
}
</style>
