<template>
  <div class="viewBox">
    <div class="profile-data-container">
      <img class="profile-picture mx-5" v-bind:src="profileData.profileImage" />
      <div class="profile-details">
        <h1>{{ profileData.displayName }}</h1>
        <h3>
          Github:
          <a v-bind:href="profileData.github">{{ profileData.github }}</a>
        </h3>
        <br />
        <h3>
          Server: <a v-bind:href="profileData.host">{{ profileData.host }}</a>
        </h3>
        <br />
        <h3 class="followers">Followers: {{ follow_count }}</h3>
        <br />
        <v-btn
          v-if="profileId === Cookies.get(USER_AUTHOR_ID_COOKIE)"
          v-bind:href="`/app/authors/${profileId}/edit`"
          >Edit Profile</v-btn
        >
        <v-btn class="FollowButton" v-else @click="follow()" :disabled="!canFollow"> Follow </v-btn>
      </div>
    </div>
    <br />
    <div class="post-container">
      <PostPreviewCard
        class="post-preview-card"
        v-for="post in posts"
        v-bind:key="post.id_url"
        v-bind:postData="post"
        v-bind:href="`/app/authors/${encodeURIComponent(
          profileData.id
        )}/posts/${encodeURIComponent(post.id)}/`"
      />
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
import { createHTTP } from "../axiosCalls";
import { USER_AUTHOR_ID_COOKIE } from "../constants";
import { useRoute } from "vue-router";
import Cookies from "js-cookie";
import PostPreviewCard from "./stream_cards/PostPreviewCard.vue";

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
  // encodeURIComponent(profileId)
  createHTTP(
    `authors/${Cookies.get(
      USER_AUTHOR_ID_COOKIE
    )}/followers/${encodeURIComponent(profileId)}`
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

.profile-data-container {
  display: flex;
  align-items: center;
}
.post-container {
  display: grid;
  grid-template-columns: auto auto auto;
  column-gap: 2em;
  max-width: 100%;
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
.profile-picture {
  width: 16vw;
  height: 16vw;
  border-radius: 100%;
}

.profile-details {
  margin-left: 1.5em;
  min-width: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.post-preview-card {
  width: 33vw;
  height: 33vw;
  margin: 1vw;
}
</style>
