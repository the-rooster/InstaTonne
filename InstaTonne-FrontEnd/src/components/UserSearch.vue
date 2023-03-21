<template>
  <div class="viewBox">
    <h2>User Search</h2>
    <!-- server list -->
    <h4 style="padding: 0px">Connected Servers</h4>
    <div class="server-list">
      <div v-for="server in servers" :key="server.host" class="server-display">
        <v-btn
          class="server-display"
          @click="
            () => {
              setServerShown(server.host);
            }
          "
          :disabled="servershown == server.host"
        >
          <h4>{{ server.host }}</h4>
        </v-btn>
      </div>
    </div>
    <br />
    <br />
    <div class="flex-container">
      <input v-model="search" type="text" placeholder="Search" /> <br />
    </div>
    <br />
    <br />
    <div class="flex-container">
      <div
        v-for="user in myVal"
        :key="user.displayName"
        class="flex-content"
        src="ProfilePage.vue"
      >
        <router-link v-bind:to="`ProfilePage/${encodeURIComponent(user.url)}/`">
          <AuthorCard :author-info="user" class="authorCard" />
        </router-link>
      </div>
    </div>
    <div class="arrows">
      <v-icon
        icon="mdi-arrow-left-bold-outline"
        size="x-large"
        @click="previousPage"
      ></v-icon>
      <div style="padding-left: 2vw" />
      <p>Page {{ pageNum.page }}</p>
      <div style="padding-left: 2vw" />
      <v-icon
        icon="mdi-arrow-right-bold-outline"
        size="x-large"
        @click="nextPage"
      ></v-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from "vue";
import AuthorCard from "./AuthorCard.vue";
import { createHTTP } from "../axiosCalls";
import { reactive } from "vue";
import { onBeforeUpdate } from "vue";

const loading = ref(true);
const result: any[] = [];
const authorsList = ref(result);
const search = ref("");

const pageSize = 5;
const pageNum = reactive({ page: 1 });

const servers = ref([]);
const servershown = ref("local");

function nextPage() {
  pageNum.page++;
  if (servershown.value == "local") {
    fetchAuthors();
    return;
  }
  fetchRemoteAuthors(servershown.value);
}

function previousPage() {
  if (pageNum.page > 1) {
    pageNum.page--;

    if (servershown.value == "local") {
      fetchAuthors();
      return;
    }
    fetchRemoteAuthors(servershown.value);
  }
}

async function getAllServers() {
  await createHTTP("connected-servers/")
    .get()
    .then((response: object) => {
      console.log("GOT CONNECTED SERVERS!!!!", response.data.servers);
      servers.value = [...response.data.servers, { host: "local" }];
    });
}

async function setServerShown(server: string) {
  servershown.value = server;
  pageNum.page = 1;

  if (server == "local") {
    fetchAuthors();
    return;
  }

  fetchRemoteAuthors(server);
}

async function fetchAuthors() {
  await createHTTP(`authors?page=${pageNum.page}&size=${pageSize}`)
    .get()
    .then((response: { data: object }) => {
      console.log("YUP");
      console.log(response);
      authorsList.value = response.data.items;
      loading.value = false;
    });
}

// fetch all authors from a remote server
async function fetchRemoteAuthors(server: string) {
  let total_remote_author_urls = encodeURI(
    "http://" + server + `/authors?page=${pageNum.page}&size=${pageSize}/`
  );
  await createHTTP(`remote-authors/${total_remote_author_urls}`)
    .get()
    .then((response) => {
      console.log("YUP");
      console.log(response);
      authorsList.value = response.data.items;
      loading.value = false;
    });
}

onBeforeMount(() => {
  fetchAuthors();
  getAllServers();
});

const myVal = computed({
  get() {
    return authorsList.value.filter((u) => {
      return (
        u.displayName.toLowerCase().indexOf(search.value.toLowerCase()) != -1
      );
    });
    // return authorsList.value
  },
  set(val) {
    return;
  },
});

// function filteredUsers() {
//   // return authorsList.value.reduce((u: string) => {
//   //   return u.toLowerCase().indexOf(this.search.toLowerCase()) != -1;
//   // });
//   return authorsList
// }
</script>

<style scoped>
.server-list {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: space-between;
}

.server-display {
  color: #888;
  margin-left: 0.1vw;
  margin-right: 0.1vw;
}

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
.flex-content {
  width: 30em;
  height: 18em;
  padding: 1em;
  /* border-style: solid; */
}
.viewBox {
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
  height: 100%;
}
.arrows {
  display: flex;
  flex-direction: row;
}
</style>
