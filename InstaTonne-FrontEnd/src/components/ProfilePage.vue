<template>
  <div class="viewBox">
    <!-- <h3>
      InstaTonne Profile page
    </h3> -->
    <br />
    <h1>{{ profileData.displayName }}</h1>
    <br />
    <v-btn
      v-if="profileId === Cookies.get(USER_AUTHOR_ID_COOKIE)"
      v-bind:href="`/app/authors/${profileId}/edit`"
      >Edit Profile</v-btn
    >
    <a v-bind:href="profileData.github"
      ><p>Github: {{ profileData.github }}</p></a
    >
    <a v-bind:href="profileData.host"
      ><p>Origin: {{ profileData.host }}</p></a
    >
    <br />
    <div class="flex-container">
      <img class="profile-picture" v-bind:src="profileData.profileImage" />
      <a class="flex-content">
        <span class="followers"><br /><br />Followers: {{ follow_count }}</span>
      </a>
    </div>
    <v-btn @click="follow()" :disabled="!canFollow"> Follow </v-btn>
    <br />
    <br />
    <div class="flex-container">
      <div v-for="post in posts" :key="post.id" class="post-tiny">
        <a
          v-bind:href="`/app/authors/${encodeURIComponent(
            profileData.id
          )}/posts/${encodeURIComponent(post.id)}/`"
        >
          <div class="post-tiny">
            <h1
              style="
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 100%;
                overflow: hidden;
              "
            >
              {{ post.title }}
            </h1>
            <span
              style="
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 100%;
                overflow: hidden;
              "
              >{{ post.description }}</span
            >
          </div>
        </a>
      </div>
      <v-snackbar v-model="showStatus">
        {{ statusMessage }}

        <template #actions>
          <v-btn color="blue" variant="text" @click="statusMessage = ''">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { USER_AUTHOR_ID_COOKIE, createHTTP } from "../axiosCalls";
import { useRoute } from "vue-router";
import Cookies from "js-cookie";

const route = useRoute();

const profileData = ref({});
const followers = ref({});
const follow_count = ref(0);
const posts = ref({});
const canFollow = ref(false);

onMounted(() => {
  // get profile here
  createHTTP(`authors/${profileId}/`)
    .get()
    .then((response) => {
      console.log(response.data, 51515);
      profileData.value = response.data;
      console.log(response.data, 567);
    });

  // see if we can follow this user
  createHTTP(
    `authors/${encodeURIComponent(profileId)}/followers/${Cookies.get(
      USER_AUTHOR_ID_COOKIE
    )}`
  )
    .get()
    .then((response) => {
      canFollow.value = false;
    })
    .catch((e) => {
      console.log(e, 13123123123);
      canFollow.value = true;
    });

  createHTTP(`authors/${profileId}/followers`)
    .get()
    .then((response) => {
      console.log(response, 123123123);
      let data = response.data;
      console.log(data, 51515);
      followers.value = data.items;
      follow_count.value = data.items.length;
      console.log(response.data, 567);
    });

  createHTTP(`authors/${profileId}/posts`)
    .get()
    .then((response) => {
      let data = response.data;
      console.log(data, 5124124);
      posts.value = data.items;
      console.log(response.data, 567);
    });
});

let profileId = route.params.id;
const statusMessage = ref("");
const showStatus = computed(() => statusMessage.value.length > 0);

function follow() {
  createHTTP(
    `authors/${encodeURIComponent(profileId)}/followers/${Cookies.get(
      USER_AUTHOR_ID_COOKIE
    )}`
  )
    .post("")
    .then((response) => {
      canFollow.value = false;
      statusMessage.value = "Follow request sent to user!";
    })
    .catch((e) => {
      console.log(e, 13123123123);
      canFollow.value = true;
      statusMessage.value = "Failed to follow user!";
    });
}

// eventually this will be replaced by some sort of backend call that grabs the profile info
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
.flex-container {
  display: grid;
  grid-template-columns: auto auto auto;
  max-width: 36em;
}
.flex-content {
  width: 10em;
  height: 10em;
  padding: 2em;
}
.viewBox {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.post-tiny {
  border: 0.2em solid black;
  padding: 1em;
  margin: 1em;
  width: 10vw;
  height: 10vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 60%;
}

.profile-picture {
  width: 9vw;
  height: 9vw;
  border-radius: 100%;
}
</style>
