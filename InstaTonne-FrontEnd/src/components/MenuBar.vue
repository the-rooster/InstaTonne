<template>
  <div
    style="
    border-width: 0.5em; 
    border-style: solid; 
    position: absolute; 
    background-color: lightcyan;
    width: 10em; 
    padding: 1em;
    "
  >
    <img
      src="../assets/EpicLogo.svg"
    >
    <h2>
      This is super temporary but will work for now!
    </h2>
    <div
      v-for="route in routes"
      :key="route.path"
      style="padding: 1em;"
    >
      <router-link :to="route.path">
        {{ route.path }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { routes } from '../main'

// class PageInfo {
//     path = '/HelloWorld'
//     displayName = ""
//     constructor(path = '/HelloWorld', displayName = "error: forgot to set displayName") {
//       this.path = path; 
//       this.displayName = displayName; 
//     }
// }

// import more pages and add them here!
// const pageList = [
//   new PageInfo('/HelloWorld', "Hello World!"),
//   new PageInfo(PostEditor, "Edit Posts"),
//   new PageInfo(ProfilePage, "Profile Page"),
//   new PageInfo(UserSearch, "User Search"),
//   new PageInfo(FollowRequests, "Follow Requests"),
// ]

// const currentPage = ref(pageList[0])

// function changePage(pageInfo = new PageInfo()) {
//   currentPage.value = pageInfo
// }

</script>

<style scoped>
img {
width: 7em;
height: 7em;
}
</style>
  