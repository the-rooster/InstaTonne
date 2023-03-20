<!-- InstaTonne-FrontEnd/src/components/ErrorPage.vue -->
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
    {{ props.errorMessage }}
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  errorMessage: {
    type: String,
    default: "404 Page Not Found",
  },
});
</script>

<style scoped></style>
