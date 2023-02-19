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
      v-for="page in pageList"
      :key="page.displayName"
      style="padding: 1em;"
    >
      <button
        type="button" 
        @click="changePage(page)"
      >
        {{ page.displayName }}
      </button>
    </div>
    <p>
      currentPage: {{ currentPage.displayName }}
    </p>
  </div>
  <component :is="currentPage.component" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HelloWorld from './HelloWorld.vue'
import PostEditor from './PostEditor.vue'

class PageInfo {
    component = HelloWorld
    displayName = ""
    constructor(component = HelloWorld, displayName = "error: forgot to set displayName") {
      this.component = component; 
      this.displayName = displayName; 
    }
}

// import more pages and add them here!
const pageList = [
  new PageInfo(HelloWorld, "Hello World!"),
  new PageInfo(PostEditor, "Edit Posts")
]

const currentPage = ref(pageList[0])

function changePage(pageInfo = new PageInfo()) {
  currentPage.value = pageInfo
}

</script>

<style scoped>
img {
width: 7em;
height: 7em;
}
</style>
  