<template>
  <div
    class="viewBox"
  >
    <!-- <h3>
      InstaTonne Profile page
    </h3> -->
    <br>
    <h1>{{profileData.displayName}}</h1>
    <br>
    <a v-bind:href="profileData.github"><p>Github: {{profileData.github}}</p></a>
    <a v-bind:href="profileData.host"><p>Origin: {{profileData.host}}</p></a>
    <br>
    <div class="flex-container">
      <img class="profile-picture" v-bind:src="profileData.profileImage">
      <a
        class="flex-content"
      >
        <span class="followers"><br><br>Followers: {{ follow_count }}</span>
      </a>
    </div>
    <br>

    <br>
    <div class="flex-container">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-tiny"
      >
      <a v-bind:href="`/authors/${encodeURIComponent(profileData.id)}/posts/${encodeURIComponent(post.id)}/`">
      <div class="post-tiny">
        <h1 style="text-overflow:ellipsis;white-space:nowrap;max-width:100%;overflow:hidden">{{post.title}}</h1>
        <span style="text-overflow:ellipsis;white-space:nowrap;max-width:100%;overflow:hidden" >{{post.description}}</span>
      </div>
      </a>
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { USER_AUTHOR_ID_COOKIE, createHTTP } from '../axiosCalls';
  import {useRoute} from "vue-router";
  import Cookies from "js-cookie";

  const route = useRoute();

  const profileData = ref({});
  const followers = ref({});
  const follow_count = ref(0);
  const posts = ref({});

  let profileId = route.params.id;

  if (!profileId){
    profileId = Cookies.get(USER_AUTHOR_ID_COOKIE);
  }

  createHTTP(`authors/${profileId}/`)
  .get()
  .then((response) => {
    console.log(response.data, 51515);
    profileData.value = response.data;
    console.log(response.data, 567);
  });

  createHTTP(`authors/${profileId}/followers/`)
  .get()
  .then((response) => {
    let data = response.data[0]
    console.log(data, 51515);
    followers.value = data.items;
    follow_count.value = data.items.length;
    console.log(response.data, 567);
  });

  createHTTP(`authors/${profileId}/posts/`)
  .get()
  .then((response) => {
    let data = response.data
    console.log(data, 5124124);
    posts.value = data.items;
    console.log(response.data, 567);
  });

  

  // eventually this will be replaced by some sort of backend call that grabs the profile info

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
  justify-content: space-around;
}
.flex-content{
  width: 10em;
  height: 10em;
  padding: 2em;
}
.viewBox{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.post-tiny {


  border: 0.2em solid black;
  padding: 1em;
  margin: 1em;
  width: 10vw;
  height:10vw;
  display:flex;
  flex-direction:column;
  justify-content: center;
  align-items: center;
  font-size: 60%
}

.profile-picture {
  width: 9vw;
  height: 9vw;
  border-radius: 100%;
}
  </style>
  