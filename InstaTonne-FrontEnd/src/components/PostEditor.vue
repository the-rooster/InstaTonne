<template>
  <div
    class="viewBox"
  >
    <div>
      <div style="display: flex;">
        <AuthorCard :author-info="postData.author" />
        <v-card>
          <template #title>
            Visibility:
          </template>
          <v-card-item>
            <v-radio-group v-model="postData.visibility">
              <v-radio
                label="public"
                value="PUBLIC"
              />
              <v-radio
                label="friends only"
                value="FRIENDS"
              />
            </v-radio-group>
          </v-card-item>
        </v-card>
      </div>
      Title:
      <v-textarea
        v-model="postData.title"
        clearable
      />
      Description:
      <v-textarea
        v-model="postData.description"
        clearable
      />
      Content:
      <ContentBox
        :content="postData.content"
        :content-type="postData.contentType"
        :editable="true"
      />
      Categories:
      <v-combobox
        v-model="postData.categories"
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
      <v-btn
        :disabled="disableSaving"
        @click="savePost"
      >
        SAVE
      </v-btn>
    </div>
  </div>
</template>
    
<script setup lang="ts">
import { ref, computed } from 'vue'
import AuthorCard from './AuthorCard.vue'
import ContentBox from './ContentBox.vue'
import { marked } from "marked";

const props = defineProps({
  postData: {
    type: Object,
    required: true,
  },
  saveFunction: {
    type: Function,
    required: true
  }
});

const postData = ref(props.postData) 

const disableSaving = computed(() => postData.value.source.length == 0 ||
postData.value.origin.length == 0 ||
postData.value.title.length == 0 ||
postData.value.content.length == 0 ||
postData.value.description.length == 0 ||
(postData.value.visibility != "PUBLIC" && postData.value.visibility != "FRIENDS"))

async function savePost() {
  props.saveFunction(postData.value)
}

</script>

<style scoped>
</style>