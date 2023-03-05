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
        v-for="user in myVal"
        :key="user.displayName"
        class="flex-content"
        src="ProfilePage.vue"
      >
        <router-link v-bind:to="`ProfilePage/${encodeURIComponent(user.id)}/`">
          <AuthorCard
            :author-info="user"
            class="authorCard"
          />
        </router-link>
      </div>
    </div>
    <div class="arrows">
      <v-icon icon="mdi-arrow-left-bold-outline" size="x-large" @click="previousPage"></v-icon> 
      <div style="padding-left:2vw"/>
      <p>Page {{pageNum.page}}</p>
      <div style="padding-left:2vw"/>
      <v-icon icon="mdi-arrow-right-bold-outline" size="x-large" @click="nextPage"></v-icon>
    </div>
    
  </div>
</template>
  
<script setup lang="ts">
  import { ref, onBeforeMount, computed } from 'vue'
  import AuthorCard from './AuthorCard.vue'
  import { createHTTP } from '../axiosCalls'
import { reactive } from 'vue';
import { onBeforeUpdate } from 'vue';

  const loading = ref(true)
  const result : any[] = [];
  const postData = ref(result);
  const search = ref("")

  const pageSize = 5;
  const pageNum = reactive({"page" : 1});

  function nextPage(){

    pageNum.page++;
    fetchAuthors()
  }

  function previousPage(){

    if (pageNum.page > 1){
      pageNum.page--;
      fetchAuthors()
    }

  }

  async function fetchAuthors(){
    await createHTTP(`authors?page=${pageNum.page}&size=${pageSize}`).get().then((response: { data: object }) => {
      console.log("YUP");
      console.log(response);
      postData.value = response.data.items;
      loading.value = false;
    });
  }

  onBeforeMount(() => {fetchAuthors()
  });

  const myVal = computed({
  get() {
    return postData.value.filter(u => {
        return u.displayName.toLowerCase().indexOf(search.value.toLowerCase()) != -1;
      })
    // return postData.value
  },
  set(val) {
    return
  }
})

  // function filteredUsers() {
  //   // return postData.value.reduce((u: string) => {
  //   //   return u.toLowerCase().indexOf(this.search.toLowerCase()) != -1;
  //   // });
  //   return postData
  // }
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
    height: 18em;
    padding: 1em;
    /* border-style: solid; */
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
  .authorCard {
    width: 100%;
    height: 100%
  }
  .arrows {
    display:flex;
    flex-direction: row;
  }
</style>
  