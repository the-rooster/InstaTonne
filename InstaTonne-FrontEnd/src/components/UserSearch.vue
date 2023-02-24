<template>
  <div
    class="viewBox"
  >
    <h3>
      User Search
    </h3>
    <div class="flex-container">
      <input
        v-model="search"
        type="text"
        placeholder="Search"
      > <br>
    </div>
    <br>
    <br>
    <div class="flex-container">
      <div
        v-for="user in postData"
        :key="user"
        class="flex-content"
        src="ProfilePage.vue"
      >
        <router-link to="/ProfilePage">
          <AuthorCard :author-info="postData.author" />
        </router-link>
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref, onBeforeMount } from 'vue'
  import AuthorCard from './AuthorCard.vue'
  import createHTTP from '../axiosCalls'

  const loading = ref(true)
  const postData = ref({});
  onBeforeMount(async () => {
    await createHTTP('authors?page=1&size=2').get().then((response: { data: object }) => {
      postData.value = response.data;
      loading.value = false;
    });
  })
  </script>
  
  <style scoped>
  .read-the-docs {
    color: #888;
  }
  .flex-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  flex-basis: 0;
  max-width: 32em;
}
.flex-content{
  width: 30em;
  height: 2em;
  padding: 1em;
  border-style: solid;
}
.viewBox{
  display: flex;
  flex-direction: column;
  align-items: center;
}
br {
   display: block;
   margin: 1em;
}
  </style>
  