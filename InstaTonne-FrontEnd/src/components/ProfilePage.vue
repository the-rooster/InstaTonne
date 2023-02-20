<template>
  <div
    class="viewBox"
  >
    <h3>
      InstaTonne Profile page
    </h3>
    <div class="flex-container">
      <img src="../assets/pfp.png">
      <a
        href="https://www.google.com/"
        class="flex-content"
      >
        <span class="followers"><br><br>{{ jsonData["Followers"] }} <br>Followers</span>
      </a>
      <a
        href="https://www.google.com/"
        class="flex-content"
      >
        <span class="followers"><br><br>{{ jsonData["Friends"] }} <br>Friends</span>
      </a>
    </div>
    <br>
    {{ jsonData["Bio"] }}
    <br>
    <div class="flex-container">
      <div
        v-for="i in numPosts"
        :key="i"
        class="flex-content"
      >
        <img
          src="https://via.placeholder.com/150"
        >
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import postJson from '../exampleBio.json'

  // eventually this will be replaced by some sort of backend call that grabs the profile info
  const jsonData = ref(postJson);
  const numPosts = jsonData.value["numPosts"]
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
  max-width: 36em;
}
.flex-content{
  width: 10em;
  height: 10em;
  padding: 1em
}
.viewBox{
  display: flex;
  flex-direction: column;
  align-items: center;
}
  </style>
  