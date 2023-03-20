<!-- InstaTonne-FrontEnd/src/components/FollowRequestsPage.vue -->
<!--
  Copyright (c) 2023 CMPUT 404 W2023 Group 6

  This file is part of InstaTonne.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  Description:
  This component is part of InstaTonne and provides authentication functionality.
-->

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
    <div v-else>
      {{}}
      <div style="display: flex">
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
import { ref, onBeforeMount, computed } from "vue";
import FollowRequestCard from "./stream_cards/FollowRequestCard.vue";
import { createHTTP, USER_AUTHOR_ID_COOKIE } from "../axiosCalls";
import Cookies from "js-cookie";

const loading = ref(true);
const postData = ref({});

const authorId = Cookies.get(USER_AUTHOR_ID_COOKIE);

const removeRequest = (request) => {
  const index = postData.value.items.indexOf(request);
  postData.value.items.splice(index, 1);
};

onBeforeMount(async () => {
  await createHTTP(`authors/${authorId}/inbox/`)
    .get()
    .then((response: { data: object }) => {
      postData.value = response.data;
      loading.value = false;
    });
});

const followRequests = computed(() =>
  postData.value?.items?.filter(
    (item) => item.type == "Follow" && item.accepted == false
  )
);
</script>

<style scoped></style>
