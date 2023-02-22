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
        @click="changePage(pageList[2])"
      >
        {{ user }}
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import postJson from '../exampleUsers.json'
  import pageList from './MenuBar.vue'
  import changePage from './MenuBar.vue'
  // eventually this will be replaced by some sort of backend call that grabs the profile info
  </script>

  <script lang="ts">
  const jsonData = ref(postJson);

  export default {
  data() {
    return {
      users:
        jsonData.value["Users"]
      ,
      search: ""
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(u => {
        return u.toLowerCase().indexOf(this.search.toLowerCase()) != -1;
      });
    }
  }
};
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
  