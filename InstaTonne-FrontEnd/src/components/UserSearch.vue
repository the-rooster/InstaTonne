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
        v-for="user in filteredUsers"
        :key="user"
        class="flex-content"
        src="ProfilePage.vue"
      >
        {{ user }}
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
  import { ref, computed } from 'vue'
  import postJson from '../exampleUsers.json'
  // eventually this will be replaced by some sort of backend call that grabs the profile info

  const jsonData = ref(postJson);

  const users = ref(jsonData.value["Users"])

  const search = ref("")

  const filteredUsers = computed(() => 
    users.value.filter(u => u.toLowerCase().indexOf(search.value.toLowerCase()) != -1))

</script>

<style scoped>
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
  