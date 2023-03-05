import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";

import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

import axios from "axios";
import VueAxios from "vue-axios";

import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "light",
  },
});

// 1. Define route components.
// These can be imported from other files
import HomePage from "./components/HomePage.vue";
import AboutPage from "./components/AboutPage.vue";
import HelloWorld from "./components/HelloWorld.vue";
import PostEditor from "./components/PostEditor.vue";
import FollowRequests from "./components/FollowRequests.vue";
import ProfilePage from "./components/ProfilePage.vue";
import UserSearch from "./components/UserSearch.vue";
import UserPost from "./components/UserPost.vue";
// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/posteditor/:postid/", name: "PostEditor", component: PostEditor },
  {
    path: "/FollowRequests",
    name: "FollowRequests",
    component: FollowRequests,
  },
  { path: "/ProfilePage", name: "ProfilePage", component: ProfilePage },
  { path: "/UserSearch", name: "UserSearch", component: UserSearch },
  {path: "/authors/:id/posts/:postid",name : "UserPost", component: UserPost}
];

export const nav_bar_routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/about", name: "About", component: AboutPage },
  {
    path: "/FollowRequests",
    name: "FollowRequests",
    component: FollowRequests,
  },
  { path: "/ProfilePage", name: "ProfilePage", component: ProfilePage },
  { path: "/UserSearch", name: "UserSearch", component: UserSearch },
];

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
export const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHistory(),
  routes, // short for `routes: routes`
});

// 5. Create and mount the root instance.
// Make sure to _use_ the router instance to make the
// whole app router-aware.

const app = createApp(App);
// const app = createApp({
//   router: router,
//   component: App
// })
app.use(vuetify);
app.use(router);

app.use(VueAxios, axios);

app.mount("#app");

// Now the app has started!
export { routes };
