<template>
  <div class="viewBox">
    <div>

      <v-text-field
        v-model="postData.title"
        label="Title"
        class="my-10"
        id="TitleInput"
        clearable
      />
      <v-select
        v-model="postData.contentType"
        label="Content Type"
        :items="[
          'text/markdown',
          'text/plain',
          'application/base64',
          'image/png;base64',
          'image/jpeg;base64',
        ]"
        class="my-10"
      />
      <v-file-input
        v-if="
          postData.contentType == 'image/png;base64' ||
          postData.contentType == 'image/jpeg;base64'
        "
        v-model="postData.content"
        label="Upload image"
        variant="filled"
        prepend-icon="mdi-camera"
        class="my-10"
        accept="image/*"
      />
      <v-textarea
        v-else
        v-model="postData.content"
        label="Content"
        class="my-10"
        id="ContentInput"
        clearable
      />
      <v-textarea
        v-model="postData.description"
        label="Description"
        class="my-10"
        id="DescriptionInput"
        clearable
      />
      <v-select
        v-model="postData.visibility"
        label="Visibility"
        :items="['PUBLIC', 'FRIENDS']"
        id="VisibilitySelector"
        class="my-10"
      />
      <v-combobox
        v-model="postData.categories"
        label="Categories"
        class="my-10"
        chips
        clearable
        multiple
      >
        <template #selection="{ attrs, item, select, selected }">
          <v-chip
            v-bind="attrs"
            :model-value="selected"
            closable
            @click="select"
            @click:close="remove(item)"
          >
            {{ item }}
          </v-chip>
        </template>
      </v-combobox>
      <v-checkbox v-model="postData.unlisted" label="Unlisted"></v-checkbox>
      <v-btn :disabled="disableSaving" @click="savePost" id="SaveButton"> SAVE </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { router } from "../main";
import AuthorCard from "./AuthorCard.vue";

const props = defineProps({
  postData: {
    type: Object,
    required: true,
  },
  saveFunction: {
    type: Function,
    required: true,
  },
});

const postData = ref(props.postData);

const disableSaving = computed(
  () =>
    postData.value.title.length == 0 ||
    postData.value.content.length == 0 ||
    postData.value.description.length == 0 ||
    (postData.value.visibility != "PUBLIC" &&
      postData.value.visibility != "FRIENDS")
  // (postData.value.contentType != "Text" &&
  //   postData.value.contentType != "Image")
);

async function savePost() {
  props.saveFunction(postData.value);
  // Go to home page
  router.push({ path: "/" });
}
</script>

<style scoped></style>
