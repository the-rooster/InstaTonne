<!-- InstaTonne-FrontEnd/src/components/AuthorCard.vue -->
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
  <v-card :elevation="10" class="authorBox">
    {{ props.authorInfo?.displayName }}

    <v-card-item>
      <img
        v-if="props.authorInfo?.profileImage"
        :src="props.authorInfo?.profileImage"
        class="profile-picture"
      />
      <img v-else class="profile-picture" src="../assets/EpicLogo.svg" />
    </v-card-item>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  authorInfo: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.authorBox {
  width: 20vw;
  height: 20vh;
  background-color: rgb(214, 227, 222);
  justify-content: center;
}
.profile-picture {
  width: 60%;
  height: 60%;

  border-radius: 100%;
}
</style>
