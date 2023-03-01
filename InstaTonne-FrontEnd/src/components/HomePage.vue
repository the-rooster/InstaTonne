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
import Cookies from 'js-cookie';
// defineProps<{ msg: string }>()

import {USER_AUTHOR_ID_COOKIE, createHTTP} from '../axiosCalls';

let posts = ref({});
let author_id = ref({"id" : 0});

createHTTP(`authors/${Cookies.get(USER_AUTHOR_ID_COOKIE)}/inbox/`).get().then((response) => {
        posts.value = response.data.items;
        console.log(response.data);
    })


</script>
  
<style scoped>
.read-the-docs {
color: #888;
}
</style>
  