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

import Cookies from "js-cookie";

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
import EditPostPage from "./components/EditPostPage.vue";
import CreatePostPage from "./components/CreatePostPage.vue";
import ProfilePage from "./components/ProfilePage.vue";
import UserSearch from "./components/UserSearch.vue";
import UserPost from "./components/UserPost.vue";
import FriendsPage from "./components/FriendsPage.vue";
import EditProfilePage from "./components/EditProfilePage.vue";
import { USER_AUTHOR_ID_COOKIE } from "./axiosCalls";
// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/editPost/:postid/", name: "EditPost", component: EditPostPage },
  { path: "/CreatePost", name: "Create New Post", component: CreatePostPage },
  { path: "/ProfilePage/:id", name: "ProfilePage", component: ProfilePage },
  { path: "/UserSearch", name: "UserSearch", component: UserSearch },
  { path: "/FriendsPage", name: "FriendsPage", component: FriendsPage },
  { path: "/authors/:id/posts/:postid", name: "UserPost", component: UserPost },
  {
    path: "/authors/:id/edit",
    name: "EditProfile",
    component: EditProfilePage,
  },
];

export const nav_bar_routes = [
  { path: "/", name: "Home", component: HomePage, icon: "mdi-home" },
  {
    path: "/about",
    name: "About",
    component: AboutPage,
    icon: "mdi-book-information-variant",
  },
  {
    path: "/CreatePost",
    name: "Create New Post",
    component: CreatePostPage,
    icon: "mdi-plus",
  },
  {
    path: `/ProfilePage/${Cookies.get(USER_AUTHOR_ID_COOKIE)}`,
    name: "ProfilePage",
    component: ProfilePage,
    icon: "mdi-account",
  },
  {
    path: "/UserSearch",
    name: "UserSearch",
    component: UserSearch,
    icon: "mdi-account-search",
  },
  {
    path: "/FriendsPage",
    name: "FriendsPage",
    component: FriendsPage,
    icon: "mdi-account-group",
  },
];

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
export const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHistory("/app"),
  routes, // short for `routes: routes`
});

router.beforeEach((to, from, next) => {
  if (to.path != "/" && !Cookies.get(USER_AUTHOR_ID_COOKIE)) {
    next({
      path: "/",
      params: { nextUrl: to.fullPath },
    });
  }
  next();
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
