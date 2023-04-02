<template>
  <div class="viewBox">
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em"
      class="loadingIcon"
    />
    <div v-else>
      <div
        style="
          display: flex;
          align-items: center;
          justify-content: center;
          padding-top: 10em;
        "
      >
        <img src="../assets/MediumLogo.png" style="width: 9em; padding: 2em" />
        <h1>InstaTonne</h1>
      </div>
      <div
        style="
          width: 40%;
          transform: translateX(80%);
          display: flex;
          flex-direction: column;
        "
        @keyup.enter="registerMode ? register() : login()"
      >
        <v-text-field v-model="username" label="Username" />
        <v-text-field
          v-model="password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          hint="At least 8 characters"
          @click:append="showPassword = !showPassword"
        />
        <div v-if="registerMode">
          <v-text-field
            v-model="confirmPassword"
            label="Confirm Password"
            :type="showConfirmPassword ? 'text' : 'password'"
            :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showConfirmPassword = !showConfirmPassword"
          />
          <div v-if="!passwordsMatch">Passwords must match</div>
        </div>
        <div>
          <v-btn
            class="button"
            :disabled="!canLogin"
            @click="registerMode ? register() : login()"
          >
            {{ registerMode ? "Sign Up" : "Login" }}
          </v-btn>
        </div>
        <div>
          <v-btn class="button" @click="registerMode = !registerMode">
            {{ registerMode ? "Return To Login" : "Register" }}
          </v-btn>
        </div>
        <v-snackbar v-model="showError">
          {{ errorMessage }}

          <template #actions>
            <v-btn color="blue" variant="text" @click="errorMessage = ''">
              Close
            </v-btn>
          </template>
        </v-snackbar>
        <!-- <v-btn
          class="button"
          @click="() => $emit('LoggedIn', true)"
        >
          FORCE LOGIN
        </v-btn> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from "vue";
import Cookies from "js-cookie";
import {
  createHTTP,
  createFormBody,
  USER_AUTHOR_ID_COOKIE,
} from "../axiosCalls";
import { router } from "../main";

const emits = defineEmits(["LoggedIn"]);

const username = ref("");

const registerMode = ref(false);

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const password = ref("");
const confirmPassword = ref("");

const errorMessage = ref("");

const showError = computed(() => errorMessage.value.length > 0);

const passwordsMatch = computed(() => password.value == confirmPassword.value);

const canLogin = computed(
  () =>
    (!registerMode.value || passwordsMatch.value) &&
    password.value.length >= 8 &&
    username.value.length > 0
);

async function login() {
  loading.value = true;
  const credentials = {
    username: username.value,
    password: password.value,
  };

  await createHTTP("login/")
    .post(credentials)
    .then((response: { authorId: string }) => {
      // login worked. Set cookies to show we are logged in
      // We assume that the session got set, if it didn't then the user needs to log in again
      // expire cookie in 12 hours
      Cookies.set(USER_AUTHOR_ID_COOKIE, response.authorId, { expires: 0.5 });
      emits("LoggedIn", response.authorId);
      loading.value = false;
      router.go();
    })
    .catch((response) => {
      console.log(response);
      // TODO: Uncomment this section
      // if(response.status === 403){
      //   errorMessage.value = "Admin has not approved of your account yet."
      // }
      // else{
      //   errorMessage.value = "Login failed"
      // }

      loading.value = false;
    });
}

async function register() {
  loading.value = true;
  // await createHTTP('login/').post('').then((response: { data: object }) => {
  // NOT WORKING YET
  const credentials = {
    username: username.value,
    password: password.value,
    check_password: confirmPassword.value,
  };
  await createHTTP("register/")
    .post(credentials)
    .then((response) => {
      // responseData.value = response.data;
      loading.value = false;
      registerMode.value = false;
    })
    .catch(() => {
      errorMessage.value = "Registration failed";
      loading.value = false;
    });
  return;
}

const loading = ref(false);
const postData = ref({});
// onBeforeMount(async () => {
//   await createHTTP("authors/1/posts/1/")
//     .get()
//     .then((response: { data: object }) => {
//       postData.value = response.data;
//       loading.value = false;
//     });
// });
</script>

<style scoped>
.button {
  width: 50%;
}
</style>
