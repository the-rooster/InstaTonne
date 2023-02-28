<template>
  <div class="viewBox">
    <h1>Your Stream</h1>
    <br>
    <div style="overflow-y:scroll;max-height:90em">
        <div v-for="item in posts" v-bind:key="item.id_url">
            <PostFullCard v-bind:postData="item" v-if="item.type='post'"></PostFullCard>
        </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import PostFullCard from './stream_cards/PostFullCard.vue';

// defineProps<{ msg: string }>()

import {createHTTP} from '../axiosCalls';

let posts = ref({});
let author_id = ref({"id" : 0});

createHTTP("authors/id/").post("").then((data) => {
    console.log(data);
    author_id.value.id = data.id;
}).then(() => {
    //update posts from inbox here
    createHTTP(`authors/${author_id.value.id}/inbox/`).get().then((response) => {
        posts.value = response.data.items;
        console.log(response.data);
    })
})


</script>
  
<style scoped>
.read-the-docs {
color: #888;
}
</style>
  